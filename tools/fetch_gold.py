#!/usr/bin/env python3
"""Fetch gold prices with monthly OHLC, in dollars and in rupees.

Yahoo's monthly series carries open/high/low/close, so the page can draw
candlesticks instead of a line. The rupee candle is the dollar candle converted
at that month's USD/INR rate.

    python tools/fetch_gold.py
"""

from __future__ import annotations

import json
import ssl
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content" / "gold.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0"
CTX = ssl.create_default_context()
OUNCE_IN_GRAMS = 31.1034768


def chart(symbol: str, period: str, interval: str) -> dict | None:
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
           f"?range={period}&interval={interval}")
    try:
        request = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(request, timeout=30, context=CTX) as response:
            payload = json.loads(response.read())
        result = payload["chart"]["result"][0]
        stamps = result.get("timestamp", [])
        quote = result["indicators"]["quote"][0]

        points = []
        for i, stamp in enumerate(stamps):
            row = {k: quote.get(k, [None] * len(stamps))[i] for k in ("open", "high", "low", "close")}
            if row["close"] is None or row["open"] is None:
                continue
            points.append({
                "d": datetime.fromtimestamp(stamp, tz=timezone.utc).date().isoformat(),
                "o": round(row["open"], 2),
                "h": round(row["high"] or row["close"], 2),
                "l": round(row["low"] or row["close"], 2),
                "c": round(row["close"], 2),
            })
        return {"points": points} if points else None
    except Exception:
        return None


def per_10g(usd_oz: float, usdinr: float) -> float:
    return round(usd_oz * usdinr / OUNCE_IN_GRAMS * 10, 0)


def pct_change(points: list[dict], back: int) -> float | None:
    if len(points) <= back:
        return None
    old = points[-1 - back]["c"]
    return round((points[-1]["c"] / old - 1) * 100, 2) if old else None


def main() -> int:
    gold_daily = chart("GC=F", "3y", "1d")
    gold_monthly = chart("GC=F", "7y", "1mo")
    fx_daily = chart("USDINR=X", "3y", "1d")
    fx_monthly = chart("USDINR=X", "7y", "1mo")

    if not (gold_daily and gold_monthly and fx_daily and fx_monthly):
        print("gold fetch incomplete")
        return 1

    # month -> rupee rate, so every gold month can be converted even if the two
    # series do not line up exactly on the same day
    fx_by_month = {p["d"][:7]: p["c"] for p in fx_monthly["points"]}

    months = []
    for point in gold_monthly["points"]:
        key = point["d"][:7]
        rate = fx_by_month.get(key)
        if rate is None:
            # fall back to the most recent earlier month
            earlier = [k for k in fx_by_month if k <= key]
            if not earlier:
                continue
            rate = fx_by_month[max(earlier)]
        months.append({
            "m": key,
            "usd": {"o": point["o"], "h": point["h"], "l": point["l"], "c": point["c"]},
            "fx": round(rate, 2),
            "inr": {
                "o": per_10g(point["o"], rate), "h": per_10g(point["h"], rate),
                "l": per_10g(point["l"], rate), "c": per_10g(point["c"], rate),
            },
        })

    months.sort(key=lambda r: r["m"])

    usd_now = gold_daily["points"][-1]
    fx_now = fx_daily["points"][-1]

    payload = {
        "fetchedAt": datetime.now(timezone.utc).isoformat(timespec="minutes"),
        "usdPerOunce": {"value": usd_now["c"], "asOf": usd_now["d"],
                        "month": pct_change(gold_daily["points"], 21),
                        "year": pct_change(gold_daily["points"], 252)},
        "usdinr": {"value": fx_now["c"], "asOf": fx_now["d"]},
        "per10g": {"value": per_10g(usd_now["c"], fx_now["c"]), "asOf": usd_now["d"]},
        "months": months[-84:],
    }

    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    last = months[-1]
    print(f"gold: ₹{last['inr']['c']:,.0f}/10g · ${last['usd']['c']:,.0f}/oz · months: {len(months)}")
    print(f"  latest month {last['m']}: open ₹{last['inr']['o']:,.0f} high ₹{last['inr']['h']:,.0f} "
          f"low ₹{last['inr']['l']:,.0f} close ₹{last['inr']['c']:,.0f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
