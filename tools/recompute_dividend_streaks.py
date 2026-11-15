#!/usr/bin/env python3
"""Recompute the original 48 dividend streaks from the payment history.

The first batch of Dividend Champions used streak figures supplied as a list
and never independently verified. This rewrites them from Yahoo's dividend
records, using the same method as the newer batch, so every record on the site
means the same thing.

    python tools/recompute_dividend_streaks.py --dry-run
    python tools/recompute_dividend_streaks.py
"""

from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from import_dividend_stocks import history, streak_years  # noqa: E402

PRODUCTS = ROOT / "content" / "products.json"


def refresh(product: dict) -> dict:
    rows = history(product["symbol"])
    if len(rows) < 4:
        return {"slug": product["slug"], "ok": False, "reason": "no history"}
    streak, first_year = streak_years(rows)
    return {
        "slug": product["slug"],
        "name": product["name"],
        "ok": True,
        "old": product.get("streakYears", 0),
        "new": streak,
        "first_year": first_year,
        "total": len(rows),
        "dividends": rows[:10],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    products = json.loads(PRODUCTS.read_text(encoding="utf-8"))
    originals = [
        p for p in products
        if p["category"] == "dividend-champions"
        and "computed" not in (p.get("review", {}).get("notes") or "").lower()
    ]
    print(f"original records to recompute: {len(originals)}")

    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(refresh, originals))

    lowered = [r for r in results if r["ok"] and r["new"] < r["old"]]
    unchanged = [r for r in results if r["ok"] and r["new"] == r["old"]]
    failed = [r for r in results if not r["ok"]]

    print(f"  lowered : {len(lowered)}")
    print(f"  same    : {len(unchanged)}")
    print(f"  failed  : {len(failed)}")

    for r in sorted(lowered, key=lambda x: x["old"] - x["new"], reverse=True)[:10]:
        print(f"    {r['name'][:38]:<38} {r['old']:>3} -> {r['new']:>3}  (history from {r['first_year']})")

    if args.dry_run:
        return 0

    by_slug = {p["slug"]: p for p in products}
    for r in results:
        if not r["ok"]:
            # no public payment history — label the figure instead of implying it was checked
            p = by_slug[r["slug"]]
            p["source"]["note"] = (
                "Streak reported by the site, not verified: no public payment history available for this company."
            )
            p["review"]["notes"] = "Listed with an unverified streak — no dividend history found in public data."
            continue
        p = by_slug[r["slug"]]
        p["streakYears"] = r["new"]
        p["dividends"] = r["dividends"]
        p["oneLiner"] = f"{p.get('sector', 'Listed company')} paying dividends in {r['new']} consecutive years."
        p["source"]["note"] = (
            f"Streak computed from {r['total']} recorded payments; history begins {r['first_year']}."
        )
        p["review"]["notes"] = (
            f"Streak computed from {r['total']} recorded payments; history begins {r['first_year']}."
        )

    PRODUCTS.write_text(json.dumps(products, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("rewritten")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
