#!/usr/bin/env python3
"""Fetch US company records from SEC EDGAR: financial facts and recent filings.

Only SEC data is used — company facts from XBRL and the filing index. Every
figure keeps the fiscal year and period end that the filing states.

    python tools/fetch_us_companies.py
"""

from __future__ import annotations

import json
import ssl
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content" / "us_companies.json"
UA = "PaisaClear research contact@paisaclear.co.in"
CTX = ssl.create_default_context()

TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "JPM", "V", "JNJ",
    "WMT", "PG", "XOM", "UNH", "HD", "MA", "BAC", "KO", "PEP", "COST",
    "DIS", "CSCO", "INTC", "AMD", "NFLX", "ADBE", "CRM", "ORCL", "PFE", "TMO",
]

REVENUE_KEYS = ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet"]
INCOME_KEYS = ["NetIncomeLoss", "ProfitLoss"]
EPS_KEYS = ["EarningsPerShareDiluted", "EarningsPerShareBasic"]


def get(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=40, context=CTX) as response:
        return response.read()


def annual_series(facts: dict, keys: list[str]) -> list[dict]:
    """Latest annual values for the first key that exists."""
    gaap = (facts.get("facts") or facts).get("us-gaap", {})
    for key in keys:
        if key not in gaap:
            continue
        units = gaap[key].get("units", {})
        rows = units.get("USD") or units.get("USD/shares") or []
        annual = [r for r in rows if r.get("form") == "10-K" and r.get("fp") == "FY" and r.get("fy")]
        if not annual:
            continue
        by_year = {}
        for row in annual:
            fy = row["fy"]
            if fy not in by_year or row["end"] > by_year[fy]["end"]:
                by_year[fy] = row
        series = sorted(by_year.values(), key=lambda r: r["end"], reverse=True)[:4]
        return [{"fy": r["fy"], "end": r["end"], "value": r["val"], "key": key} for r in series]
    return []


def build(ticker: str, cik_map: dict) -> dict | None:
    cik = cik_map.get(ticker)
    if not cik:
        return None
    padded = str(cik).zfill(10)
    try:
        facts = json.loads(get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{padded}.json"))
        subs = json.loads(get(f"https://data.sec.gov/submissions/CIK{padded}.json"))
    except Exception:
        return None

    recent = subs.get("filings", {}).get("recent", {})
    filings = []
    for i in range(min(len(recent.get("form", [])), 40)):
        if len(filings) >= 6:
            break
        form = recent["form"][i]
        if form not in ("10-K", "10-Q", "8-K"):
            continue
        acc = recent["accessionNumber"][i].replace("-", "")
        doc = recent["primaryDocument"][i]
        filings.append({
            "form": form,
            "date": recent["filingDate"][i],
            "url": f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/{doc}",
        })

    return {
        "ticker": ticker,
        "name": subs.get("name", ticker),
        "cik": cik,
        "sic": subs.get("sicDescription", ""),
        "fiscalYearEnd": subs.get("fiscalYearEnd", ""),
        "revenue": annual_series(facts, REVENUE_KEYS),
        "income": annual_series(facts, INCOME_KEYS),
        "eps": annual_series(facts, EPS_KEYS),
        "filings": filings,
        "fetchedAt": subs.get("filings", {}).get("recent", {}).get("filingDate", [""])[0],
    }


def main() -> int:
    tickers = json.loads(get("https://www.sec.gov/files/company_tickers.json"))
    cik_map = {row["ticker"].upper(): row["cik_str"] for row in tickers.values()}
    print(f"SEC tickers loaded: {len(cik_map)}")

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = [r for r in pool.map(lambda t: build(t, cik_map), TICKERS) if r]

    OUT.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"companies: {len(results)}")
    for r in results[:3]:
        rev = r["revenue"][0]["value"] if r["revenue"] else None
        print(f"  {r['ticker']:<6} {r['name'][:34]:<34} filings {len(r['filings'])} revenue {rev}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
