#!/usr/bin/env python3
"""Import a diversified set of direct-plan mutual funds with real NAV history.

Pulls the scheme list and daily NAV series from the AMFI mirror at api.mfapi.in,
computes 1y / 3y / 5y CAGR from NAV, assigns a risk band from the scheme
category, and writes product records plus NAV entries into content/.

Run once. Re-running skips schemes already present (matched by scheme code).

    python tools/import_funds.py --count 100 --dry-run
    python tools/import_funds.py --count 100
"""

from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRODUCTS = ROOT / "content" / "products.json"
RATES = ROOT / "content" / "rates.json"

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
TODAY = "2026-10-19"

# category: (label, risk band, risk level, slot count, keywords)
CATEGORIES = [
    ("Liquid", "low", "low", 8, [r"liquid fund"]),
    ("Ultra Short Duration", "low-to-moderate", "low", 6, [r"ultra short"]),
    ("Corporate Bond", "low-to-moderate", "low", 6, [r"corporate bond"]),
    ("Banking & PSU", "low-to-moderate", "low", 6, [r"banking (and|&) psu"]),
    ("Short Duration", "low-to-moderate", "low", 6, [r"short duration"]),
    ("Gilt", "moderate", "moderate", 6, [r"gilt"]),
    ("Dynamic Bond", "moderate", "moderate", 5, [r"dynamic bond"]),
    ("Balanced Advantage", "moderate", "moderate", 8, [r"balanced advantage"]),
    ("Aggressive Hybrid", "moderately-high", "moderate", 6, [r"aggressive hybrid"]),
    ("Index / Nifty 50", "high", "high", 10, [r"nifty 50 index", r"nifty50 index", r"index fund"]),
    ("Large Cap", "high", "high", 10, [r"large cap"]),
    ("Large & Mid Cap", "high", "high", 6, [r"large (and|&) mid"]),
    ("Value", "high", "high", 5, [r"value fund"]),
    ("ELSS", "high", "high", 8, [r"elss|tax saver"]),
    ("Mid Cap", "very-high", "high", 8, [r"mid cap"]),
    ("Small Cap", "very-high", "high", 8, [r"small cap"]),
    ("Sectoral / Thematic", "very-high", "high", 6, [r"banking", r"technology", r"pharma", r"consumption"]),
]

RISK_LEVEL = {"low": "low", "low-to-moderate": "low", "moderate": "moderate",
              "moderately-high": "moderate", "high": "high", "very-high": "high"}

RISK_BLURB = {
    "low": "Low",
    "low-to-moderate": "Low to moderate",
    "moderate": "Moderate",
    "moderately-high": "Moderately high",
    "high": "High",
    "very-high": "Very high",
}

RISKS = {
    "Liquid": [
        "In stressed markets a liquid fund can deliver a negative day.",
        "Returns are modest and may not beat inflation.",
        "Exit loads or redemption limits can apply in unusual conditions.",
    ],
    "Ultra Short Duration": [
        "Interest-rate changes move the NAV, though less than for longer debt.",
        "Credit events in the holdings can hit the NAV.",
        "Returns are modest after expenses.",
    ],
    "Corporate Bond": [
        "The issuers in the fund can be downgraded or default.",
        "Prices fall when yields rise.",
        "Lower liquidity in the underlying bonds can widen exit spreads.",
    ],
    "Banking & PSU": [
        "Concentrated in one sector, so sector news moves the whole fund.",
        "Rate changes affect the bond holdings.",
        "Issuer concentration can matter more than in a diversified fund.",
    ],
    "Short Duration": [
        "Yields can rise faster than the portfolio reprices.",
        "Credit risk in the underlying issuers.",
        "Returns may lag a fixed deposit over short periods.",
    ],
    "Gilt": [
        "No credit risk, but full interest-rate risk: prices fall when yields rise.",
        "Long-duration gilts swing more than short ones.",
        "Returns can be negative in a rising-rate year.",
    ],
    "Dynamic Bond": [
        "The manager's rate calls can be wrong.",
        "Duration changes are not visible to you in advance.",
        "Returns can be volatile for a debt fund.",
    ],
    "Balanced Advantage": [
        "The equity-debt mix is the manager's call, so risk is not fixed.",
        "Still falls in a sharp equity downturn.",
        "Past smoothness is not a forecast.",
    ],
    "Aggressive Hybrid": [
        "Equity risk dominates; this is not a low-volatility product.",
        "The debt portion does not offset a severe equity fall.",
        "Tax treatment depends on the equity share, which can change.",
    ],
    "Index / Nifty 50": [
        "Falls with the market and can stay down for years.",
        "The index can be concentrated in a few sectors.",
        "Tracking difference makes returns drift from the index.",
    ],
    "Large Cap": [
        "Equity falls of 20-40% are normal, not exceptional.",
        "Manager decisions can lag the index.",
        "A higher expense ratio than a passive fund.",
    ],
    "Large & Mid Cap": [
        "Mid-cap exposure adds volatility beyond large caps.",
        "Concentration in a few holdings can drive returns.",
        "Falls harder than a pure large-cap fund in a downturn.",
    ],
    "Value": [
        "Cheap stocks can stay cheap for years.",
        "Style risk: value can lag growth for long stretches.",
        "Holdings can be concentrated in cyclical sectors.",
    ],
    "ELSS": [
        "Equity risk with a three-year lock-in that prevents a reaction.",
        "The deduction may be worth nothing under the new tax regime.",
        "Each SIP instalment has its own three-year clock.",
    ],
    "Mid Cap": [
        "Mid caps swing harder than large caps in both directions.",
        "Liquidity in the underlying stocks can dry up.",
        "Long drawdowns are common.",
    ],
    "Small Cap": [
        "The most volatile equity category; steep drawdowns are normal.",
        "Funds can close to new money when they get too large.",
        "Exit at scale can move prices against you.",
    ],
    "Sectoral / Thematic": [
        "A single sector or theme: one piece of news moves the whole fund.",
        "Sector indices can lag the broad market for years.",
        "Concentration is the point, and also the risk.",
    ],
}

USES = {
    "debt": ["Parking money for weeks or months", "A steadier alternative to equity"],
    "hybrid": ["Long-term goals with lower swings than pure equity", "A single fund that manages the mix"],
    "equity": ["Long-term goals seven years or more away", "The growth portion of a savings plan"],
}

COLLECTION_BY_RISK = {
    "low": ["short-term", "start-small"],
    "low-to-moderate": ["short-term"],
    "moderate": ["understand-before-you-invest"],
    "moderately-high": ["understand-before-you-invest"],
    "high": ["understand-before-you-invest", "start-small"],
    "very-high": ["understand-before-you-invest"],
}


def http_json(url: str):
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=30, context=ssl.create_default_context()) as response:
        return json.loads(response.read())


def slugify(text: str, code: int) -> str:
    text = re.sub(r"\s*-\s*direct plan.*$", "", text, flags=re.I)
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    text = re.sub(r"-+", "-", text)[:58].strip("-")
    return f"{text}-{code}"


def cagr(history: list[tuple[datetime, float]], years: float) -> float | None:
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


def pick_schemes(listing: list[dict], wanted: int) -> list[tuple[dict, tuple]]:
    pool = []
    for scheme in listing:
        name = scheme["schemeName"]
        low = name.lower()
        if "direct" not in low or "growth" not in low:
            continue
        if any(bad in low for bad in ("idcw", "dividend", "bonus", "regular plan")):
            continue
        for label, band, level, limit, patterns in CATEGORIES:
            if any(re.search(p, low) for p in patterns):
                pool.append((scheme, (label, band, level, limit, patterns)))
                break

    chosen, used_amc = [], {}
    for scheme, meta in pool:
        label, band, level, limit, _ = meta
        taken = used_amc.setdefault(label, 0)
        if taken >= limit:
            continue
        chosen.append((scheme, meta))
        used_amc[label] = taken + 1
        if len(chosen) >= wanted:
            break
    return chosen


def build_record(scheme: dict, meta: tuple, detail: dict) -> tuple[dict, dict] | None:
    label, band, level, _, _ = meta
    code = scheme["schemeCode"]
    name = detail["meta"]["scheme_name"]
    fund_house = detail["meta"]["fund_house"]

    history = []
    for row in detail["data"]:
        try:
            history.append((datetime.strptime(row["date"], "%d-%m-%Y"), float(row["nav"])))
        except (KeyError, ValueError):
            continue
    history.sort()
    if len(history) < 700:
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

    clean_name = re.sub(r"\s*-\s*direct plan", "", name, flags=re.I)
    clean_name = re.sub(r"\s*-\s*growth( option)?", "", clean_name, flags=re.I).strip(" -")

    slug = slugify(name, code)
    rate_key = f"nav-{code}"
    bucket = "debt" if level == "low" or label in {"Gilt", "Dynamic Bond", "Corporate Bond", "Short Duration"} else (
        "hybrid" if label in {"Balanced Advantage", "Aggressive Hybrid"} else "equity")
    lock_in = "3 years per contribution" if label == "ELSS" else None

    product = {
        "slug": slug,
        "name": clean_name,
        "provider": fund_house,
        "providerShort": fund_house.replace(" Mutual Fund", "").replace(" Mutual Fund", ""),
        "providerType": "Asset manager",
        "category": "mutual-funds",
        "returnType": "market-linked",
        "rateKey": rate_key,
        "fundCategory": label,
        "riskBand": band,
        "riskRank": ["low", "low-to-moderate", "moderate", "moderately-high", "high", "very-high"].index(band) + 1,
        "returns": returns,
        "demo": False,
        "oneLiner": f"{label} fund, direct plan. The figures shown are computed from its own NAV history, not quoted from a factsheet.",
        "minInvestment": 500,
        "minInvestmentNote": "typical SIP minimum; confirm on the scheme page",
        "tenure": "3-year lock-in per contribution" if label == "ELSS" else "No lock-in",
        "tenureMonths": 36 if label == "ELSS" else None,
        "payout": "Growth — no payout",
        "payoutFrequency": "growth",
        "liquidity": "Locked for three years from each contribution, then redeemable."
        if label == "ELSS"
        else "Redeemable on any business day. Exit load may apply within the first year.",
        "lockIn": lock_in,
        "eligibility": "Resident individuals and permitted non-resident categories, subject to KYC.",
        "tax": "Gains are taxed by holding period under equity or debt rules depending on the scheme's classification. Confirm the current treatment.",
        "protection": "No capital protection. The NAV moves with the underlying holdings.",
        "riskLevel": level,
        "risks": RISKS[label],
        "commonUses": USES[bucket],
        "check": [
            "The expense ratio and exit load on the scheme page",
            "The benchmark the fund is measured against",
        ],
        "collections": COLLECTION_BY_RISK[band],
        "sources": [
            {"label": "AMFI — scheme information", "url": "https://www.amfiindia.com"},
            {"label": "SEBI — mutual funds", "url": "https://www.sebi.gov.in"},
        ],
        "source": {
            "label": "AMFI — scheme and NAV data",
            "url": "https://www.amfiindia.com/mutual-fund",
            "note": f'Search "{clean_name}" on AMFI for this scheme\'s official NAV history, expense ratio and scheme documents.',
        },
        "lastVerified": TODAY,
        "review": {
            "status": "approved",
            "reviewer": "Automated NAV import, 19 Oct 2026",
            "approvedAt": TODAY,
            "notes": "Scheme name, category and NAV from AMFI data. Returns computed by PaisaClear; not a fund-house or SEBI figure.",
        },
    }

    rate = {
        "value": f"₹{latest_nav:,.2f}",
        "label": "NAV, direct plan",
        "asOf": latest_date.strftime("%Y-%m-%d"),
        "cadence": "Published daily by AMFI",
        "sourceUrl": "https://www.amfiindia.com/mutual-fund",
        "sourceLabel": "AMFI — mutual fund NAV data",
    }
    return product, rate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print(f"Fetching scheme list… (target {args.count} funds)")
    listing = http_json("https://api.mfapi.in/mf")
    picked = pick_schemes(listing, args.count * 2)
    print(f"  candidates after category filtering: {len(picked)}")

    products = json.loads(PRODUCTS.read_text(encoding="utf-8"))
    rates = json.loads(RATES.read_text(encoding="utf-8"))
    existing_slugs = {p["slug"] for p in products}
    existing_rates = set(rates["values"])

    def fetch(item):
        scheme, meta = item
        try:
            return scheme, meta, http_json(f"https://api.mfapi.in/mf/{scheme['schemeCode']}")
        except Exception:
            return scheme, meta, None

    built, seen = [], set()
    with ThreadPoolExecutor(max_workers=8) as pool:
        for scheme, meta, detail in pool.map(fetch, picked):
            if detail is None or len(built) >= args.count:
                continue
            result = build_record(scheme, meta, detail)
            if not result:
                continue
            product, rate = result
            # Skip anything already in the catalogue, including scheme codes we
            # imported earlier under a hand-written slug.
            if (product["slug"] in existing_slugs
                    or product["slug"] in seen
                    or product["rateKey"] in existing_rates):
                continue
            seen.add(product["slug"])
            built.append((product, rate))

    print(f"  built {len(built)} fund records")

    if args.dry_run:
        for product, rate in built[:10]:
            r = product["returns"]
            print(f"    {product['fundCategory']:<22} 1y={r['oneYear']!s:>7} 3y={r['threeYear']:>6} "
                  f"5y={r['fiveYear']!s:>7}  {product['name'][:48]}")
        print("  dry run — nothing written")
        return 0

    for product, rate in built:
        products.append(product)
        rates["values"][product["rateKey"]] = rate

    rates["generatedAt"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    PRODUCTS.write_text(json.dumps(products, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    RATES.write_text(json.dumps(rates, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    by_cat: dict[str, int] = {}
    for product, _ in built:
        by_cat[product["fundCategory"]] = by_cat.get(product["fundCategory"], 0) + 1
    print("\n  by category:")
    for label, count in sorted(by_cat.items()):
        print(f"    {label:<24} {count}")
    print(f"\n  products now: {len(products)} | rates now: {len(rates['values'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
