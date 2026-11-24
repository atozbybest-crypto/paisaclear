#!/usr/bin/env python3
"""Build the AskPaisa index — every answerable thing on the site, in one JSON.

The assistant can only answer from this file, which is generated from the site's
own content. Nothing outside the site is reachable.

    python tools/build_askpaisa.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
OUT = ROOT / "site" / "assets" / "data" / "askpaisa.json"


def load(name: str):
    path = CONTENT / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def clean(text: str, limit: int = 220) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]


def main() -> int:
    entries: list[dict] = []

    # --- products
    products = load("products.json") or []
    categories = {c["id"]: c for c in (load("categories.json") or [])}
    for p in products:
        cat = categories.get(p["category"], {})
        entries.append({
            "t": p["name"],
            "u": f"products/{p['slug']}.html",
            "k": cat.get("name", "Product"),
            "s": clean(p.get("oneLiner", "")),
            "w": " ".join(filter(None, [
                p["name"], p.get("provider", ""), cat.get("name", ""), cat.get("short", ""),
                p.get("returnType", ""), p.get("riskLevel", ""), p.get("sector", ""),
                p.get("providerShort", ""), p.get("plan", ""),
            ])),
        })

    # --- plan guides
    for slug, title, line in (
        ("plans/sukanya-samriddhi", "Sukanya Samriddhi Yojana", "Who can open it, deposit rules, withdrawal and a 21-year calculator."),
        ("plans/public-provident-fund", "Public Provident Fund", "Fifteen-year tax-free account with a calculator."),
        ("plans/national-savings-certificate", "National Savings Certificate", "Five-year certificate, interest paid at maturity."),
        ("plans/senior-citizens-savings-scheme", "Senior Citizens' Savings Scheme", "Quarterly income for those over 60."),
        ("plans/kisan-vikas-patra", "Kisan Vikas Patra", "Money doubles in about 115 months."),
        ("plans/post-office-monthly-income-scheme", "Post Office Monthly Income Scheme", "Monthly interest with capital returned."),
        ("plans/beti-bachao-beti-padhao", "Beti Bachao Beti Padhao", "A campaign, not a savings scheme."),
    ):
        entries.append({"t": title, "u": slug + ".html", "k": "Plan guide", "s": line,
                        "w": title + " plan scheme yojana calculator"})

    # --- calculators
    for slug, title, line in (
        ("calculators/savings", "Savings calculator", "Work out what a deposit becomes over time."),
        ("calculators/loan", "Loan EMI calculator", "Monthly payment and total interest on a loan."),
        ("calculators/income-tax", "Income tax calculator", "Old and new regime for individuals, HUF, firms and companies."),
        ("calculators/salary", "Salary calculator", "Take-home pay from CTC."),
        ("calculators/planning", "Goal calculator", "What to save each month for a target."),
        ("calculators/spending", "Spending planner", "Where the money goes each month."),
    ):
        entries.append({"t": title, "u": slug + ".html", "k": "Calculator", "s": line,
                        "w": title + " calculator calculate emi tax salary goal budget"})

    # --- articles
    for slug, title, line in (
        ("health-insurance-policy-clauses", "How to read a health insurance policy", "The five clauses that decide your claim."),
        ("ppf-vs-fd-vs-nsc-tax", "PPF vs FD vs NSC: the tax arithmetic", "After-tax returns and a worked example."),
        ("dividend-streak", "What a dividend streak predicts", "A long record is a habit, not a forecast."),
        ("scss-vs-fd", "SCSS vs a fixed deposit", "When the senior scheme beats a deposit."),
        ("health-insurance-after-60", "Health insurance for parents after 60", "Co-payment, waiting periods and renewal."),
        ("small-savings-rates", "Why small-savings rates change quarterly", "How the government sets PPF and SSY rates."),
        ("emergency-fund", "The emergency fund", "How much, and where to keep it in India."),
        ("us-investing-from-india", "Buying US stocks from India", "LRS, TCS, withholding tax and the estate-tax trap."),
    ):
        entries.append({"t": title, "u": slug + ".html", "k": "Article", "s": line,
                        "w": title + " article guide explainer"})

    # --- sections
    for slug, title, line in (
        ("browse.html", "All products", "Every Indian product on the site, with filters."),
        ("compare.html", "Compare products", "Put two or three products side by side."),
        ("rates.html", "Rates", "Every published rate with the date it applied."),
        ("paisadiscover.html", "PaisaDiscover", "Answer five questions and see which products fit."),
        ("answers.html", "Answers", "Common questions about Indian financial products."),
        ("check.html", "Scam checker", "Paste a message and see the red flags."),
        ("market-game.html", "Market game", "A simulated market with fake money."),
        ("articles.html", "Articles", "Long-form guides."),
        ("plans.html", "Plans", "Government scheme guides."),
        ("us-funds.html", "US funds and ETFs", "Sixty-two US funds across ten categories."),
        ("us-compare.html", "Compare US funds", "All US funds in one table."),
        ("gold-price.html", "Gold price", "Gold per 10 grams, the dollar price and the NSE gold ETF, with history."),
        ("us-market.html", "US market", "Indices, Treasury yields and deposit rates."),
        ("news.html", "Money news", "Headlines from Indian finance publishers."),
        ("about-editor.html", "About the editor", "Who writes PaisaClear."),
        ("how-we-work.html", "How we work", "How figures are checked and dated."),
    ):
        entries.append({"t": title, "u": slug, "k": "Section", "s": line, "w": title + " page section"})

    # category hubs
    for c in (load("categories.json") or []):
        entries.append({
            "t": c["name"], "u": f"categories/{c['slug']}.html", "k": "Category",
            "s": clean(c.get("blurb") or c.get("tagline", "")),
            "w": f"{c['name']} {c.get('short','')} category list",
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(entries, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"askpaisa index: {len(entries)} entries, {OUT.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
