#!/usr/bin/env python3
"""Fail if any published rate has gone stale for its cadence.

Run in CI after a refresh. A green run means every number on the site is
current for its own update cycle; a red run means the cron stopped, a source
changed shape, or a quarterly value was forgotten.

    python tools/check_freshness.py
    python tools/check_freshness.py --warn-only

Exit codes: 0 all fresh, 1 something is stale (or unreadable).
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RATES = ROOT / "content" / "rates.json"
PRODUCTS = ROOT / "content" / "products.json"

# Days a value may age before the site is considered out of date.
# Small savings are notified quarterly, so 100 days leaves room for a late
# notification; market yields should never be more than a fortnight old.
RULES = [
    ("quarterly", 100),
    ("moves continuously", 10),
    ("set at each auction", 10),
    ("moves weekly", 10),
    ("daily", 10),
]
DEFAULT_MAX_AGE = 30


def max_age(cadence: str) -> int:
    lowered = (cadence or "").lower()
    for needle, days in RULES:
        if needle in lowered:
            return days
    return DEFAULT_MAX_AGE


def main() -> int:
    parser = argparse.ArgumentParser(description="Check that published rates are current.")
    parser.add_argument("--warn-only", action="store_true", help="report but always exit 0")
    args = parser.parse_args()

    rates = json.loads(RATES.read_text(encoding="utf-8"))
    products = json.loads(PRODUCTS.read_text(encoding="utf-8"))
    values = rates.get("values", {})

    used = {
        product["rateKey"]
        for product in products
        if product.get("review", {}).get("status") == "approved" and product.get("rateKey")
    }

    today = date.today()
    stale: list[tuple[str, str, int, int]] = []

    print(f"Rate freshness — checked {today.isoformat()}")
    print("-" * 58)
    for key in sorted(used):
        entry = values.get(key)
        if not entry:
            print(f"  {key:<14} MISSING from rates.json")
            stale.append((key, "—", 999, 0))
            continue
        try:
            as_of = datetime.strptime(entry["asOf"], "%Y-%m-%d").date()
        except (KeyError, ValueError):
            print(f"  {key:<14} unreadable asOf {entry.get('asOf')!r}")
            stale.append((key, str(entry.get("asOf")), 999, 0))
            continue

        age = (today - as_of).days
        limit = max_age(entry.get("cadence", ""))
        status = "ok" if age <= limit else "STALE"
        print(f"  {key:<14} {entry['value']:>9}  {age:>4}d / {limit:>3}d  {status}")
        if age > limit:
            stale.append((key, entry["value"], age, limit))

    print("-" * 58)

    if not stale:
        print(f"  all {len(used)} published rates are within their update window")
        return 0

    print(f"  {len(stale)} rate(s) out of date:")
    for key, value, age, limit in stale:
        print(f"    - {key} ({value}): {age} days old, limit {limit}")
    print("\nRun `python refresh_rbi.py`, or update content/rates.json by hand for")
    print("the quarterly small-savings values, then rebuild.")
    return 0 if args.warn_only else 1


if __name__ == "__main__":
    raise SystemExit(main())
