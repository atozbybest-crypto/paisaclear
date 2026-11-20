#!/usr/bin/env python3
"""Fetch US mutual funds and ETFs — real NAV/price history from Yahoo Finance.

Categories cover what a retail investor can actually buy: index equity,
international, bonds, money market, dividend, sector, target date and balanced.
Collective investment trusts, stable-value funds and variable annuities are not
publicly priced instruments, so they are deliberately absent.

    python tools/fetch_us_funds.py
"""

from __future__ import annotations

import json
import ssl
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content" / "us_funds.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0"
CTX = ssl.create_default_context()

# (ticker, name, category, kind)
FUNDS = [
    # --- index equity
    ("SPY", "SPDR S&P 500 ETF Trust", "Index equity", "ETF"),
    ("VOO", "Vanguard S&P 500 ETF", "Index equity", "ETF"),
    ("IVV", "iShares Core S&P 500 ETF", "Index equity", "ETF"),
    ("VTI", "Vanguard Total Stock Market ETF", "Index equity", "ETF"),
    ("ITOT", "iShares Core S&P Total US Stock Market ETF", "Index equity", "ETF"),
    ("QQQ", "Invesco QQQ Trust", "Index equity", "ETF"),
    ("QQQM", "Invesco NASDAQ 100 ETF", "Index equity", "ETF"),
    ("IWM", "iShares Russell 2000 ETF", "Index equity", "ETF"),
    ("VV", "Vanguard Large-Cap ETF", "Index equity", "ETF"),
    ("SCHX", "Schwab US Large-Cap ETF", "Index equity", "ETF"),
    ("VXF", "Vanguard Extended Market ETF", "Index equity", "ETF"),
    ("FXAIX", "Fidelity 500 Index Fund", "Index equity", "Mutual fund"),
    ("VFIAX", "Vanguard 500 Index Fund Admiral", "Index equity", "Mutual fund"),
    ("VTSAX", "Vanguard Total Stock Market Index Fund", "Index equity", "Mutual fund"),
    ("FSKAX", "Fidelity Total Market Index Fund", "Index equity", "Mutual fund"),
    # --- international
    ("VEA", "Vanguard FTSE Developed Markets ETF", "International", "ETF"),
    ("VWO", "Vanguard FTSE Emerging Markets ETF", "International", "ETF"),
    ("VXUS", "Vanguard Total International Stock ETF", "International", "ETF"),
    ("IEFA", "iShares Core MSCI EAFE ETF", "International", "ETF"),
    ("EEM", "iShares MSCI Emerging Markets ETF", "International", "ETF"),
    ("VGTSX", "Vanguard Total International Stock Index Fund", "International", "Mutual fund"),
    ("VTIAX", "Vanguard Total International Stock Index Admiral", "International", "Mutual fund"),
    # --- bonds
    ("BND", "Vanguard Total Bond Market ETF", "Bonds", "ETF"),
    ("AGG", "iShares Core US Aggregate Bond ETF", "Bonds", "ETF"),
    ("TLT", "iShares 20+ Year Treasury Bond ETF", "Bonds", "ETF"),
    ("IEF", "iShares 7-10 Year Treasury Bond ETF", "Bonds", "ETF"),
    ("SHY", "iShares 1-3 Year Treasury Bond ETF", "Bonds", "ETF"),
    ("LQD", "iShares iBoxx Investment Grade Corporate Bond ETF", "Bonds", "ETF"),
    ("HYG", "iShares iBoxx High Yield Corporate Bond ETF", "Bonds", "ETF"),
    ("BNDX", "Vanguard Total International Bond ETF", "Bonds", "ETF"),
    ("VBTLX", "Vanguard Total Bond Market Index Fund", "Bonds", "Mutual fund"),
    ("FXNAX", "Fidelity US Bond Index Fund", "Bonds", "Mutual fund"),
    # --- money market
    ("VMFXX", "Vanguard Federal Money Market Fund", "Money market", "Mutual fund"),
    ("VUSXX", "Vanguard Treasury Money Market Fund", "Money market", "Mutual fund"),
    # --- dividend
    ("SCHD", "Schwab US Dividend Equity ETF", "Dividend", "ETF"),
    ("VYM", "Vanguard High Dividend Yield ETF", "Dividend", "ETF"),
    ("VIG", "Vanguard Dividend Appreciation ETF", "Dividend", "ETF"),
    ("DVY", "iShares Select Dividend ETF", "Dividend", "ETF"),
    ("DGRO", "iShares Core Dividend Growth ETF", "Dividend", "ETF"),
    # --- sectors
    ("XLK", "Technology Select Sector SPDR Fund", "Sector", "ETF"),
    ("XLV", "Health Care Select Sector SPDR Fund", "Sector", "ETF"),
    ("XLF", "Financial Select Sector SPDR Fund", "Sector", "ETF"),
    ("XLE", "Energy Select Sector SPDR Fund", "Sector", "ETF"),
    ("XLP", "Consumer Staples Select Sector SPDR Fund", "Sector", "ETF"),
    ("XLY", "Consumer Discretionary Select Sector SPDR Fund", "Sector", "ETF"),
    ("XLI", "Industrial Select Sector SPDR Fund", "Sector", "ETF"),
    ("XLU", "Utilities Select Sector SPDR Fund", "Sector", "ETF"),
    ("XLB", "Materials Select Sector SPDR Fund", "Sector", "ETF"),
    ("XLRE", "Real Estate Select Sector SPDR Fund", "Sector", "ETF"),
    ("XLC", "Communication Services Select Sector SPDR Fund", "Sector", "ETF"),
    # --- real estate and commodities
    ("VNQ", "Vanguard Real Estate ETF", "Real estate", "ETF"),
    ("SCHH", "Schwab US REIT ETF", "Real estate", "ETF"),
    ("GLD", "SPDR Gold Shares", "Commodities", "ETF"),
    ("IAU", "iShares Gold Trust", "Commodities", "ETF"),
    ("SLV", "iShares Silver Trust", "Commodities", "ETF"),
    # --- target date
    ("VFFVX", "Vanguard Target Retirement 2055 Fund", "Target date", "Mutual fund"),
    ("VTTSX", "Vanguard Target Retirement 2060 Fund", "Target date", "Mutual fund"),
    ("VFIFX", "Vanguard Target Retirement 2050 Fund", "Target date", "Mutual fund"),
    # --- balanced
    ("VBIAX", "Vanguard Balanced Index Fund", "Balanced", "Mutual fund"),
    ("AOR", "iShares Core Growth Allocation ETF", "Balanced", "ETF"),
    ("AOA", "iShares Core Aggressive Allocation ETF", "Balanced", "ETF"),
    ("AOM", "iShares Core Moderate Allocation ETF", "Balanced", "ETF"),
]


def get(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=30, context=CTX) as response:
        return response.read()


def fetch(ticker: str) -> dict | None:
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
           "?range=6y&interval=1mo&events=div")
    try:
        payload = json.loads(get(url))
        result = payload["chart"]["result"][0]
        closes = result["indicators"]["quote"][0]["close"]
        stamps = result.get("timestamp", [])
        pairs = [(s, c) for s, c in zip(stamps, closes) if c is not None]
        if len(pairs) < 13:
            return None
        pairs.sort()
        latest_stamp, latest = pairs[-1]

        def cagr(years):
            need = years * 12
            if len(pairs) <= need:
                return None
            start = pairs[-1 - need][1]
            if start <= 0 or latest <= 0:
                return None
            return round(((latest / start) ** (1 / years) - 1) * 100, 2)

        divs = result.get("events", {}).get("dividends", {})
        cutoff = latest_stamp - 365 * 86400
        ttm = sum(d["amount"] for d in divs.values() if d["date"] >= cutoff)
        yield_pct = round((ttm / latest) * 100, 2) if latest else None

        return {
            "price": round(latest, 2),
            "asOf": datetime.fromtimestamp(latest_stamp, tz=timezone.utc).date().isoformat(),
            "c1": cagr(1), "c3": cagr(3), "c5": cagr(5),
            "yield": yield_pct,
            "points": len(pairs),
        }
    except Exception:
        return None


def main() -> int:
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(lambda row: (row, fetch(row[0])), FUNDS))

    records = []
    failed = []
    for (ticker, name, category, kind), data in results:
        if not data:
            failed.append(ticker)
            continue
        records.append({"ticker": ticker, "name": name, "category": category,
                        "kind": kind, **data})

    categories = sorted({r["category"] for r in records})
    OUT.write_text(json.dumps({
        "fetchedAt": datetime.now(timezone.utc).isoformat(timespec="minutes"),
        "records": records,
        "categories": categories,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"US funds: {len(records)} records in {len(categories)} categories")
    if failed:
        print("  no data:", ", ".join(failed))
    from collections import Counter
    print("  per category:", dict(Counter(r["category"] for r in records)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
