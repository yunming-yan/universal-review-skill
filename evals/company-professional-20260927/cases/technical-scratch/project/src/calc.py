"""Tiny receipt calculator; intentionally flawed training fixture."""

import json
import sys


def total_cents(quantity, unit_cents):
    if not isinstance(quantity, int) or quantity <= 0:
        raise ValueError("quantity must be a positive integer")
    if not isinstance(unit_cents, int) or unit_cents <= 0:
        raise ValueError("unit_cents must be a positive integer")
    return quantity * unit_cents


def main():
    try:
        payload = json.load(sys.stdin)
        amount = total_cents(payload["quantity"], payload["unit_cents"])
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"invalid input: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"total_cents": amount}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
