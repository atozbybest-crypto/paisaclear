#!/usr/bin/env python3
"""LIC policy records, built from LIC's own sales brochures.

Each record was read from the brochure named in `brochure`; the terms below are
those the brochure states. Premiums are deliberately not published: they depend
on age, term and sum assured, so every record links to LIC's calculator page.

    python tools/import_lic.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRODUCTS = ROOT / "content" / "products.json"
TODAY = "2026-10-19"

PLANS_PAGE = "https://licindia.in/web/guest/insurance-plan"
PENSION_PAGE = "https://licindia.in/web/guest/pension-plan"
ULIP_PAGE = "https://licindia.in/web/guest/unit-linked-plans"
TERM_PAGE = "https://licindia.in/web/guest/term-assurance-plans"
ENDOW_PAGE = "https://licindia.in/web/guest/endowment-plans"
GIFT_PAGE = "https://licindia.in/web/guest/gift-city-plans"

PREMIUM_NOTE = "Premium depends on age, term and sum assured — use LIC's calculator for your figure"

TAX_COMMON = (
    "Premiums may qualify for a deduction under Section 80C. Maturity proceeds are exempt "
    "only if the policy meets the conditions in Section 10(10D), including the aggregate "
    "premium limit — check the current rules for the year you buy."
)
PROT_COMMON = (
    "Backed by LIC, a state-owned insurer. A policy is not a bank deposit and is not covered "
    "by DICGC insurance."
)

PLANS = [
    {
        "slug": "lic-index-plus",
        "name": "LIC's Index Plus",
        "uin": "512L354V01",
        "type": "linked",
        "one": "A unit-linked savings plan: part of each premium buys life cover, the rest buys units in a fund you choose.",
        "tenure": "Policy term chosen at purchase",
        "payout": "Fund value at maturity, with guaranteed additions",
        "liquidity": "No surrender or withdrawal at all in the first five years. After that, partial withdrawals are allowed within the rules.",
        "elig": "Entry ages and sum-assured multiples (7x or 10x annualised premium) are set out in the brochure.",
        "protect": "Life cover for the term; the investment value is not guaranteed.",
        "risks": [
            "The fund value can fall — the investment risk is yours.",
            "Nothing can be withdrawn for the first five years.",
            "Charges are deducted from the fund and reduce the eventual value.",
        ],
        "uses": ["Long-term savings with life cover in one contract", "Investing in a fund of your choice inside an insurance wrapper"],
        "check": ["The charges: allocation, policy administration and fund management", "What the guaranteed additions are worth as a percentage of premium"],
        "url": ULIP_PAGE,
        "brochure": "101941 LIC_Index Plus Sales Brochure.pdf",
    },
    {
        "slug": "lic-dhan-vriddhi",
        "name": "LIC's Dhan Vriddhi",
        "uin": "512N362V02",
        "type": "endowment",
        "one": "A single-premium savings policy with a guaranteed lump sum at maturity, sold as protection plus savings.",
        "tenure": "10, 15 or 18 years",
        "payout": "Guaranteed lump sum at maturity",
        "liquidity": "Surrender is allowed once the policy acquires a surrender value; a policy loan is available.",
        "elig": "Entry from 90 days (18-year term), 3 years (15-year) or 8 years (10-year). Maximum entry age 60, 35 or 32 depending on term.",
        "protect": "Guaranteed benefits fixed at purchase; not a market-linked return.",
        "risks": [
            "A single premium ties up a large sum for 10 to 18 years.",
            "Surrendering early usually returns less than you paid.",
            "The guaranteed return can lag inflation and other savings options.",
        ],
        "uses": ["A guaranteed lump sum at a known date", "Parking a maturity or bonus in a single-premium policy"],
        "check": ["The minimum sum assured (₹1,25,000) and the multiples it must be in", "The surrender value in each of the first five years"],
        "url": ENDOW_PAGE,
        "brochure": "Lic leaflet  Dhan Vriddhi 4x9 inches wxh web.pdf",
    },
    {
        "slug": "lic-new-jeevan-shanti",
        "name": "LIC's New Jeevan Shanti",
        "uin": "512N338V08",
        "type": "annuity",
        "one": "A deferred annuity: pay a single premium now, and a guaranteed pension starts after a waiting period you choose.",
        "tenure": "Deferment period chosen at purchase, then income for life",
        "payout": "Annuity for life, yearly to monthly",
        "liquidity": "The purchase price is locked in; a loan or surrender may be available on the terms in the policy.",
        "elig": "Single or joint life. A joint annuity can be taken with a spouse, siblings, or a lineal descendant or ancestor.",
        "protect": "Annuity rates are guaranteed at inception and paid for life.",
        "risks": [
            "Once bought, the money is committed — you cannot change your mind cheaply.",
            "A fixed rupee pension loses value to inflation over a long retirement.",
            "The rate is locked at purchase; if annuity rates rise later, you cannot benefit.",
        ],
        "uses": ["Turning a lump sum into a pension that starts later", "A joint-life pension for a couple"],
        "check": ["The deferment period and what happens if you die during it", "The annuity rate for the option you choose"],
        "url": PENSION_PAGE,
        "brochure": "Lic NEW Jeevan Shanti  2025 _Eng_Singal page 21.08.2025.pdf",
    },
    {
        "slug": "lic-jeevan-akshay-vii",
        "name": "LIC's Jeevan Akshay-VII",
        "uin": "512N337V07",
        "type": "annuity",
        "one": "An immediate annuity: pay a single premium and the pension starts straight away, at a rate fixed for life.",
        "tenure": "Lifetime",
        "payout": "Annuity for life, yearly to monthly",
        "liquidity": "The purchase price is not returnable except under the options that include a return of purchase price.",
        "elig": "Single or joint life; joint annuity with a spouse, siblings or a lineal descendant or ancestor.",
        "protect": "Annuity rate guaranteed at inception.",
        "risks": [
            "No return of capital unless you choose an option that includes it.",
            "The pension is fixed in rupees and loses value to inflation.",
            "You cannot exit if you later need the money.",
        ],
        "uses": ["Converting a retirement corpus into a lifelong income", "A pension that starts immediately"],
        "check": ["Which option you need: life only, or with a 5- or 10-year guarantee", "Whether a return of purchase price matters to your heirs"],
        "url": PENSION_PAGE,
        "brochure": "LIC_Jeevan Akshay VII_Sales Brochure_4 inch x 9 inch_Eng _20082025.pdf",
    },
    {
        "slug": "lic-saral-pension",
        "name": "LIC's Saral Pension",
        "uin": "512N342V05",
        "type": "annuity",
        "one": "An IRDAI standard immediate annuity, sold on identical terms by every insurer: pension for life with the purchase price returned on death.",
        "tenure": "Lifetime",
        "payout": "Annuity for life, yearly to monthly",
        "liquidity": "The purchase price comes back to your nominee, but not to you during your life.",
        "elig": "Single life with return of purchase price, or joint life with return on the death of the last survivor.",
        "protect": "Annuity rate guaranteed at inception; 100% of the purchase price is returned on death.",
        "risks": [
            "The pension is fixed in rupees, so inflation erodes it.",
            "You cannot withdraw the capital yourself.",
            "The annuity rate is locked at purchase.",
        ],
        "uses": ["A simple pension with capital returned to the family", "Comparing insurers on identical terms"],
        "check": ["The annuity rate offered for your age", "The difference between Option I and Option II for a couple"],
        "url": PENSION_PAGE,
        "brochure": "LIC_Saral Pension_Sales Brochure_4 inch x 9 inch_Eng (1) (1).pdf",
    },
    {
        "slug": "lic-bima-jyoti",
        "name": "LIC's BIMA JYOTI",
        "uin": "512N339V03",
        "type": "endowment",
        "one": "A savings policy that pays a guaranteed lump sum at maturity and adds guaranteed additions of ₹50 per thousand of sum assured.",
        "tenure": "Policy term chosen at purchase",
        "payout": "Lump sum at maturity, with guaranteed additions",
        "liquidity": "Surrender value after the policy acquires one; a loan is available against it.",
        "elig": "Entry from 30 days completed to age 60. Minimum maturity age 18.",
        "protect": "Guaranteed benefits fixed at purchase.",
        "risks": [
            "The return is modest compared with market-linked options.",
            "Stopping premiums early can mean a much lower payout.",
            "A fixed rupee payout loses value to inflation over long terms.",
        ],
        "uses": ["A guaranteed sum for a long-term goal", "Life cover with a savings component"],
        "check": ["The guaranteed additions for your term and sum assured", "The surrender value in the early years"],
        "url": ENDOW_PAGE,
        "brochure": "LIC's Modified BIMA JYOTI Plan_Sales Brochure _Eng.pdf",
    },
    {
        "slug": "lic-nav-jeevan-shree",
        "name": "LIC's Nav Jeevan Shree — Single Premium",
        "uin": "512N390V01",
        "type": "endowment",
        "one": "A single-premium endowment with guaranteed additions of ₹85 per ₹1,000 of sum assured, paid at maturity.",
        "tenure": "Policy term chosen at purchase",
        "payout": "Maturity or death benefit, in lump sum or instalments",
        "liquidity": "Surrender once a surrender value exists; a policy loan is available.",
        "elig": "Two sum-assured-on-death options, chosen at inception.",
        "protect": "Guaranteed benefits fixed at purchase.",
        "risks": [
            "A large single premium is locked away for the full term.",
            "Early surrender returns less than the premium paid.",
            "The guaranteed return may be below inflation.",
        ],
        "uses": ["A guaranteed corpus from a lump sum", "A single-premium policy with instalment payout options"],
        "check": ["The surrender value in each of the first five years", "Which death-benefit option suits your dependants"],
        "url": ENDOW_PAGE,
        "brochure": "LIC_Single prem Nav Jeevan Shree_Sales Brochure_Eng single.pdf",
    },
    {
        "slug": "lic-new-jeevan-dhara-ii",
        "name": "LIC's New Jeevan Dhara-II",
        "uin": "512N398V01",
        "type": "annuity",
        "one": "A deferred annuity with regular or single premiums, where you choose when the pension starts — up to 15 years later.",
        "tenure": "Deferment 2–15 years (regular premium), 1–15 years (single premium)",
        "payout": "Annuity for life after the deferment period",
        "liquidity": "A liquidity option allows a lump sum in return for a lower annuity; otherwise the corpus is committed.",
        "elig": "Single or joint life. Regular or single premium.",
        "protect": "Annuity rates guaranteed at inception.",
        "risks": [
            "A long deferment means the money is committed for years.",
            "The annuity is fixed in rupees and loses value to inflation.",
            "Taking the liquidity option permanently reduces the pension.",
        ],
        "uses": ["Building a pension while still earning", "Choosing a start date for retirement income"],
        "check": ["The deferment period you can commit to", "What a top-up contribution does to the eventual annuity"],
        "url": PENSION_PAGE,
        "brochure": "LIC's New Jeevan Dhara-II_Sales Brochure_English.pdf",
    },
    {
        "slug": "lic-siip",
        "name": "LIC's SIIP",
        "uin": "512L334V02",
        "type": "linked",
        "one": "A unit-linked savings plan with four fund choices, life cover, and a refund of mortality charges if you survive to maturity.",
        "tenure": "Policy term chosen at purchase",
        "payout": "Fund value at maturity, plus guaranteed additions",
        "liquidity": "No surrender or withdrawal in the first five years; partial withdrawals after that within the rules.",
        "elig": "Entry ages set out in the brochure; four fund types to choose from.",
        "protect": "Life cover only; the fund value is not guaranteed.",
        "risks": [
            "The fund value can fall with the market.",
            "Five-year lock-in with no access.",
            "Charges reduce the units you hold.",
        ],
        "uses": ["Market-linked savings with cover", "Choosing your own fund mix inside a policy"],
        "check": ["The charge structure in the first five years", "The fund options and their mandates"],
        "url": ULIP_PAGE,
        "brochure": "SIIP Sales Brochure.pdf",
    },
    {
        "slug": "lic-smart-pension",
        "name": "LIC's Smart Pension",
        "uin": "512N386V01",
        "type": "annuity",
        "one": "An immediate annuity with a wide range of options, including liquidity, advance annuity and annuity accumulation.",
        "tenure": "Lifetime",
        "payout": "Annuity for life, yearly to monthly",
        "liquidity": "Depends on the options chosen; some allow a lump sum at a cost to the annuity.",
        "elig": "Individuals or groups; single or joint life.",
        "protect": "Annuity rates guaranteed at inception.",
        "risks": [
            "The pension is fixed in rupees and does not rise with prices.",
            "Choosing a liquidity option permanently lowers the pension.",
            "The rate is locked; later, better rates cannot be taken.",
        ],
        "uses": ["A pension with more flexibility than a plain annuity", "Converting a corpus with optional withdrawal features"],
        "check": ["Which options are included in the quote you receive", "The effect of the liquidity option on your pension"],
        "url": PENSION_PAGE,
        "brochure": "Smart Pension Individual_Sales Brochure Eng.pdf",
    },
    {
        "slug": "lic-new-pension-plus",
        "name": "LIC's New Pension Plus",
        "uin": "512L347V01",
        "type": "linked",
        "one": "A unit-linked pension plan: premiums buy units in a fund, and the corpus is converted into an annuity at vesting.",
        "tenure": "Policy term with a vesting age",
        "payout": "Annuity after vesting; commutation within the rules",
        "liquidity": "No surrender or withdrawal in the first five years. At vesting, benefits must be taken as an annuity except for the permitted commutation.",
        "elig": "Single or regular premium; policy term and vesting age within the limits in the brochure.",
        "protect": "No capital protection: the fund value moves with the market.",
        "risks": [
            "The corpus can fall before vesting.",
            "Most of the benefit must be converted to an annuity, at rates available then.",
            "Charges are deducted from the fund throughout.",
        ],
        "uses": ["Building a retirement corpus with market exposure", "A pension with a choice of funds"],
        "check": ["The charges and fund options", "The commutation limit at vesting"],
        "url": ULIP_PAGE,
        "brochure": "Lic LIC’s New Pension Plus  2024  4x9 inches wxh single pages[75] (1).pdf",
    },
    {
        "slug": "lic-gift-wealth-builder-plus",
        "name": "LIC's Gift Wealth Builder Plus",
        "uin": "IIULGC001V01202526",
        "type": "linked",
        "one": "A US-dollar unit-linked plan sold from LIC's GIFT City branch — premiums buy units in one of four funds, with life cover.",
        "tenure": "Policy term chosen at purchase",
        "payout": "Fund value at maturity",
        "liquidity": "Partial withdrawals after five years; no access before that.",
        "elig": "Indian residents, NRIs, foreign nationals and overseas residents, subject to the IFSCA rules.",
        "protect": "Life cover of 7x the annualised premium; the fund value is not guaranteed.",
        "risks": [
            "Currency risk on top of market risk — your returns are in dollars.",
            "The fund value can fall.",
            "Sold under IFSCA rules from GIFT City, which differ from a domestic policy.",
        ],
        "uses": ["Building a dollar-denominated corpus", "Wealth transfer for families with overseas links"],
        "check": ["The four funds and their mandates", "The IFSCA rules that apply, and how the policy is taxed"],
        "url": GIFT_PAGE,
        "brochure": "GiftCityProductImage.jpg",
    },
    {
        "slug": "lic-jeevan-amar",
        "name": "LIC's New Jeevan Amar",
        "uin": "512N350V02",
        "type": "term",
        "one": "A pure term plan: it pays your family if you die during the term and nothing if you survive it.",
        "tenure": "Policy term chosen at purchase",
        "payout": "Lump sum to the nominee on death",
        "liquidity": "No maturity value. The policy can lapse if premiums stop.",
        "elig": "Single, regular or limited premium. Smoker and non-smoker rates; special rates for women.",
        "protect": "Death benefit only — there is no investment component.",
        "risks": [
            "No money comes back if you survive the term.",
            "Stopping premiums lapses the cover, and revival has conditions.",
            "Cover ends at the end of the term, when renewal may cost much more.",
        ],
        "uses": ["Pure life cover at the lowest premium", "Protecting a family while loans are being repaid"],
        "check": ["Level or increasing sum assured — which suits your needs", "The smoker/non-smoker rate that applies to you"],
        "url": TERM_PAGE,
        "brochure": "LIC_Jeevan amar_Sales Brochure_4 inch x 9 inch_Eng (1).pdf",
    },
]


def build(plan: dict) -> dict:
    is_linked = plan["type"] == "linked"
    return_type = "market-linked" if is_linked else ("conditional" if plan["type"] == "term" else "guaranteed")
    return {
        "slug": plan["slug"],
        "name": plan["name"],
        "provider": "Life Insurance Corporation of India",
        "providerShort": "LIC",
        "providerType": "Insurer",
        "category": "lic-life-insurance",
        "returnType": return_type,
        "rateRef": {
            "label": "Premium set by LIC",
            "url": plan["url"],
            "note": PREMIUM_NOTE,
        },
        "demo": False,
        "oneLiner": plan["one"],
        "minInvestment": None,
        "minInvestmentNote": PREMIUM_NOTE,
        "tenure": plan["tenure"],
        "tenureMonths": None,
        "payout": plan["payout"],
        "payoutFrequency": "maturity",
        "liquidity": plan["liquidity"],
        "lockIn": "5 years (unit-linked)" if is_linked else None,
        "eligibility": plan["elig"],
        "tax": TAX_COMMON,
        "protection": plan["protect"],
        "riskLevel": "moderate" if is_linked else "low",
        "risks": plan["risks"],
        "commonUses": plan["uses"],
        "check": plan["check"],
        "collections": ["understand-before-you-invest"] if is_linked else ["government-backed"],
        "sources": [
            {"label": "LIC — plan details", "url": plan["url"]},
            {"label": "IRDAI — policyholder rights", "url": "https://www.irdai.gov.in"},
        ],
        "source": {
            "label": "LIC — plan brochure",
            "url": plan["url"],
            "note": f'Read from LIC\'s sales brochure "{plan["brochure"]}". Use LIC\'s calculator for a premium at your age.',
        },
        "uin": plan["uin"],
        "lastVerified": TODAY,
        "review": {
            "status": "approved",
            "reviewer": "Editorial review, 19 Oct 2026",
            "approvedAt": TODAY,
            "notes": f'Terms taken from LIC\u2019s own brochure. UIN {plan["uin"]}. No premium published: it depends on age, term and sum assured.',
        },
    }


def main() -> int:
    products = json.loads(PRODUCTS.read_text(encoding="utf-8"))
    existing = {p["slug"] for p in products}
    added = 0
    for plan in PLANS:
        record = build(plan)
        if record["slug"] in existing:
            continue
        products.append(record)
        added += 1
    products.sort(key=lambda p: (p["category"], p["name"]))
    PRODUCTS.write_text(json.dumps(products, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    counts = {}
    for p in products:
        counts[p["category"]] = counts.get(p["category"], 0) + 1
    print(f"added {added} LIC plans | totals: {counts} | all: {len(products)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
