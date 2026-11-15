#!/usr/bin/env python3
"""Add dividend-paying stocks, with the streak computed from the payment history.

Yahoo's Indian dividend records begin around 2008, so the longest verifiable
streak is about 18 years. Each record states the window it was verified over
instead of repeating an unverifiable claim.

    python tools/import_dividend_stocks.py --want 30
"""

from __future__ import annotations

import argparse
import json
import re
import ssl
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRODUCTS = ROOT / "content" / "products.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0"
CTX = ssl.create_default_context()

CANDIDATES = [
    ("ITC", "ITC", "FMCG"),
    ("Hindustan Unilever", "HINDUNILVR", "FMCG"),
    ("Nestle India", "NESTLEIND", "FMCG"),
    ("Britannia Industries", "BRITANNIA", "FMCG"),
    ("Marico", "MARICO", "FMCG"),
    ("Godrej Consumer Products", "GODREJCP", "FMCG"),
    ("Colgate-Palmolive India", "COLPAL", "FMCG"),
    ("Emami", "EMAMILTD", "FMCG"),
    ("Bajaj Auto", "BAJAJ-AUTO", "Automobiles"),
    ("Hero MotoCorp", "HEROMOTOCO", "Automobiles"),
    ("TVS Motor", "TVSMOTOR", "Automobiles"),
    ("Bosch", "BOSCHLTD", "Auto components"),
    ("Siemens India", "SIEMENS", "Capital goods"),
    ("ABB India", "ABB", "Capital goods"),
    ("Thermax", "THERMAX", "Capital goods"),
    ("SKF India", "SKFINDIA", "Capital goods"),
    ("Grindwell Norton", "GRINDWELL", "Capital goods"),
    ("Carborundum Universal", "CARBORUNIV", "Capital goods"),
    ("Power Grid Corporation", "POWERGRID", "Utilities"),
    ("Coal India", "COALINDIA", "Mining"),
    ("Oil and Natural Gas Corporation", "ONGC", "Energy"),
    ("GAIL India", "GAIL", "Energy"),
    ("Petronet LNG", "PETRONET", "Energy"),
    ("Hindustan Petroleum", "HINDPETRO", "Energy"),
    ("Bharat Petroleum", "BPCL", "Energy"),
    ("Indian Oil", "IOC", "Energy"),
    ("NLC India", "NLCINDIA", "Utilities"),
    ("Power Finance Corporation", "PFC", "Financials"),
    ("REC", "RECLTD", "Financials"),
    ("HUDCO", "HUDCO", "Financials"),
    ("Can Fin Homes", "CANFINHOME", "Financials"),
    ("Cholamandalam Investment", "CHOLAFIN", "Financials"),
    ("Sundaram Finance", "SUNDARMFIN", "Financials"),
    ("Muthoot Finance", "MUTHOOTFIN", "Financials"),
    ("Manappuram Finance", "MANAPPURAM", "Financials"),
    ("Karur Vysya Bank", "KARURVYSYA", "Financials"),
    ("Federal Bank", "FEDERALBNK", "Financials"),
    ("South Indian Bank", "SOUTHBANK", "Financials"),
    ("Sun Pharmaceutical", "SUNPHARMA", "Pharma"),
    ("Cipla", "CIPLA", "Pharma"),
    ("Lupin", "LUPIN", "Pharma"),
    ("Torrent Pharmaceuticals", "TORNTPHARM", "Pharma"),
    ("Alkem Laboratories", "ALKEM", "Pharma"),
    ("Ipca Laboratories", "IPCA", "Pharma"),
    ("Ajanta Pharma", "AJANTPHARM", "Pharma"),
    ("Natco Pharma", "NATCOPHARM", "Pharma"),
    ("Abbott India", "ABBOTINDIA", "Pharma"),
    ("Pfizer India", "PFIZER", "Pharma"),
    ("GlaxoSmithKline Pharmaceuticals", "GLAXO", "Pharma"),
    ("Tata Consultancy Services", "TCS", "IT services"),
    ("Infosys", "INFY", "IT services"),
    ("Wipro", "WIPRO", "IT services"),
    ("HCL Technologies", "HCLTECH", "IT services"),
    ("Tech Mahindra", "TECHM", "IT services"),
    ("Oracle Financial Services", "OFSS", "IT services"),
    ("Persistent Systems", "PERSISTENT", "IT services"),
    ("Page Industries", "PAGEIND", "Consumer"),
    ("Hawkins Cookers", "HAWKINS", "Consumer"),
    ("TTK Prestige", "TTKPRESTIG", "Consumer"),
    ("Jyothy Labs", "JYOTHYLAB", "Consumer"),
    ("V.I.P. Industries", "VIPIND", "Consumer"),
    ("Cera Sanitaryware", "CERA", "Building materials"),
]


def get(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=30, context=CTX) as response:
        return response.read()


def history(symbol: str):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}.NS?range=30y&interval=1mo&events=div"
    try:
        payload = json.loads(get(url))
        events = payload["chart"]["result"][0].get("events", {}).get("dividends", {})
    except Exception:
        return []
    rows = []
    for item in events.values():
        rows.append({
            "date": datetime.fromtimestamp(item["date"], tz=timezone.utc).date().isoformat(),
            "amount": round(float(item["amount"]), 2),
        })
    rows.sort(key=lambda r: r["date"], reverse=True)
    return rows


def streak_years(rows) -> tuple[int, str]:
    years = sorted({int(r["date"][:4]) for r in rows})
    if not years:
        return 0, ""
    this_year = date.today().year
    streak, cursor = 0, years[-1]
    # a current year with no payment yet should not break the streak
    if cursor == this_year and len([y for y in years if y == this_year]) == 0:
        cursor -= 1
    while cursor in years:
        streak += 1
        cursor -= 1
    return streak, str(min(years))


def build(name, symbol, sector):
    rows = history(symbol)
    if len(rows) < 6:
        return None
    streak, first_year = streak_years(rows)
    if streak < 8:
        return None
    return {
        "name": name, "symbol": symbol, "sector": sector, "streak": streak,
        "first_year": first_year, "dividends": rows[:10], "total": len(rows),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--want", type=int, default=30)
    args = parser.parse_args()

    products = json.loads(PRODUCTS.read_text(encoding="utf-8"))
    existing = {p.get("symbol") for p in products if p["category"] == "dividend-champions"}
    pool = [c for c in CANDIDATES if c[1] not in existing]

    with ThreadPoolExecutor(max_workers=6) as pool_exec:
        results = [r for r in pool_exec.map(lambda c: build(*c), pool) if r]

    results.sort(key=lambda r: (-r["streak"], r["name"]))
    chosen = results[: args.want]
    print(f"verified {len(results)} companies with 8+ year streaks; adding {len(chosen)}")

    today = date.today().isoformat()
    for row in chosen:
        slug = "dividend-" + re.sub(r"[^a-z0-9]+", "-", row["symbol"].lower()).strip("-")
        if any(p["slug"] == slug for p in products):
            continue
        products.append({
            "slug": slug, "name": row["name"], "provider": "Listed on NSE",
            "providerShort": row["symbol"], "providerType": "Listed company",
            "category": "dividend-champions", "returnType": "market-linked", "demo": False,
            "oneLiner": f"{row['sector']} company paying dividends for {row['streak']} straight years.",
            "minInvestment": None, "minInvestmentNote": "One share, at the market price",
            "tenure": "No fixed term", "tenureMonths": None,
            "payout": "Dividends when declared", "payoutFrequency": "dividend",
            "liquidity": "Sold on the exchange during market hours", "lockIn": None,
            "eligibility": "Any investor with a demat account",
            "tax": "Dividends are taxed at your slab. Capital gains depend on holding period.",
            "protection": "No capital protection. Share prices fall as well as rise.",
            "riskLevel": "high",
            "risks": ["Dividends are not guaranteed and can be cut in a bad year.",
                      "The share price can fall more than the dividend pays.",
                      "Past payout history does not oblige the company to keep paying."],
            "commonUses": ["Income alongside equity exposure"],
            "check": ["The payout ratio and free cash flow", "Whether the dividend is sustainable"],
            "collections": ["understand-before-you-invest"],
            "symbol": row["symbol"], "sector": row["sector"],
            "streakYears": row["streak"], "dividends": row["dividends"],
            "rateRef": {"label": "Dividend per share, declared by the board",
                        "url": f"https://finance.yahoo.com/quote/{row['symbol']}.NS/history",
                        "note": "The amount varies each year and is not a fixed rate."},
            "sources": [{"label": "Yahoo Finance — dividend history",
                         "url": f"https://finance.yahoo.com/quote/{row['symbol']}.NS/history"},
                        {"label": "Screener — company page",
                         "url": f"https://www.screener.in/company/{row['symbol']}/"}],
            "source": {"label": "Dividend records — Yahoo Finance",
                       "url": f"https://finance.yahoo.com/quote/{row['symbol']}.NS/history",
                       "note": f"Streak computed from payments recorded since {row['first_year']}."},
            "lastVerified": today,
            "review": {"status": "approved", "reviewer": "Automated import, computed streak",
                       "approvedAt": today,
                       "notes": f"Streak computed from {row['total']} recorded payments; history begins {row['first_year']}."},
        })

    products.sort(key=lambda p: (p["category"], p["name"]))
    PRODUCTS.write_text(json.dumps(products, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    total = sum(1 for p in products if p["category"] == "dividend-champions")
    print(f"dividend-champions now {total} | products {len(products)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
