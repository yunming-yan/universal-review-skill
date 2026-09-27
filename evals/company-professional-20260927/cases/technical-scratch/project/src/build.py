"""Deliberately uses the current directory for generated artifacts."""

import json
from pathlib import Path


def main():
    current = Path.cwd()
    (current / ".cache").mkdir(exist_ok=True)
    (current / "build").mkdir(exist_ok=True)
    (current / ".cache" / "index.json").write_text(json.dumps({"status": "built"}), encoding="utf-8")
    (current / "build" / "report.json").write_text(json.dumps({"result": "ready"}), encoding="utf-8")
    (current / "run.log").write_text("synthetic build completed\n", encoding="utf-8")


if __name__ == "__main__":
    main()
