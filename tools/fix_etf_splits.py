#!/usr/bin/env python3
"""Repair fund/ETF return figures that a NAV unit split has broken.

A split leaves a single-day jump in the NAV series, so any CAGR that spans it
is meaningless (a 10:1 split shows up as a 90% loss). This rebuilds the series
with the split removed, recomputes the returns and rewrites the record.

    python tools/fix_etf_splits.py --dry-run
    python tools/fix_etf_splits.py
"""

from __future__ import annotations

import argparse
import json
import ssl
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRODUCTS = ROOT / "content" / "products.json"
RATES = ROOT / "content" / "rates.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

SPLIT_HIGH = 1.35   # a jump upward larger than this is a consolidation
SPLIT_LOW = 0.75    # a drop larger than this is a split


def http_json(url: str):
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=30, context=ssl.create_default_context()) as response:
        return json.loads(response.read())


def clean_history(code: str):
    payload = http_json(f"https://api.mfapi.in/mf/{code}")
    rows = []
    for row in payload.get("data", []):
        try:
            day = datetime.strptime(row["date"], "%d-%m-%Y").date()
            nav = float(row["nav"])
        except (KeyError, ValueError):
            continue
        if nav > 0:
            rows.append((day, nav))
    rows.sort()
    return rows


CLEAN_STEPS = (0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0)


def clean_step(ratio: float):
    """A unit split always lands on a simple ratio. Anything else is a data
    error, not a corporate action, so the figure gets withheld instead."""
    for step in CLEAN_STEPS:
        if abs(ratio - step) / step <= 0.03:
            return step
    return None


def repair(rows):
    """Return (adjusted rows, list of (date, factor))."""
    fixed = [rows[0]] if rows else []
    events = []
    for day, nav in rows[1:]:
        prev_day, prev_nav = fixed[-1]
        ratio = nav / prev_nav
        if ratio > SPLIT_HIGH or ratio < SPLIT_LOW:
            # A 10:1 split shows as ratio 0.1, so earlier prices must be
            # multiplied by 0.1 to sit on today's scale.
            factor = clean_step(ratio)
            if factor is None:
                events.append((day, ratio, None))  # unexplained break
                fixed.append((day, nav))
                continue
            events.append((day, ratio, factor))
            fixed = [(d, v * factor) for d, v in fixed]
        fixed.append((day, nav))
    return fixed, events


def cagr(rows, years: float):
    target = rows[-1][0] - timedelta(days=int(365.25 * years))
    past = [r for r in rows if r[0] <= target]
    if not past:
        return None
    start_day, start_nav = past[-1]
    end_day, end_nav = rows[-1]
    span_years = (end_day - start_day).days / 365.25
    if span_years < years * 0.9 or start_nav <= 0:
        return None
    return (pow(end_nav / start_nav, 1 / span_years) - 1) * 100


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    products = json.loads(PRODUCTS.read_text(encoding="utf-8"))
    rates = json.loads(RATES.read_text(encoding="utf-8"))
    changed = 0

    for product in products:
        returns = product.get("returns") or {}
        values = [returns.get("oneYear"), returns.get("threeYear"), returns.get("fiveYear")]
        if not any(v is not None and (v > 60 or v < -40) for v in values):
            continue

        key = product.get("rateKey", "")
        if not key.startswith("nav-"):
            continue
        code = key.split("-", 1)[1]

        try:
            rows = clean_history(code)
        except Exception as error:
            print(f"  ! {product['name'][:40]}: {type(error).__name__}")
            continue
        if len(rows) < 300:
            print(f"  ! {product['name'][:40]}: only {len(rows)} rows")
            continue

        fixed, events = repair(rows)
        if any(f is None for _, _, f in events):
            note = ", ".join(f"{d} x{r:.2f}?" for d, r, f in events if f is None)
            print(f"  ~ {product['name'][:40]}: unexplained NAV break ({note}) — returns withheld")
            if not args.dry_run:
                product["returns"] = {
                    "oneYear": None, "threeYear": None, "fiveYear": None,
                    "asOf": rows[-1][0].isoformat(),
                    "basis": "NAV series contains an unexplained break, so no return is published",
                }
                changed += 1
            continue
        one, three, five = cagr(fixed, 1), cagr(fixed, 3), cagr(fixed, 5)

        if any(v is not None and (v > 80 or v < -60) for v in (one, three, five)):
            print(f"  ! {product['name'][:40]}: still implausible after repair, skipped")
            continue

        old = (returns.get("oneYear"), returns.get("threeYear"), returns.get("fiveYear"))
        new = (round(one, 2) if one is not None else None,
               round(three, 2) if three is not None else None,
               round(five, 2) if five is not None else None)
        note = ", ".join(f"{d} x{f:g}" for d, _, f in events) or "no split found"

        print(f"  {product['name'][:44]:<44} {old} -> {new}   [{note}]")
        if not args.dry_run:
            product["returns"] = {
                "oneYear": new[0], "threeYear": new[1], "fiveYear": new[2],
                "asOf": rows[-1][0].isoformat(),
                "basis": "CAGR from AMFI NAV, adjusted for unit splits",
            }
            if key in rates["values"]:
                rates["values"][key]["asOf"] = rows[-1][0].isoformat()
                rates["values"][key]["value"] = "₹" + f"{rows[-1][1]:,.2f}"
            changed += 1

    if not args.dry_run and changed:
        PRODUCTS.write_text(json.dumps(products, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        RATES.write_text(json.dumps(rates, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"\n{changed} record(s) rewritten" if not args.dry_run else "\ndry run — nothing written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
