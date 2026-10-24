#!/usr/bin/env python3
"""Recompute 1/3/5-year returns for every fund and ETF in the catalogue.

Returns were calculated once at import, so their "as of" date drifts behind the
NAV date. This rebuilds them from the latest history, repairing unit splits on
the way, so the figure and the date always agree.

    python tools/recompute_returns.py --dry-run
    python tools/recompute_returns.py
"""

from __future__ import annotations

import argparse
import json
import ssl
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRODUCTS = ROOT / "content" / "products.json"
RATES = ROOT / "content" / "rates.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
CLEAN_STEPS = (0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0)


def http_json(url: str):
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=30, context=ssl.create_default_context()) as response:
        return json.loads(response.read())


def clean_step(ratio: float):
    for step in CLEAN_STEPS:
        if abs(ratio - step) / step <= 0.03:
            return step
    return None


def history(code: str):
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


def repair(rows):
    fixed = [rows[0]] if rows else []
    broken = False
    for day, nav in rows[1:]:
        _, previous = fixed[-1]
        ratio = nav / previous
        if ratio > 1.35 or ratio < 0.75:
            step = clean_step(ratio)
            if step is None:
                broken = True
                fixed.append((day, nav))
                continue
            fixed = [(d, v * step) for d, v in fixed]
        fixed.append((day, nav))
    return fixed, broken


def cagr(rows, years: float):
    target = rows[-1][0] - timedelta(days=int(365.25 * years))
    past = [r for r in rows if r[0] <= target]
    if not past:
        return None
    start_day, start_nav = past[-1]
    end_day, end_nav = rows[-1]
    span = (end_day - start_day).days / 365.25
    if span < years * 0.9 or start_nav <= 0:
        return None
    return (pow(end_nav / start_nav, 1 / span) - 1) * 100


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    products = json.loads(PRODUCTS.read_text(encoding="utf-8"))
    rates = json.loads(RATES.read_text(encoding="utf-8"))
    targets = [p for p in products if str(p.get("rateKey", "")).startswith("nav-")]

    def work(product):
        code = product["rateKey"].split("-", 1)[1]
        try:
            rows = history(code)
            if len(rows) < 300:
                return product["slug"], None, "short history"
            fixed, broken = repair(rows)
            if broken:
                return product["slug"], ("broken", rows[-1][0].isoformat()), None
            values = (cagr(fixed, 1), cagr(fixed, 3), cagr(fixed, 5))
            return product["slug"], (
                "ok",
                rows[-1][0].isoformat(),
                tuple(round(v, 2) if v is not None else None for v in values),
            ), None
        except Exception as error:
            return product["slug"], None, type(error).__name__

    results = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        for row in pool.map(work, targets):
            results.append(row)

    by_slug = {p["slug"]: p for p in products}
    changed = broken = failed = 0
    for slug, data, error in results:
        if error:
            failed += 1
            continue
        product = by_slug[slug]
        if data[0] == "broken":
            product["returns"] = {
                "oneYear": None, "threeYear": None, "fiveYear": None,
                "asOf": data[1], "basis": "NAV series has an unexplained break; returns withheld",
            }
            broken += 1
            continue
        _, as_of, values = data
        product["returns"] = {
            "oneYear": values[0], "threeYear": values[1], "fiveYear": values[2],
            "asOf": as_of, "basis": "CAGR from AMFI NAV, adjusted for unit splits",
        }
        if product.get("rateKey") in rates["values"]:
            rates["values"][product["rateKey"]]["asOf"] = as_of
        changed += 1

    print(f"recomputed {changed} · withheld {broken} · failed {failed} of {len(targets)}")
    if not args.dry_run:
        PRODUCTS.write_text(json.dumps(products, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        RATES.write_text(json.dumps(rates, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
