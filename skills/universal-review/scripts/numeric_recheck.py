#!/usr/bin/env python3
"""Exact arithmetic from an explicit JSON ledger; no source verification."""

import argparse
from decimal import Decimal
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile


DECIMAL_PATTERN = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]+)?|\.[0-9]+)\Z")
OPERAND_COUNTS = {
    "sum": (1, None),
    "difference": (2, 2),
    "product": (2, None),
    "ratio": (2, 2),
    "percentage": (2, 2),
    "percent_change": (2, 2),
}
ROUNDING_MODES = {"half_even", "half_up", "toward_zero"}
MAX_OPERAND_DIGITS = 1200
MAX_CALCULATION_DIGITS = 4000
SOURCE_REFS_NOTE = (
    "source_refs are user-supplied locators; source authenticity was not verified."
)


class InputError(ValueError):
    """A ledger or calculation failed validation."""


class ResultPublishedCleanupPending(Exception):
    """The complete result is public, but its temporary name remains."""


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InputError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise InputError(f"non-finite JSON value: {value}")


def bounded_json_int(value):
    if len(value.lstrip("-")) > MAX_OPERAND_DIGITS:
        raise InputError(
            f"JSON numeric token exceeds {MAX_OPERAND_DIGITS} digits; operands must be strings"
        )
    return int(value)


def reject_json_float(_value):
    raise InputError("JSON numeric token is invalid; operands must be decimal strings")


def require_fields(value, required, optional, label):
    if not isinstance(value, dict):
        raise InputError(f"{label} must be an object")
    missing = required - value.keys()
    unknown = value.keys() - required - optional
    if missing:
        raise InputError(f"{label} missing field(s): {', '.join(sorted(missing))}")
    if unknown:
        raise InputError(f"{label} unknown field(s): {', '.join(sorted(unknown))}")


def nonempty_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise InputError(f"{label} must be a nonempty string")
    return value


def operand_digit_count(value, label):
    if not isinstance(value, str) or DECIMAL_PATTERN.fullmatch(value) is None:
        raise InputError(f"{label} operand must be an explicit decimal string")
    digits = len(value.lstrip("+-").replace(".", ""))
    if digits > MAX_OPERAND_DIGITS:
        raise InputError(f"{label} operand exceeds {MAX_OPERAND_DIGITS} decimal digits")
    return digits


def validate_rounding(value, label):
    require_fields(value, {"places", "mode"}, set(), f"{label}.rounding")
    places = value["places"]
    mode = value["mode"]
    if type(places) is not int or not 0 <= places <= 50:
        raise InputError(f"{label}.rounding.places must be an integer from 0 to 50")
    if not isinstance(mode, str) or mode not in ROUNDING_MODES:
        raise InputError(f"{label}.rounding.mode must be half_even, half_up, or toward_zero")
    return {"places": places, "mode": mode}


def rounded_decimal(value, places, mode):
    scaled_numerator = abs(value.numerator) * 10**places
    whole, remainder = divmod(scaled_numerator, value.denominator)
    if mode == "half_up" and 2 * remainder >= value.denominator:
        whole += 1
    elif mode == "half_even" and (
        2 * remainder > value.denominator
        or (2 * remainder == value.denominator and whole % 2 == 1)
    ):
        whole += 1
    digits = str(whole).zfill(places + 1)
    rendered = digits if places == 0 else f"{digits[:-places]}.{digits[-places:]}"
    return ("-" if value < 0 and whole != 0 else "") + rendered


def calculate(operation, operands, label):
    if operation == "sum":
        return sum(operands, Fraction(0))
    if operation == "difference":
        return operands[0] - operands[1]
    if operation == "product":
        result = Fraction(1)
        for operand in operands:
            result *= operand
        return result
    if operation in {"ratio", "percentage"}:
        if operands[1] == 0:
            raise InputError(f"{label}: zero {operation} denominator")
        quotient = operands[0] / operands[1]
        return quotient * 100 if operation == "percentage" else quotient
    if operands[0] <= 0:
        raise InputError(f"{label}: percent_change baseline must be positive and nonzero")
    return (operands[1] - operands[0]) / operands[0] * 100


def process_calculation(record):
    require_fields(
        record,
        {"metric_id", "operation", "operands", "unit", "source_refs"},
        {"rounding"},
        "calculation",
    )
    metric_id = nonempty_text(record["metric_id"], "metric_id")
    label = f"metric {metric_id}"
    operation = record["operation"]
    if not isinstance(operation, str) or operation not in OPERAND_COUNTS:
        raise InputError(f"{label}: unknown operation: {operation!r}")
    raw_operands = record["operands"]
    if not isinstance(raw_operands, list):
        raise InputError(f"{label}.operands must be an array")
    minimum, maximum = OPERAND_COUNTS[operation]
    if len(raw_operands) < minimum or (maximum is not None and len(raw_operands) > maximum):
        raise InputError(f"{label}: {operation} needs {minimum}" + (
            " or more operands" if maximum is None else " operands"
        ))
    digit_total = sum(
        operand_digit_count(value, f"{label}[{index}]")
        for index, value in enumerate(raw_operands)
    )
    if digit_total > MAX_CALCULATION_DIGITS:
        raise InputError(
            f"{label} operands exceed {MAX_CALCULATION_DIGITS} decimal digits in total"
        )
    operands = [Fraction(Decimal(value)) for value in raw_operands]
    unit = nonempty_text(record["unit"], f"{label}.unit")
    if operation == "ratio" and unit not in {"1", "times", "倍"}:
        raise InputError(f"{label}.unit must be 1, times, or 倍 for ratio")
    if operation in {"percentage", "percent_change"} and unit != "%":
        raise InputError(f"{label}.unit must be % for {operation}")
    source_refs = record["source_refs"]
    if not isinstance(source_refs, list) or any(
        not isinstance(ref, str) or not ref.strip() for ref in source_refs
    ):
        raise InputError(f"{label}.source_refs must be an array of nonempty strings")
    rounding = validate_rounding(record["rounding"], label) if "rounding" in record else None
    value = calculate(operation, operands, label)
    result = {
        "metric_id": metric_id,
        "operation": operation,
        "operands": raw_operands,
        "unit": unit,
        "source_refs": source_refs,
        "exact_fraction": f"{value.numerator}/{value.denominator}",
    }
    if rounding is not None:
        result["rounding"] = rounding
        result["rounded_decimal"] = rounded_decimal(value, rounding["places"], rounding["mode"])
    return result


def process_ledger(raw):
    document = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique_keys,
        parse_constant=reject_constant,
        parse_int=bounded_json_int,
        parse_float=reject_json_float,
    )
    require_fields(document, {"schema_version", "calculations"}, set(), "ledger")
    if type(document["schema_version"]) is not int or document["schema_version"] != 1:
        raise InputError("schema_version must be 1")
    calculations = document["calculations"]
    if not isinstance(calculations, list) or not calculations:
        raise InputError("calculations must be a nonempty array")
    results = []
    identifiers = set()
    for calculation in calculations:
        result = process_calculation(calculation)
        metric_id = result["metric_id"]
        if metric_id in identifiers:
            raise InputError(f"duplicate metric_id: {metric_id}")
        identifiers.add(metric_id)
        results.append(result)
    return {
        "schema_version": 1,
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "source_refs_note": SOURCE_REFS_NOTE,
        "results": results,
    }


def publish_new_result(path, content):
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    published = False
    try:
        with os.fdopen(descriptor, "wb") as stream:
            if stream.write(content) != len(content):
                raise OSError("incomplete temporary result write")
            stream.flush()
            os.fsync(stream.fileno())
        if temporary.read_bytes() != content:
            raise OSError("temporary result verification failed")
        os.link(temporary, path)
        published = True
    finally:
        try:
            temporary.unlink(missing_ok=True)
            if temporary.exists():
                raise OSError("temporary file still exists after cleanup")
        except OSError as error:
            if published:
                raise ResultPublishedCleanupPending(
                    f"RESULT_PUBLISHED_CLEANUP_PENDING: complete result={path.resolve()}; "
                    f"temporary={temporary}; cleanup error={error}; "
                    "do not retry or delete the published result blindly"
                ) from error
            raise OSError(
                f"result was not published; temporary cleanup failed at {temporary}: {error}"
            ) from error


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", type=Path)
    parser.add_argument("output_json", type=Path)
    args = parser.parse_args(argv)
    try:
        raw = args.input_json.read_bytes()
        result = process_ledger(raw)
        encoded = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        publish_new_result(args.output_json, encoded)
    except ResultPublishedCleanupPending as error:
        print(f"numeric_recheck: {error}", file=sys.stderr)
        return 3
    except (ValueError, UnicodeError, OSError) as error:
        print(f"numeric_recheck: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
