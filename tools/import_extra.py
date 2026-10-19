#!/usr/bin/env python3
"""Extra central schemes and link-only bonds.

These records carry no rate: each links to the official page where the current
terms live. That keeps the catalogue honest when a figure changes by
notification rather than by market.

    python tools/import_extra.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRODUCTS = ROOT / "content" / "products.json"
TODAY = "2026-10-19"

IP = "https://www.indiapost.gov.in/banking-services/savings"
JS = "https://www.jansuraksha.gov.in"
PFRDA = "https://www.pfrda.org.in"
MAANDHAN = "https://maandhan.in"
PMJDY = "https://pmjdy.gov.in"
NPS = "https://www.npscra.nsdl.co.in"
RBI = "https://www.rbi.org.in"

SCHEMES = [
    {
        "slug": "post-office-recurring-deposit",
        "name": "Post Office Recurring Deposit",
        "one": "A five-year monthly-deposit scheme: you pay a fixed amount each month and receive the total with interest at maturity.",
        "min": 100, "min_note": "per month, and in multiples of ₹10",
        "tenure": "5 years", "months": 60, "payout": "At maturity", "freq": "maturity",
        "liquidity": "Locked for five years; premature closure allowed after three years with a rate penalty.",
        "elig": "Resident individuals, singly or jointly. A guardian can open one for a minor.",
        "tax": "Interest is taxable as income from other sources and may attract tax deducted at source.",
        "prot": "A sovereign liability of the Government of India.",
        "risks": [
            "Missing a monthly instalment can default the account and attract a fee.",
            "The rate is notified quarterly and can be revised.",
            "Five years of fixed monthly payments is a commitment, not a flexible saving.",
        ],
        "uses": ["Building a lump sum from monthly savings", "A disciplined, low-risk savings habit"],
        "check": ["The default fee if you miss an instalment", "Whether the account can be revived after default"],
        "url": IP, "label": "India Post — saving schemes",
        "note": "The official page listing this scheme with the current rates and rules.",
        "collections": ["government-backed", "start-small"],
    },
    {
        "slug": "post-office-time-deposit-1-year",
        "name": "Post Office Time Deposit (1 year)",
        "one": "A one-year deposit with the post office at a notified rate, with a shorter lock-in than the longer tenures.",
        "min": 1000, "min_note": "and in multiples of ₹100",
        "tenure": "1 year", "months": 12, "payout": "Interest credited annually", "freq": "annual",
        "liquidity": "Premature closure allowed after six months at a reduced rate.",
        "elig": "Resident individuals, singly or jointly, and some institutions.",
        "tax": "Interest is taxable. The one-year deposit does not qualify for the Section 80C deduction.",
        "prot": "A sovereign liability of the Government of India.",
        "risks": [
            "No 80C deduction at this tenure.",
            "Early exit reduces the rate you earned.",
            "The rate is fixed at opening, so a later deposit may earn more.",
        ],
        "uses": ["Parking money for a year at a notified rate", "A short, fixed commitment"],
        "check": ["The current rate for the one-year tenure", "The penalty for closing early"],
        "url": IP, "label": "India Post — saving schemes",
        "note": "The official page listing this scheme with the current rates and rules.",
        "collections": ["government-backed", "short-term"],
    },
    {
        "slug": "post-office-time-deposit-2-year",
        "name": "Post Office Time Deposit (2 years)",
        "one": "A two-year deposit with the post office, sitting between the one-year and three-year rates.",
        "min": 1000, "min_note": "and in multiples of ₹100",
        "tenure": "2 years", "months": 24, "payout": "Interest credited annually", "freq": "annual",
        "liquidity": "Premature closure allowed after six months at a reduced rate.",
        "elig": "Resident individuals, singly or jointly, and some institutions.",
        "tax": "Interest is taxable. The two-year deposit does not qualify for the Section 80C deduction.",
        "prot": "A sovereign liability of the Government of India.",
        "risks": [
            "No 80C deduction at this tenure.",
            "Early exit reduces the effective rate.",
            "Interest is taxed as it accrues.",
        ],
        "uses": ["A two-year place for money with a known date", "A step between short and medium tenures"],
        "check": ["The rate for the two-year tenure", "The penalty for closing early"],
        "url": IP, "label": "India Post — saving schemes",
        "note": "The official page listing this scheme with the current rates and rules.",
        "collections": ["government-backed", "short-term"],
    },
    {
        "slug": "pradhan-mantri-jan-dhan-yojana",
        "name": "Pradhan Mantri Jan Dhan Yojana",
        "one": "A basic savings account with no minimum balance requirement, opened through any bank or post office.",
        "min": 0, "min_note": "no minimum balance requirement",
        "tenure": "No fixed term", "months": None, "payout": "Interest credited periodically", "freq": "annual",
        "liquidity": "Withdraw any time.",
        "elig": "Any resident aged 10 or above without an existing bank account, with KYC documents.",
        "tax": "Interest is taxable as income from other sources.",
        "prot": "A bank deposit, covered by DICGC insurance up to the statutory limit.",
        "risks": [
            "The rate is typically low, so the balance loses value to inflation.",
            "It is a bank account, not an investment.",
            "Some accounts attract charges if the balance stays nil for long periods.",
        ],
        "uses": ["A first bank account with no balance requirement", "Receiving government transfers"],
        "check": ["Whether the account comes with a RuPay card and accident cover", "Any charges for inactivity"],
        "url": PMJDY, "label": "PMJDY — official portal",
        "note": "The official scheme portal, with eligibility and how to open an account.",
        "collections": ["government-backed", "start-small"],
    },
    {
        "slug": "national-pension-system",
        "name": "National Pension System (NPS)",
        "one": "A voluntary pension account where contributions are invested in market-linked funds until you retire.",
        "min": 500, "min_note": "minimum per contribution; annual minimum applies",
        "tenure": "Until age 60", "months": 240, "payout": "Pension after 60", "freq": "monthly",
        "liquidity": "Locked until 60 in most cases, with limited partial withdrawals after three years.",
        "elig": "Resident individuals aged 18 to 70, subject to KYC.",
        "tax": "Contributions may qualify for a deduction. Part of the maturity amount is taxable; rules differ by how you exit.",
        "prot": "No capital protection: the corpus is invested in market-linked funds.",
        "risks": [
            "The corpus can fall: it is invested in equity and debt funds.",
            "Part of the corpus must buy an annuity at exit, on terms available then.",
            "Charges and fund choices affect the final corpus.",
        ],
        "uses": ["Building a retirement corpus with regular contributions", "A market-linked pension alongside fixed deposits"],
        "check": ["The fund manager and allocation you choose", "The annuity rules at your exit age"],
        "url": NPS, "label": "NPS — official portal",
        "note": "The official NPS portal, with contribution rules, fund choices and exit conditions.",
        "collections": ["understand-before-you-invest"],
        "returnType": "market-linked",
    },
    {
        "slug": "atal-pension-yojana",
        "name": "Atal Pension Yojana (APY)",
        "one": "A government pension scheme for the unorganised sector: contribute until 60, then receive a fixed monthly pension.",
        "min": 1000, "min_note": "minimum annual contribution; varies with the pension chosen",
        "tenure": "Until age 60", "months": 240, "payout": "Pension after 60", "freq": "monthly",
        "liquidity": "Locked until 60, except in specified circumstances such as death or terminal illness.",
        "elig": "Indian citizens aged 18 to 40 with a savings account, and not already in a tax-paying bracket under the scheme rules.",
        "tax": "Contributions may qualify for a deduction. The pension is taxable as income.",
        "prot": "The pension is guaranteed by the government once the scheme conditions are met.",
        "risks": [
            "The pension is fixed in rupees, so inflation erodes it over a long retirement.",
            "Contributions are locked for decades.",
            "Missing contributions can lead to account closure and penalties.",
        ],
        "uses": ["A small guaranteed pension after 60", "Saving for retirement without market risk"],
        "check": ["The contribution for your age and chosen pension", "The penalty for a missed contribution"],
        "url": PFRDA, "label": "PFRDA — Atal Pension Yojana",
        "note": "The regulator's page for the scheme, with the contribution chart and eligibility.",
        "collections": ["government-backed", "monthly-income"],
        "returnType": "conditional",
    },
    {
        "slug": "pradhan-mantri-jeevan-jyoti-bima-yojana",
        "name": "Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY)",
        "one": "A low-cost term life cover of ₹2 lakh, renewed annually, with the premium debited from your bank account.",
        "min": 436, "min_note": "annual premium, debited automatically; the figure is revised periodically",
        "tenure": "One year, renewable", "months": 12, "payout": "Lump sum to the nominee on death", "freq": "maturity",
        "liquidity": "There is no maturity value: this is insurance, not savings.",
        "elig": "Account holders aged 18 to 50 who join before turning 50, with the premium auto-debited.",
        "tax": "The premium may qualify for a deduction; the payout to a nominee is generally exempt.",
        "prot": "Backed by the participating bank or insurer under the scheme's terms.",
        "risks": [
            "No money comes back if you survive the term — it is pure protection.",
            "Cover stops if the premium cannot be debited.",
            "The premium and terms can be revised by the government.",
        ],
        "uses": ["Cheap life cover for a family's protection", "A safety net alongside savings products"],
        "check": ["The current premium for the enrolment year", "The cut-off age for joining and renewing"],
        "url": JS, "label": "Jan Suraksha — official portal",
        "note": "The official portal for the scheme, with current premium, eligibility and enrolment steps.",
        "collections": ["government-backed", "start-small"],
        "returnType": "conditional",
    },
    {
        "slug": "pradhan-mantri-suraksha-bima-yojana",
        "name": "Pradhan Mantri Suraksha Bima Yojana (PMSBY)",
        "one": "Accident cover of ₹2 lakh for a very small annual premium, debited from your account.",
        "min": 20, "min_note": "annual premium, debited automatically; the figure is revised periodically",
        "tenure": "One year, renewable", "months": 12, "payout": "Lump sum on accidental death or disability", "freq": "maturity",
        "liquidity": "No maturity value: this is accident insurance.",
        "elig": "Account holders aged 18 to 70, with the premium auto-debited.",
        "tax": "The payout is generally exempt; the premium is not a savings deduction.",
        "prot": "Backed by the participating bank or insurer under the scheme's terms.",
        "risks": [
            "Covers accidents only, not illness or natural death.",
            "Cover stops if the premium cannot be debited.",
            "There is no return of premium.",
        ],
        "uses": ["Very cheap accident cover", "A basic safety net alongside a savings account"],
        "check": ["The current premium", "What counts as disability under the scheme"],
        "url": JS, "label": "Jan Suraksha — official portal",
        "note": "The official portal for the scheme, with current premium and claim conditions.",
        "collections": ["government-backed", "start-small"],
        "returnType": "conditional",
    },
]

BONDS = [
    {
        "slug": "sovereign-gold-bond",
        "name": "Sovereign Gold Bond",
        "one": "A government bond denominated in grams of gold, issued in tranches, paying a small fixed interest on top of the gold price.",
        "min": 10000, "min_note": "roughly one gram, priced per tranche",
        "tenure": "8 years", "months": 96, "payout": "Half-yearly interest, principal in gold at maturity", "freq": "semi-annual",
        "liquidity": "Tradable on the exchange after the lock-in; early redemption allowed after five years on interest-payment dates.",
        "elig": "Resident individuals, with limits on how much one person may hold per year.",
        "tax": "Interest is taxable. Redemption at maturity is generally exempt from capital gains; an early sale is not.",
        "prot": "Sovereign — the Government of India is the issuer.",
        "risks": [
            "The redemption value follows the gold price, which can fall.",
            "An early sale before maturity changes the tax treatment.",
            "Issues are periodic; you can only buy during an open tranche.",
        ],
        "uses": ["Holding gold without storage costs", "A hedge alongside equity"],
        "check": ["Whether a tranche is currently open", "The issue price and the holding limits"],
        "url": f"{RBI}", "label": "RBI — Sovereign Gold Bond",
        "note": "The RBI's page for the scheme, with tranche dates, issue price and redemption rules.",
        "collections": ["government-backed", "understand-before-you-invest"],
    },
    {
        "slug": "state-development-loan",
        "name": "State Development Loan (SDL)",
        "one": "A bond issued by a state government to fund local spending, paying a fixed coupon until maturity.",
        "min": 10000, "min_note": "minimum amount in the retail direct scheme",
        "tenure": "Typically 5 to 10 years", "months": 120, "payout": "Half-yearly interest", "freq": "semi-annual",
        "liquidity": "Traded, usually with thinner volumes than central government bonds.",
        "elig": "Resident individuals with a demat account and an RBI Retail Direct account.",
        "tax": "Interest is taxable as income from other sources; sale before maturity creates a capital gain or loss.",
        "prot": "Issued by a state government. State issuers are not identical in credit quality.",
        "risks": [
            "Thinner liquidity than central government bonds, so exit prices can be worse.",
            "A fixed coupon for years may lag inflation.",
            "State finances differ; do not treat all state issuers as equivalent.",
        ],
        "uses": ["A slightly higher yield than central government debt", "Regular semi-annual income"],
        "check": ["Which state is issuing, and its borrowing record", "The difference between the offer price and face value"],
        "url": RBI, "label": "RBI Retail Direct — government securities",
        "note": "Where state and central government securities are listed for retail purchase.",
        "collections": ["government-backed"],
    },
]


def make(record: dict, category: str, return_type: str) -> dict:
    return {
        "slug": record["slug"],
        "name": record["name"],
        "provider": "Government of India — small savings" if category == "government-schemes" else "Government of India — via RBI Retail Direct",
        "providerShort": "Government",
        "providerType": "Government",
        "category": category,
        "returnType": record.get("returnType", return_type),
        "rateRef": {
            "label": "Terms set by notification",
            "url": record["url"],
            "note": record["note"],
        },
        "demo": False,
        "oneLiner": record["one"],
        "minInvestment": record["min"],
        "minInvestmentNote": record["min_note"],
        "tenure": record["tenure"],
        "tenureMonths": record["months"],
        "payout": record["payout"],
        "payoutFrequency": record["freq"],
        "liquidity": record["liquidity"],
        "lockIn": None,
        "eligibility": record["elig"],
        "tax": record["tax"],
        "protection": record["prot"],
        "riskLevel": "moderate" if record.get("returnType") == "market-linked" else "low",
        "risks": record["risks"],
        "commonUses": record["uses"],
        "check": record["check"],
        "collections": record["collections"],
        "sources": [{"label": record["label"], "url": record["url"]}],
        "source": {"label": record["label"], "url": record["url"], "note": record["note"]},
        "lastVerified": TODAY,
        "review": {
            "status": "approved",
            "reviewer": "Editorial review, 19 Oct 2026",
            "approvedAt": TODAY,
            "notes": "Structure and official link verified. No rate stored: terms are set by notification and change.",
        },
    }


def main() -> int:
    products = json.loads(PRODUCTS.read_text(encoding="utf-8"))
    existing = {p["slug"] for p in products}
    added = 0
    for record in SCHEMES:
        if record["slug"] in existing:
            continue
        products.append(make(record, "government-schemes", "guaranteed"))
        added += 1
    for record in BONDS:
        if record["slug"] in existing:
            continue
        products.append(make(record, "bonds", "guaranteed"))
        added += 1
    products.sort(key=lambda p: (p["category"], p["name"]))
    PRODUCTS.write_text(json.dumps(products, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    counts = {}
    for p in products:
        counts[p["category"]] = counts.get(p["category"], 0) + 1
    print(f"added {added} | totals: {counts} | all: {len(products)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
