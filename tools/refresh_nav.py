#!/usr/bin/env python3
"""Refresh the NAV of every fund and ETF already in the catalogue.

The products were imported once, but NAVs move daily, so they need the same
treatment as the RBI rates: pull, update in place, re-stamp the date.

    python tools/refresh_nav.py --dry-run
    python tools/refresh_nav.py
"""

from __future__ import annotations

import argparse
import json
import ssl
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RATES = ROOT / "content" / "rates.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def http_json(url: str, attempts: int = 4):
    """AMFI's mirror rate-limits bursts, so back off and retry."""
    last = None
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(request, timeout=30, context=ssl.create_default_context()) as response:
                return json.loads(response.read())
        except Exception as error:
            last = error
            time.sleep(1.5 * (attempt + 1))
    raise last


def money(value: float) -> str:
    text = f"{value:,.2f}"
    return "₹" + text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    rates = json.loads(RATES.read_text(encoding="utf-8"))
    values = rates["values"]
    keys = [key for key in values if key.startswith("nav-")]
    if not keys:
        print("No nav-* rates found.")
        return 0

    latest_dates = {}

    def refresh(key: str):
        code = key.split("-", 1)[1]
        try:
            payload = http_json(f"https://api.mfapi.in/mf/{code}")
            row = payload["data"][0]
            return key, row["nav"], row["date"]
        except Exception as error:  # one dead scheme must not stop the rest
            return key, None, type(error).__name__

    updated, unchanged, failed = [], 0, []

    with ThreadPoolExecutor(max_workers=4) as pool:
        for key, nav, date_text in pool.map(refresh, keys):
            if nav is None:
                failed.append((key, date_text))
                continue
            try:
                as_of = datetime.strptime(date_text, "%d-%m-%Y").strftime("%Y-%m-%d")
            except ValueError:
                failed.append((key, "bad date"))
                continue

            entry = values[key]
            new_value = money(float(nav))
            if entry.get("asOf") == as_of and entry.get("value") == new_value:
                unchanged += 1
                continue

            if not args.dry_run:
                entry["value"] = new_value
                entry["asOf"] = as_of
            updated.append((key, entry.get("value"), as_of))
            latest_dates[as_of] = latest_dates.get(as_of, 0) + 1

    newest = max(latest_dates) if latest_dates else "—"
    stamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    print(f"NAV refresh — {len(keys)} schemes checked")
    print("-" * 54)
    print(f"  updated   : {len(updated)}")
    print(f"  unchanged : {unchanged}")
    print(f"  failed    : {len(failed)}")
    if latest_dates:
        print(f"  newest NAV date: {newest}")
    for key, error in failed[:5]:
        print(f"    ! {key}: {error}")
    print("-" * 54)

    if args.dry_run:
        for key, value, as_of in updated[:5]:
            print(f"    {key:<14} → {value} ({as_of})")
        print("Dry run — nothing written.")
        return 0

    if updated:
        rates["generatedAt"] = stamp
        RATES.write_text(json.dumps(rates, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Updated {RATES.name}. Rebuild with: python build.py && python bundle.py")
    else:
        print("Already current. Nothing written.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
