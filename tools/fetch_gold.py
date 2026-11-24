#!/usr/bin/env python3
"""Fetch gold prices and history, in dollars and in rupees.

Three independent figures, each with its own date:
  * international gold futures, USD per troy ounce
  * USD/INR
  * the NSE gold ETF (GOLDBEES), rupees per unit

The rupee-per-10-gram figure is computed from the first two. It is a reference
conversion, not the landed Indian price — import duty and dealer premium are not
in it, and the page says so.

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
        closes = result["indicators"]["quote"][0]["close"]
        points = [
            {"d": datetime.fromtimestamp(s, tz=timezone.utc).date().isoformat(), "v": round(c, 2)}
            for s, c in zip(stamps, closes) if c is not None
        ]
        if not points:
            return None
        return {"points": points, "last": points[-1]}
    except Exception:
        return None


def pct_change(points: list[dict], days_back: int) -> float | None:
    if len(points) <= days_back:
        return None
    old = points[-1 - days_back]["v"]
    if not old:
        return None
    return round((points[-1]["v"] / old - 1) * 100, 2)


def per_10g(usd_oz: float, usdinr: float) -> float:
    return round(usd_oz * usdinr / OUNCE_IN_GRAMS * 10, 0)


def main() -> int:
    daily = chart("GC=F", "6y", "1d")
    monthly = chart("GC=F", "6y", "1mo")
    fx_daily = chart("USDINR=X", "6y", "1d")
    fx_monthly = chart("USDINR=X", "6y", "1mo")
    etf_monthly = chart("GOLDBEES.NS", "6y", "1mo")

    if not (daily and fx_daily):
        print("gold fetch failed")
        return 1

    usd_oz = daily["last"]["v"]
    usdinr = fx_daily["last"]["v"]

    # monthly history in rupees per 10 g, built by pairing the two series by date
    fx_by_month = {p["d"][:7]: p["v"] for p in (fx_monthly or {}).get("points", [])}
    history = []
    for point in (monthly or {}).get("points", []):
        key = point["d"][:7]
        rate = fx_by_month.get(key)
        if rate:
            history.append({"m": key, "usd": point["v"], "inr": round(rate, 2),
                            "per10g": per_10g(point["v"], rate)})

    payload = {
        "fetchedAt": datetime.now(timezone.utc).isoformat(timespec="minutes"),
        "usdPerOunce": {"value": usd_oz, "asOf": daily["last"]["d"],
                        "day": pct_change(daily["points"], 1),
                        "month": pct_change(daily["points"], 21),
                        "year": pct_change(daily["points"], 252)},
        "usdinr": {"value": usdinr, "asOf": fx_daily["last"]["d"]},
        "per10g": {"value": per_10g(usd_oz, usdinr), "asOf": daily["last"]["d"]},
        "etf": ({"value": etf_monthly["points"][-1]["v"], "asOf": etf_monthly["points"][-1]["d"]}
                if etf_monthly else None),
        "history": history[-72:],
        "etfHistory": ([{"m": p["d"][:7], "v": p["v"]} for p in etf_monthly["points"]][-72:]
                       if etf_monthly else []),
    }

    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"gold: ${usd_oz:,.2f}/oz · ₹{usdinr:.2f}/$ · ₹{payload['per10g']['value']:,.0f} per 10 g "
          f"({len(history)} months of history)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
