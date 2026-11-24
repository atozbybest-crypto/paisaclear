#!/usr/bin/env python3
"""Fetch US market data: indices, Treasury yields, ETFs, funds and deposit rates.

Every figure written carries the date it was observed. Sources are recorded so
the page can link to them.

    python tools/fetch_us_market.py
"""

from __future__ import annotations

import csv
import time
import io
import json
import ssl
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content" / "us_market.json"
UA = "PaisaClear research contact@paisaclear.co.in"
CTX = ssl.create_default_context()

INDICES = [("^GSPC", "S&P 500"), ("^IXIC", "Nasdaq Composite"), ("^DJI", "Dow Jones Industrial Average")]
ETFS = [
    ("SPY", "SPDR S&P 500 ETF"), ("QQQ", "Invesco QQQ Trust"), ("VOO", "Vanguard S&P 500 ETF"),
    ("IVV", "iShares Core S&P 500 ETF"), ("VTI", "Vanguard Total Stock Market ETF"),
    ("IWM", "iShares Russell 2000 ETF"), ("GLD", "SPDR Gold Shares"), ("TLT", "iShares 20+ Year Treasury Bond ETF"),
    ("BND", "Vanguard Total Bond Market ETF"), ("VEA", "Vanguard FTSE Developed Markets ETF"),
    ("VWO", "Vanguard FTSE Emerging Markets ETF"), ("SCHD", "Schwab US Dividend Equity ETF"),
]
FUNDS = [
    ("VFIAX", "Vanguard 500 Index Fund Admiral"), ("VTSAX", "Vanguard Total Stock Market Index Fund"),
    ("FXAIX", "Fidelity 500 Index Fund"), ("VBTLX", "Vanguard Total Bond Market Index Fund"),
]


def get(url: str, accept: str = "application/json", attempts: int = 3) -> bytes:
    last = None
    for attempt in range(attempts):
        for host in ("query1", "query2"):
            try:
                fixed = url.replace("query1.finance.yahoo.com", f"{host}.finance.yahoo.com")
                request = urllib.request.Request(fixed, headers={"User-Agent": UA, "Accept": accept})
                with urllib.request.urlopen(request, timeout=30, context=CTX) as response:
                    return response.read()
            except Exception as error:
                last = error
        time.sleep(2 * (attempt + 1))
    raise last


def quote(ticker: str) -> dict | None:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=3y&interval=1d"
    try:
        payload = json.loads(get(url))
        result = payload["chart"]["result"][0]
        closes = [c for c in result["indicators"]["quote"][0]["close"] if c is not None]
        stamps = result["timestamp"]
        if not closes:
            return None
        latest = closes[-1]
        as_of = datetime.fromtimestamp(stamps[-1], tz=timezone.utc).date().isoformat()

        def change(days):
            if len(closes) <= days:
                return None
            return round((latest / closes[-1 - days] - 1) * 100, 2)

        year_ago = closes[-252] if len(closes) > 252 else closes[0]
        return {
            "price": round(latest, 2),
            "asOf": as_of,
            "day": change(1),
            "month": change(21),
            "year": round((latest / year_ago - 1) * 100, 2) if year_ago else None,
        }
    except Exception:
        return None


def treasury_yields() -> list[dict]:
    url = ("https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
           "daily-treasury-rates.csv/2026/all?type=daily_treasury_yield_curve"
           "&field_tdr_date_value=2026&page&_format=csv")
    try:
        text = get(url, "text/csv").decode("utf-8", "replace")
        rows = list(csv.DictReader(io.StringIO(text)))
        if not rows:
            return []
        latest = rows[0]
        wanted = [("2 Yr", "2 Yr"), ("5 Yr", "5 Yr"), ("10 Yr", "10 Yr"), ("30 Yr", "30 Yr")]
        out = []
        for label, key in wanted:
            value = latest.get(key) or latest.get(key + " ")
            if value:
                out.append({"label": label, "value": float(value), "asOf": latest.get("Date", "")})
        return out
    except Exception:
        return []


def main() -> int:
    today = date.today().isoformat()
    payload = {
        "fetchedAt": datetime.now(timezone.utc).isoformat(timespec="minutes"),
        "indices": [], "etfs": [], "funds": [], "treasuries": treasury_yields(),
    }

    for ticker, label in INDICES:
        q = quote(ticker)
        if q:
            payload["indices"].append({"ticker": ticker.lstrip("^"), "label": label, **q})

    for ticker, label in ETFS:
        q = quote(ticker)
        if q:
            payload["etfs"].append({"ticker": ticker, "label": label, **q})

    for ticker, label in FUNDS:
        q = quote(ticker)
        if q:
            payload["funds"].append({"ticker": ticker, "label": label, **q})

    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"US market: {len(payload['indices'])} indices, {len(payload['etfs'])} ETFs, "
          f"{len(payload['funds'])} funds, {len(payload['treasuries'])} yields")
    if payload["indices"]:
        top = payload["indices"][0]
        print(f"  {top['label']}: {top['price']} as of {top['asOf']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
