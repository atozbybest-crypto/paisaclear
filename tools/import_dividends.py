#!/usr/bin/env python3
"""Build the Dividend Champions category from public sources.

Per company:
  * dividend history  -> Yahoo Finance chart API (dates + amounts)
  * sector            -> Screener.in company page
  * founded year      -> Wikipedia infobox
  * streak            -> the list supplied by the site owner, labelled as such

    python tools/import_dividends.py --dry-run
    python tools/import_dividends.py
"""

from __future__ import annotations

import argparse
import html
import json
import re
import ssl
import urllib.parse
import urllib.request
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRODUCTS = ROOT / "content" / "products.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
CTX = ssl.create_default_context()
TODAY = "2026-10-25"

COMPANIES = [
    ("NMDC", "NMDC", 25), ("Sudarshan Chemical Industries", "SUDARSCHEM", 25),
    ("GRP", "GRPLTD", 25), ("Shri Jagdamba Polymers", "SHRJAGP", 25),
    ("Industrial & Prudential Investment", "INDPRUD", 25), ("Elcid Investments", "ELCIDIN", 25),
    ("Texmaco Infrastructure & Holdings", "TEXINFRA", 24), ("Bharat Forge", "BHARATFORG", 23),
    ("Dabur India", "DABUR", 23), ("GIC Housing Finance", "GICHSGFIN", 23),
    ("Visaka Industries", "VISAKAIND", 23), ("Empire Industries", "EMPIND", 23),
    ("NTPC", "NTPC", 22), ("Indian Oil Corporation", "IOC", 22),
    ("Bharat Electronics", "BEL", 22), ("Cummins India", "CUMMINSIND", 22),
    ("Asian Paints", "ASIANPAINT", 22), ("Dr. Reddy's Laboratories", "DRREDDY", 22),
    ("Divi's Laboratories", "DIVISLAB", 22), ("Zydus Lifesciences", "ZYDUSLIFE", 22),
    ("Container Corporation of India", "CONCOR", 22), ("Chambal Fertilisers & Chemicals", "CHAMBLFERT", 22),
    ("Engineers India", "ENGINERSIN", 22), ("Gujarat State Fertilizers & Chemicals", "GSFC", 22),
    ("Gujarat Mineral Development Corporation", "GMDCLTD", 22), ("DCM Shriram", "DCMSHRIRAM", 22),
    ("Birlasoft", "BSOFT", 22), ("Ambuja Cements", "AMBUJACEM", 22),
    ("Grasim Industries", "GRASIM", 22), ("UPL", "UPL", 22),
    ("GHCL", "GHCL", 22), ("Polyplex Corporation", "POLYPLEX", 22),
    ("BASF India", "BASF", 22), ("Linde India", "LINDEINDIA", 22),
    ("Nava", "NAVA", 22), ("City Union Bank", "CUB", 22),
    ("Kalpataru Projects International", "KPIL", 22), ("NCC", "NCC", 22),
    ("Subros", "SUBROS", 22), ("Saksoft", "SAKSOFT", 22),
    ("Greenply Industries", "GREENPLY", 22), ("Bannari Amman Sugars", "BANARISUG", 22),
    ("Indian Hume Pipe Company", "INDIANHUME", 22), ("Ramco Industries", "RAMCOIND", 22),
    ("Adani Enterprises", "ADANIENT", 22), ("Aditya Birla Real Estate", "ABREL", 22),
    ("Bombay Burmah Trading Corporation", "BBTC", 22), ("Ruby Mills", "RUBYMILLS", 22),
    ("Everest Industries", "EVERESTIND", 22),
    ("Procter & Gamble Hygiene and Health Care", "PGHH", 22),
]


def get(url: str, timeout: int = 25) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=timeout, context=CTX) as response:
        return response.read().decode("utf-8", "replace")


def dividends(symbol: str):
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}.NS"
           "?range=30y&interval=1mo&events=div")
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
    return rows[:10]


def sector(symbol: str) -> str:
    page = ""
    for attempt in range(3):
        try:
            page = get(f"https://www.screener.in/company/{symbol}/")
            break
        except Exception:
            time.sleep(1.5 * (attempt + 1))
    if not page:
        return ""
    for label in ("Industry", "Sector"):
        match = re.search(r'title="' + label + r'">([^<]{2,60})</a>', page)
        if match:
            return html.unescape(match.group(1)).strip()
    return ""


def founded(name: str) -> str:
    for title in (name.replace(" ", "_"), name.replace(" ", "_") + "_Limited"):
        try:
            page = get(f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title)}")
        except Exception:
            continue
        match = re.search(r"Founded</th>\s*<td[^>]*>(.*?)</td>", page, re.S)
        if match:
            text = re.sub(r"<[^>]+>", "", match.group(1))
            year = re.search(r"(1[89]\d{2}|20\d{2})", text)
            if year:
                return year.group(1)
    return ""


def build(company):
    name, symbol, streak = company
    return {
        "name": name, "symbol": symbol, "streak": streak,
        "dividends": dividends(symbol), "sector": sector(symbol), "founded": founded(name),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    with ThreadPoolExecutor(max_workers=2) as pool:
        rows = list(pool.map(build, COMPANIES))

    complete = [r for r in rows if r["dividends"]]
    print(f"companies: {len(rows)} | with dividend history: {len(complete)}")
    print(f"  with sector: {sum(1 for r in rows if r['sector'])}")
    print(f"  with founded year: {sum(1 for r in rows if r['founded'])}")

    for r in rows[:5]:
        print(f"  {r['symbol']:<10} divs {len(r['dividends']):>2}  sector {r['sector'][:22]:<22} founded {r['founded']}")

    out = ROOT / "content" / "dividend_champions.json"
    if not args.dry_run:
        out.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("written:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
