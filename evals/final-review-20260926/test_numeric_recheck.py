"""CLI tests, plus controlled filesystem failures, for numeric_recheck.py."""

import contextlib
import errno
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


HERE = Path(__file__).resolve().parent
TOOL = HERE.parents[1] / "skills" / "universal-review" / "scripts" / "numeric_recheck.py"


def load_tool():
    spec = importlib.util.spec_from_file_location("tested_numeric_recheck", TOOL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def item(metric_id="metric-1", operation="sum", operands=None, **changes):
    result = {
        "metric_id": metric_id,
        "operation": operation,
        "operands": ["0.1", "0.2"] if operands is None else operands,
        "unit": "元",
        "source_refs": ["用户提供的表A!B2", "用户提供的表A!B3"],
    }
    result.update(changes)
    return result


class NumericRecheckCliTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(dir=HERE)
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.input = self.directory / "input.json"
        self.output = self.directory / "result.json"

    def run_tool(self, calculations, *, raw_bytes=None):
        if raw_bytes is None:
            raw_bytes = json.dumps(
                {"schema_version": 1, "calculations": calculations},
                ensure_ascii=False,
            ).encode("utf-8")
        self.input.write_bytes(raw_bytes)
        completed = subprocess.run(
            [sys.executable, str(TOOL), str(self.input), str(self.output)],
            capture_output=True,
            text=True,
            check=False,
        )
        return completed, raw_bytes

    def assert_rejected(self, calculations, *, raw_bytes=None, error_fragment=None):
        completed, original = self.run_tool(calculations, raw_bytes=raw_bytes)
        self.assertEqual(completed.returncode, 2, completed.stderr)
        self.assertTrue(completed.stderr.startswith("numeric_recheck: "), completed.stderr)
        self.assertFalse(self.output.exists())
        self.assertEqual(self.input.read_bytes(), original)
        if error_fragment:
            self.assertIn(error_fragment, completed.stderr)

    def test_exact_arithmetic_and_provenance(self):
        calculations = [
            item("sum", "sum", ["0.1", "0.2"]),
            item("difference", "difference", ["10.00", "3.75"]),
            item("product", "product", ["0.25", "-0.4"]),
            item("ratio", "ratio", ["1", "3"], unit="倍"),
            item("change", "percent_change", ["80", "100"], unit="%"),
        ]
        completed, original = self.run_tool(calculations)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(self.input.read_bytes(), original)
        output = json.loads(self.output.read_text(encoding="utf-8"))
        self.assertEqual(output["input_sha256"], hashlib.sha256(original).hexdigest())
        self.assertEqual(
            [row["exact_fraction"] for row in output["results"]],
            ["3/10", "25/4", "-1/10", "1/3", "25/1"],
        )
        self.assertEqual(output["results"][0]["operands"], ["0.1", "0.2"])
        self.assertEqual(output["results"][0]["unit"], "元")
        self.assertEqual(
            output["results"][0]["source_refs"],
            ["用户提供的表A!B2", "用户提供的表A!B3"],
        )
        self.assertIn("user-supplied", output["source_refs_note"].lower())
        self.assertIn("not verified", output["source_refs_note"].lower())
        self.assertTrue(all("rounded_decimal" not in row for row in output["results"]))

    def test_rounding_is_explicit_and_uses_ties_as_requested(self):
        calculations = [
            item("even-down", "sum", ["2.345"], rounding={"places": 2, "mode": "half_even"}),
            item("even-up", "sum", ["2.355"], rounding={"places": 2, "mode": "half_even"}),
            item("half-up", "sum", ["2.345"], rounding={"places": 2, "mode": "half_up"}),
            item("toward-zero", "sum", ["-2.359"], rounding={"places": 2, "mode": "toward_zero"}),
        ]
        completed, _ = self.run_tool(calculations)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        output = json.loads(self.output.read_text(encoding="utf-8"))
        self.assertEqual(
            [row["rounded_decimal"] for row in output["results"]],
            ["2.34", "2.36", "2.35", "-2.35"],
        )
        self.assertEqual(output["results"][0]["rounding"], {"places": 2, "mode": "half_even"})

    def test_no_implicit_numeric_conversions_or_defaults(self):
        for bad in ["NaN", "Infinity", "-Infinity", "1e3", "1,000", " 1", "", 1, 0.5, True, None]:
            with self.subTest(bad=bad):
                self.assert_rejected([item(operands=[bad])], error_fragment="operand")
                if self.input.exists():
                    self.input.unlink()

    def test_unknown_operation_and_bad_arity_are_rejected(self):
        cases = [
            item(operation="average"),
            item(operation="sum", operands=[]),
            item(operation="difference", operands=["1"]),
            item(operation="ratio", operands=["1", "2", "3"]),
            item(operation="percent_change", operands=["1"]),
        ]
        for bad in cases:
            with self.subTest(bad=bad):
                self.assert_rejected([bad])
                self.input.unlink()

    def test_division_by_zero_is_rejected_for_ratio_and_change(self):
        for bad in [
            item(operation="ratio", operands=["1", "0"], unit="倍"),
            item(operation="percent_change", operands=["0", "100"], unit="%"),
        ]:
            with self.subTest(bad=bad):
                self.assert_rejected([bad], error_fragment="zero")
                self.input.unlink()

    def test_percent_change_requires_percent_result_unit(self):
        self.assert_rejected(
            [item(operation="percent_change", operands=["80", "100"], unit="元")],
            error_fragment="unit",
        )

    def test_metadata_and_rounding_must_be_complete(self):
        cases = [
            item(unit=""),
            item(source_refs="a locator"),
            item(source_refs=[""]),
            item(rounding={"places": 2}),
            item(rounding={"places": True, "mode": "half_up"}),
            item(rounding={"places": -1, "mode": "half_up"}),
            item(rounding={"places": 2, "mode": "unknown"}),
        ]
        for bad in cases:
            with self.subTest(bad=bad):
                self.assert_rejected([bad])
                self.input.unlink()

    def test_duplicate_ids_keys_and_malformed_json_are_rejected(self):
        self.assert_rejected([item(), item()])
        self.input.unlink()
        self.assert_rejected(
            [],
            raw_bytes=b'{"schema_version":1,"schema_version":1,"calculations":[]}',
            error_fragment="duplicate",
        )
        self.input.unlink()
        self.assert_rejected([], raw_bytes=b"{bad json")

    def test_unpaired_unicode_escape_is_rejected_before_output_creation(self):
        self.assert_rejected(
            [],
            raw_bytes=(
                b'{"schema_version":1,"calculations":[{'
                b'"metric_id":"\\ud800","operation":"sum","operands":["1"],'
                b'"unit":"unit","source_refs":[]}]}'
            ),
        )

    def test_oversized_json_number_is_rejected_without_traceback(self):
        raw = (
            b'{"schema_version":1,"calculations":[{'
            b'"metric_id":"large","operation":"sum","operands":['
            + b"9" * 5000
            + b'],"unit":"unit","source_refs":[]}]}'
        )
        self.assert_rejected([], raw_bytes=raw)

    def test_existing_output_is_never_overwritten(self):
        self.output.write_text("preserve me", encoding="utf-8")
        completed, original = self.run_tool([item()])
        self.assertEqual(completed.returncode, 2)
        self.assertTrue(completed.stderr.startswith("numeric_recheck: "), completed.stderr)
        self.assertEqual(self.output.read_text(encoding="utf-8"), "preserve me")
        self.assertEqual(self.input.read_bytes(), original)

    def test_partial_write_failure_never_publishes_result(self):
        original = json.dumps({"schema_version": 1, "calculations": [item()]}).encode("utf-8")
        self.input.write_bytes(original)
        module = load_tool()
        path_open = Path.open
        fdopen = os.fdopen

        class ShortWriter:
            def __init__(self, stream):
                self.stream = stream

            def __enter__(self):
                return self

            def __exit__(self, *_):
                self.stream.close()

            def write(self, data):
                self.stream.write(data[:17])
                raise OSError("injected write failure after 17 bytes")

        def intercept_path_open(path, *args, **kwargs):
            stream = path_open(path, *args, **kwargs)
            mode = args[0] if args else kwargs.get("mode", "r")
            return ShortWriter(stream) if mode in {"xb", "wb"} else stream

        def intercept_fdopen(fd, *args, **kwargs):
            stream = fdopen(fd, *args, **kwargs)
            mode = args[0] if args else kwargs.get("mode", "r")
            return ShortWriter(stream) if mode in {"xb", "wb"} else stream

        error = io.StringIO()
        with patch.object(Path, "open", intercept_path_open), patch.object(os, "fdopen", intercept_fdopen):
            with contextlib.redirect_stderr(error):
                code = module.main([str(self.input), str(self.output)])
        self.assertEqual(code, 2, error.getvalue())
        self.assertFalse(self.output.exists())
        self.assertEqual(self.input.read_bytes(), original)
        self.assertEqual(set(self.directory.iterdir()), {self.input})

    def test_publish_race_preserves_other_writers_result(self):
        self.input.write_text(
            json.dumps({"schema_version": 1, "calculations": [item()]}), encoding="utf-8"
        )
        module = load_tool()
        link = os.link

        def competing_writer(source, target, *args, **kwargs):
            Path(target).write_bytes(b"other writer")
            return link(source, target, *args, **kwargs)

        error = io.StringIO()
        with patch.object(os, "link", competing_writer), contextlib.redirect_stderr(error):
            code = module.main([str(self.input), str(self.output)])
        self.assertEqual(code, 2, error.getvalue())
        self.assertEqual(self.output.read_bytes(), b"other writer")
        self.assertEqual(set(self.directory.iterdir()), {self.input, self.output})

    def test_unavailable_hard_link_fails_without_result(self):
        self.input.write_text(
            json.dumps({"schema_version": 1, "calculations": [item()]}), encoding="utf-8"
        )
        module = load_tool()
        error = io.StringIO()
        with patch.object(os, "link", side_effect=OSError(errno.ENOTSUP, "hard links unavailable")):
            with contextlib.redirect_stderr(error):
                code = module.main([str(self.input), str(self.output)])
        self.assertEqual(code, 2, error.getvalue())
        self.assertFalse(self.output.exists())
        self.assertEqual(set(self.directory.iterdir()), {self.input})

    def test_cleanup_failure_after_publication_has_distinct_status(self):
        original = json.dumps({"schema_version": 1, "calculations": [item()]}).encode("utf-8")
        self.input.write_bytes(original)
        module = load_tool()
        unlink = Path.unlink
        attempted_temporary_paths = []

        def deny_temporary_cleanup(path, *args, **kwargs):
            if path.name.startswith(f".{self.output.name}.") and path.suffix == ".tmp":
                attempted_temporary_paths.append(path)
                raise PermissionError("injected temporary cleanup denial")
            return unlink(path, *args, **kwargs)

        error = io.StringIO()
        with patch.object(Path, "unlink", deny_temporary_cleanup), contextlib.redirect_stderr(error):
            code = module.main([str(self.input), str(self.output)])
        self.assertEqual(code, 3, error.getvalue())
        self.assertEqual(len(attempted_temporary_paths), 1)
        temporary = attempted_temporary_paths[0]
        self.assertTrue(temporary.exists())
        self.assertEqual(self.output.read_bytes(), temporary.read_bytes())
        self.assertEqual(
            json.loads(self.output.read_text(encoding="utf-8"))["results"][0]["exact_fraction"],
            "3/10",
        )
        self.assertEqual(self.input.read_bytes(), original)
        self.assertIn("RESULT_PUBLISHED_CLEANUP_PENDING", error.getvalue())
        self.assertIn(str(self.output.resolve()), error.getvalue())
        self.assertIn(str(temporary), error.getvalue())
        self.assertIn("do not retry", error.getvalue().lower())

    def test_success_publishes_and_cleans_temporary_file(self):
        completed, _ = self.run_tool([item()])
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertTrue(self.output.exists())
        self.assertEqual(set(self.directory.iterdir()), {self.input, self.output})

    def test_silent_cleanup_failure_is_not_reported_as_success(self):
        self.input.write_text(
            json.dumps({"schema_version": 1, "calculations": [item()]}), encoding="utf-8"
        )
        module = load_tool()
        unlink = Path.unlink

        def skip_temporary_cleanup(path, *args, **kwargs):
            if path.name.startswith(f".{self.output.name}.") and path.suffix == ".tmp":
                return None
            return unlink(path, *args, **kwargs)

        error = io.StringIO()
        with patch.object(Path, "unlink", skip_temporary_cleanup), contextlib.redirect_stderr(error):
            code = module.main([str(self.input), str(self.output)])
        self.assertEqual(code, 3, error.getvalue())
        self.assertTrue(self.output.exists())
        self.assertIn("RESULT_PUBLISHED_CLEANUP_PENDING", error.getvalue())
        self.assertEqual(len(list(self.directory.glob("*.tmp"))), 1)

    def test_prepublication_failure_with_cleanup_failure_stays_exit_two(self):
        self.input.write_text(
            json.dumps({"schema_version": 1, "calculations": [item()]}), encoding="utf-8"
        )
        module = load_tool()
        unlink = Path.unlink

        def deny_temporary_cleanup(path, *args, **kwargs):
            if path.suffix == ".tmp":
                raise PermissionError("injected temporary cleanup denial")
            return unlink(path, *args, **kwargs)

        error = io.StringIO()
        with patch.object(os, "link", side_effect=OSError(errno.ENOTSUP, "hard links unavailable")):
            with patch.object(Path, "unlink", deny_temporary_cleanup):
                with contextlib.redirect_stderr(error):
                    code = module.main([str(self.input), str(self.output)])
        self.assertEqual(code, 2, error.getvalue())
        self.assertFalse(self.output.exists())
        self.assertIn("result was not published", error.getvalue())
        self.assertEqual(len(list(self.directory.glob("*.tmp"))), 1)

    def test_ratio_requires_dimensionless_result_unit(self):
        for unit in ["%", "percent", "bps", "元/人"]:
            with self.subTest(unit=unit):
                try:
                    self.assert_rejected([item(operation="ratio", operands=["1", "4"], unit=unit)],
                                         error_fragment="unit")
                finally:
                    self.input.unlink(missing_ok=True)
                    self.output.unlink(missing_ok=True)

    def test_percentage_applies_explicit_hundredfold_scale(self):
        completed, _ = self.run_tool([
            item(operation="percentage", operands=["1", "4"], unit="%",
                 rounding={"places": 2, "mode": "half_even"})
        ])
        self.assertEqual(completed.returncode, 0, completed.stderr)
        row = json.loads(self.output.read_text(encoding="utf-8"))["results"][0]
        self.assertEqual(row["exact_fraction"], "25/1")
        self.assertEqual(row["rounded_decimal"], "25.00")
        self.assertEqual(row["unit"], "%")

    def test_percentage_rejects_wrong_unit_and_zero_denominator(self):
        self.assert_rejected([item(operation="percentage", operands=["1", "4"], unit="times")],
                             error_fragment="unit")
        self.input.unlink()
        self.assert_rejected([item(operation="percentage", operands=["1", "0"], unit="%")],
                             error_fragment="zero")

    def test_percent_change_requires_positive_baseline(self):
        for new in ["-50", "-150", "50"]:
            with self.subTest(new=new):
                try:
                    self.assert_rejected(
                        [item(operation="percent_change", operands=["-100", new], unit="%")],
                        error_fragment="positive",
                    )
                finally:
                    self.input.unlink(missing_ok=True)
                    self.output.unlink(missing_ok=True)

    def test_operand_digit_limit_is_explicit_and_stable(self):
        self.assert_rejected([item(operands=["9" * 1201])], error_fragment="1200")

    def test_calculation_digit_budget_is_explicit_and_stable(self):
        self.assert_rejected([item(operation="product", operands=["9" * 1001] * 4)],
                             error_fragment="4000")

    def test_declared_digit_boundary_still_computes_exactly(self):
        completed, _ = self.run_tool([
            item("operand-boundary", "sum", ["9" * 1200, "1"]),
            item("budget-boundary", "product", ["9" * 1000] * 4,
                 rounding={"places": 50, "mode": "half_even"}),
        ])
        self.assertEqual(completed.returncode, 0, completed.stderr)
        rows = json.loads(self.output.read_text(encoding="utf-8"))["results"]
        self.assertEqual(rows[0]["exact_fraction"], "1" + "0" * 1200 + "/1")
        self.assertEqual(len(rows[1]["exact_fraction"].split("/")[0]), 4000)
        self.assertTrue(rows[1]["rounded_decimal"].endswith("." + "0" * 50))

    def test_large_json_numeric_token_gets_stable_boundary_error(self):
        raw = (
            b'{"schema_version":1,"calculations":[{'
            b'"metric_id":"large","operation":"sum","operands":['
            + b"9" * 5000
            + b'],"unit":"unit","source_refs":[]}]}'
        )
        self.assert_rejected([], raw_bytes=raw, error_fragment="JSON numeric token")


if __name__ == "__main__":
    unittest.main()
