#!/usr/bin/env python3
"""Import exchange-traded funds with real NAV history.

Same approach as import_funds.py, but for the ETF universe: no "direct plan"
suffix, risk band derived from what the ETF tracks.

    python tools/import_etfs.py --count 25 --dry-run
    python tools/import_etfs.py --count 25
"""

from __future__ import annotations

import argparse
import json
import re
import ssl
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRODUCTS = ROOT / "content" / "products.json"
RATES = ROOT / "content" / "rates.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
TODAY = "2026-10-19"

# (band, rank, keywords)
BUCKETS = [
    ("low", 1, [r"liquid", r"overnight", r"money market"]),
    ("low-to-moderate", 2, [r"gilt", r"bond", r"psu", r"debt", r"credit"]),
    ("moderate", 3, [r"gold", r"silver"]),
    ("high", 4, [r"nifty 50", r"nifty50", r"sensex", r"index", r"large cap", r"quality", r"low volatility"]),
    ("very-high", 5, [r"bank", r"it ", r"technology", r"pharma", r"auto", r"consumption", r"midcap", r"smallcap", r"next 50"]),
]

RISK_LEVEL = {"low": "low", "low-to-moderate": "low", "moderate": "moderate", "high": "high", "very-high": "high"}


def http_json(url: str):
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=30, context=ssl.create_default_context()) as response:
        return json.loads(response.read())


def cagr(history, years):
    latest_date, latest_nav = history[-1]
    target = latest_date - timedelta(days=int(365.25 * years))
    older = [row for row in history if row[0] <= target]
    if not older:
        return None
    base_date, base_nav = older[-1]
    span = (latest_date - base_date).days / 365.25
    if span <= 0 or base_nav <= 0:
        return None
    return round(((latest_nav / base_nav) ** (1 / span) - 1) * 100, 2)


def classify(name: str):
    low = name.lower()
    for band, rank, patterns in BUCKETS:
        if any(re.search(p, low) for p in patterns):
            return band, rank
    return "high", 4


def slugify(text: str, code: int) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return f"{re.sub(r'-+', '-', text)[:56].strip('-')}-{code}"


def build(scheme: dict, detail: dict):
    code = scheme["schemeCode"]
    name = detail["meta"]["scheme_name"].strip()
    fund_house = detail["meta"]["fund_house"]

    history = []
    for row in detail["data"]:
        try:
            history.append((datetime.strptime(row["date"], "%d-%m-%Y"), float(row["nav"])))
        except (KeyError, ValueError):
            continue
    history.sort()
    if len(history) < 400:
        return None

    latest_date, latest_nav = history[-1]
    returns = {
        "oneYear": cagr(history, 1),
        "threeYear": cagr(history, 3),
        "fiveYear": cagr(history, 5),
        "asOf": latest_date.strftime("%Y-%m-%d"),
        "basis": "CAGR computed from AMFI NAV",
    }
    if returns["threeYear"] is None:
        return None

    band, rank = classify(name)
    rate_key = f"nav-{code}"

    product = {
        "slug": slugify(name, code),
        "name": name,
        "provider": fund_house,
        "providerShort": fund_house.replace(" Mutual Fund", ""),
        "providerType": "Asset manager",
        "category": "etfs",
        "returnType": "market-linked",
        "rateKey": rate_key,
        "fundCategory": "ETF",
        "riskBand": band,
        "riskRank": rank,
        "returns": returns,
        "demo": False,
        "oneLiner": "Exchange-traded fund. Figures shown are computed from its own NAV history; the traded price can differ from NAV.",
        "minInvestment": 100,
        "minInvestmentNote": "one unit at the traded price; brokerage applies",
        "tenure": "No lock-in",
        "tenureMonths": None,
        "payout": "Growth — no payout",
        "payoutFrequency": "growth",
        "liquidity": "Traded during market hours. Liquidity depends on how many units change hands.",
        "lockIn": None,
        "eligibility": "Resident individuals with a demat and trading account, subject to KYC.",
        "tax": "Gains are taxed by holding period under equity, debt or commodity rules depending on what the fund holds.",
        "protection": "No capital protection. The price moves with the underlying and can diverge from NAV.",
        "riskLevel": RISK_LEVEL[band],
        "risks": [
            "The traded price can sit above or below the value of the holdings.",
            "Thin trading widens the spread you pay to get in or out.",
            "Tracking difference makes the return drift from the index or asset it follows.",
        ],
        "commonUses": [
            "A single trade for exposure to an index, commodity or sector",
            "A low-cost building block in a portfolio"
        ],
        "check": [
            "The expense ratio and tracking difference",
            "Average daily traded volume and the bid-ask spread"
        ],
        "collections": ["understand-before-you-invest"],
        "sources": [
            {"label": "AMFI — NAV data", "url": "https://www.amfiindia.com/spages/NAVAll.txt"},
            {"label": "SEBI — ETFs", "url": "https://www.sebi.gov.in"},
        ],
        "source": {
            "label": "AMFI — scheme and NAV data",
            "url": "https://www.amfiindia.com/mutual-fund",
            "note": f'Search "{name}" on AMFI for its official NAV history; check the exchange page for the traded price.',
        },
        "lastVerified": TODAY,
        "review": {
            "status": "approved",
            "reviewer": "Automated NAV import, 19 Oct 2026",
            "approvedAt": TODAY,
            "notes": "NAV from AMFI data; returns computed by PaisaClear; risk band assigned from what the ETF tracks.",
        },
    }

    rate = {
        "value": f"₹{latest_nav:,.2f}",
        "label": "NAV per unit",
        "asOf": latest_date.strftime("%Y-%m-%d"),
        "cadence": "Published daily by AMFI",
        "sourceUrl": "https://www.amfiindia.com/mutual-fund",
        "sourceLabel": "AMFI — mutual fund NAV data",
    }
    return product, rate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=25)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    listing = http_json("https://api.mfapi.in/mf")
    candidates = []
    for scheme in listing:
        name = scheme["schemeName"]
        low = name.lower()
        if "etf" not in low or "fof" in low:
            continue
        if any(bad in low for bad in ("idcw", "dividend", "bonus")):
            continue
        candidates.append(scheme)
    print(f"ETF schemes found: {len(candidates)}")

    products = json.loads(PRODUCTS.read_text(encoding="utf-8"))
    rates = json.loads(RATES.read_text(encoding="utf-8"))
    existing_slugs = {p["slug"] for p in products}
    existing_rates = set(rates["values"])

    def fetch(scheme):
        try:
            return scheme, http_json(f"https://api.mfapi.in/mf/{scheme['schemeCode']}")
        except Exception:
            return scheme, None

    built, seen = [], set()
    with ThreadPoolExecutor(max_workers=8) as pool:
        for scheme, detail in pool.map(fetch, candidates[: args.count * 4]):
            if detail is None or len(built) >= args.count:
                continue
            result = build(scheme, detail)
            if not result:
                continue
            product, rate = result
            if (product["slug"] in existing_slugs or product["slug"] in seen
                    or product["rateKey"] in existing_rates):
                continue
            seen.add(product["slug"])
            built.append((product, rate))

    print(f"built {len(built)} ETF records")
    if args.dry_run:
        for product, _ in built[:12]:
            r = product["returns"]
            print(f"  {product['riskBand']:<16} 3y={r['threeYear']:>6} {product['name'][:52]}")
        return 0

    for product, rate in built:
        products.append(product)
        rates["values"][product["rateKey"]] = rate
    rates["generatedAt"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    PRODUCTS.write_text(json.dumps(products, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    RATES.write_text(json.dumps(rates, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"products now: {len(products)} | rates now: {len(rates['values'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
