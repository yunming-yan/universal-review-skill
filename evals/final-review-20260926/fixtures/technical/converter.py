import json
import sys
from datetime import datetime
from pathlib import Path


def convert(rows):
    by_id = {}
    for row in rows:
        quantity = row.get("quantity") or 1
        stamp = datetime.fromisoformat(row["timestamp"])
        by_id[row["id"]] = {
            "id": row["id"],
            "timestamp": stamp.replace(tzinfo=None).isoformat() + "Z",
            "quantity": quantity,
        }
    return list(by_id.values())


def main():
    rows = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    Path(sys.argv[2]).write_text(json.dumps(convert(rows)), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
