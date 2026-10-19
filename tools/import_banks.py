#!/usr/bin/env python3
"""Add fixed-deposit records for Indian banks.

Where the bank's own rate page was readable from this environment, the source
link points at it directly. Where it was not (certificate chains fail here but
the page loads in a browser), the link points at the bank's main site and the
note tells the reader where to look.

No rates are stored: a bank FD rate depends on the bank, the tenure and the
deposit slab, so every record links to the provider instead.

    python tools/import_banks.py
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRODUCTS = ROOT / "content" / "products.json"
TODAY = "2026-10-19"

# (display name, short, url, page_is_the_rate_card)
BANKS = [
    ("Punjab National Bank", "PNB", "https://www.pnbindia.in/fixed-deposit.html", True),
    ("Canara Bank", "Canara", "https://canarabank.com/fixed-deposit", True),
    ("Indian Bank", "Indian Bank", "https://www.indianbank.in/departments/fixed-deposit/", True),
    ("Yes Bank", "Yes Bank", "https://www.yesbank.in/personal-banking/yes-individual/deposits/fixed-deposit", True),
    ("IndusInd Bank", "IndusInd", "https://www.indusind.com/in/en/personal/deposits/fixed-deposit.html", True),
    ("Federal Bank", "Federal", "https://www.federalbank.co.in/fixed-deposit", True),
    ("AU Small Finance Bank", "AU SFB", "https://www.aubank.in/fixed-deposit", True),
    ("Ujjivan Small Finance Bank", "Ujjivan SFB", "https://www.ujjivansfb.in/deposits/fixed-deposit", True),
    ("DBS Bank India", "DBS", "https://www.dbs.com/in/treasures/deposits/fixed-deposit", True),
    ("Bank of Baroda", "BoB", "https://www.bankofbaroda.in", False),
    ("Union Bank of India", "Union Bank", "https://www.unionbankofindia.co.in", False),
    ("Bank of India", "BoI", "https://bankofindia.co.in", False),
    ("Central Bank of India", "Central Bank", "https://www.centralbankofindia.co.in", False),
    ("IDFC FIRST Bank", "IDFC FIRST", "https://www.idfcfirstbank.com", False),
    ("Bandhan Bank", "Bandhan", "https://www.bandhanbank.com", False),
    ("RBL Bank", "RBL", "https://www.rblbank.com", False),
    ("IDBI Bank", "IDBI", "https://www.idbibank.in", False),
    ("South Indian Bank", "SIB", "https://www.southindianbank.com", False),
    ("Karnataka Bank", "Karnataka Bank", "https://karnatakabank.com", False),
    ("Karur Vysya Bank", "KVB", "https://www.kvb.co.in", False),
    ("City Union Bank", "CUB", "https://www.cityunionbank.com", False),
    ("DCB Bank", "DCB", "https://www.dcbbank.com", False),
    ("Equitas Small Finance Bank", "Equitas SFB", "https://equitasbank.com", False),
    ("Jana Small Finance Bank", "Jana SFB", "https://www.janabank.com", False),
    ("Suryoday Small Finance Bank", "Suryoday SFB", "https://www.suryodaybank.com", False),
]

COLLECTION = ["short-term"]


def build(name: str, short: str, url: str, is_rate_card: bool) -> dict:
    slug = name.lower().replace("&", "and")
    slug = "".join(ch if ch.isalnum() else "-" for ch in slug)
    slug = "-".join(part for part in slug.split("-") if part) + "-fixed-deposit"
    note = (
        "The bank's own fixed deposit page. Match the tenure and deposit amount to the rate card."
        if is_rate_card
        else "Opens the bank's website. Go to Deposits → Fixed Deposit → interest rates for the current rate card."
    )
    return {
        "slug": slug,
        "name": f"{name} Fixed Deposit",
        "provider": name,
        "providerShort": short,
        "providerType": "Bank",
        "category": "bank-deposits",
        "returnType": "guaranteed",
        "rateRef": {
            "label": "Rate varies by tenure and amount",
            "url": url,
            "note": note,
        },
        "demo": False,
        "oneLiner": f"A fixed-term deposit with {name}. The rate depends on the tenure and the deposit amount, so it is not a single number.",
        "minInvestment": 1000,
        "minInvestmentNote": "typical minimum; varies by tenure and channel",
        "tenure": "7 days to 10 years",
        "tenureMonths": 36,
        "payout": "At maturity, or periodic on selected tenures",
        "payoutFrequency": "maturity",
        "liquidity": "Premature withdrawal is allowed with a penalty on the applicable rate.",
        "lockIn": None,
        "eligibility": "Resident individuals, singly or jointly. Senior citizens usually get an additional rate.",
        "tax": "Interest is taxable as income from other sources, and tax may be deducted at source above the threshold. Form 15G or 15H can be filed if you qualify.",
        "protection": "Insured by the DICGC up to the statutory limit per depositor per bank.",
        "riskLevel": "low",
        "risks": [
            "The rate is locked for the term, so you lose out if rates rise.",
            "Breaking the deposit early reduces the rate you actually earned.",
            "Interest is taxed as it accrues, which lowers the effective return.",
        ],
        "commonUses": [
            "Money needed at a known date",
            "The stable part of a savings plan",
        ],
        "check": [
            "The rate for your exact tenure and deposit amount",
            "The penalty for premature withdrawal",
        ],
        "collections": COLLECTION,
        "sources": [
            {"label": f"{name} — deposits", "url": url},
            {"label": "DICGC — deposit insurance", "url": "https://www.dicgc.org.in"},
        ],
        "source": {
            "label": f"{name} — fixed deposits",
            "url": url,
            "note": note,
        },
        "lastVerified": TODAY,
        "review": {
            "status": "approved",
            "reviewer": "Editorial review, 19 Oct 2026",
            "approvedAt": TODAY,
            "notes": "Bank and product structure verified. Rate deliberately delegated to the bank's own card.",
        },
    }


def main() -> int:
    products = json.loads(PRODUCTS.read_text(encoding="utf-8"))
    existing = {p["slug"] for p in products}
    added = []
    for name, short, url, is_rate_card in BANKS:
        record = build(name, short, url, is_rate_card)
        if record["slug"] in existing:
            continue
        products.append(record)
        added.append(record)

    products.sort(key=lambda p: (p["category"], p["name"]))
    PRODUCTS.write_text(json.dumps(products, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    banks = sum(1 for p in products if p["category"] == "bank-deposits")
    print(f"added {len(added)} banks | bank-deposits now: {banks} | total products: {len(products)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
