"""Plan guide pages generated from one config per scheme.

Each scheme needs a rate, a term and a payout shape; everything else is shared
structure. Keeps five guides consistent instead of five hand-written layouts.
"""

from __future__ import annotations

import json

from .site import esc, icon

SCHEMES = [
    {
        "slug": "public-provident-fund",
        "tag": "Government scheme",
        "name": "Public Provident Fund",
        "rate_key": "ppf",
        "term": "15 years",
        "limits": "₹500 – ₹1.5 lakh a year",
        "payout": "Lump sum at maturity",
        "calc": "recurring",
        "calc_years": 15,
        "intro": "A fifteen-year government account that is tax-free at every stage. The default long-term savings "
                 "product for anyone without a specific goal.",
        "who": "Any resident individual, and a guardian on behalf of a minor. One account per person.",
        "how": [
            "Deposit between ₹500 and ₹1.5 lakh in a financial year; twelve deposits a year is the maximum.",
            "Interest is compounded annually and credited at the end of each year.",
            "The rate is notified every quarter, so the balance earns whatever rate is in force — it is not fixed "
            "for the whole term.",
            "After fifteen years you can close it, or extend in five-year blocks with or without further deposits.",
        ],
        "rules": [
            "A loan against the balance is available from the third financial year.",
            "Partial withdrawal is allowed from the sixth year, within limits and for specified purposes.",
            "The account does not lapse if you skip a year, but a year without the minimum gets no interest credit.",
            "It can be transferred between post offices and banks without closing it.",
        ],
        "tax": "Deposits qualify under 80C (old regime). Interest is not taxed as it accrues. Maturity is not taxed.",
        "compare": "Against SSY it pays less but is open to anyone. Against an FD the tax treatment is the whole "
                   "difference: an FD needs about 10.1% to match a tax-free 7.10%.",
        "compare_link": ("guides/ppf-vs-fd-vs-nsc.html", "PPF vs FD vs NSC"),
    },
    {
        "slug": "national-savings-certificate",
        "tag": "Government scheme",
        "name": "National Savings Certificate",
        "rate_key": "nsc",
        "term": "5 years",
        "limits": "₹1,000 minimum, no maximum",
        "payout": "Lump sum at maturity",
        "calc": "lumpsum",
        "calc_years": 5,
        "intro": "A five-year government certificate bought once and repaid at maturity. Interest accrues and is "
                 "paid with the principal, which is why it suits a lump sum rather than a monthly habit.",
        "who": "Any resident individual, singly or jointly, and a guardian for a minor. Also available to trusts "
               "and HUFs.",
        "how": [
            "You invest a lump sum at any post office and receive the accumulated amount after five years.",
            "Interest is compounded annually but paid at maturity, not along the way.",
            "The rate is notified quarterly for new purchases; once bought, your certificate carries its own rate.",
            "It can be pledged as security for a loan.",
        ],
        "rules": [
            "There is no early withdrawal — the money is locked for the full five years.",
            "A nominated person receives the proceeds on the holder's death.",
            "The certificate can be transferred between post offices.",
            "Interest accrued each year is treated as reinvested, which is why it also counts towards 80C.",
        ],
        "tax": "The investment qualifies under 80C. Interest is taxable at your slab each year as it accrues, even "
               "though you receive it at maturity.",
        "compare": "The rate looks better than PPF, but the interest is taxed. For a 30% slab taxpayer, PPF at "
                   "7.10% tax-free usually wins.",
        "compare_link": ("guides/ppf-vs-fd-vs-nsc.html", "PPF vs FD vs NSC"),
    },
    {
        "slug": "senior-citizens-savings-scheme",
        "tag": "Government scheme",
        "name": "Senior Citizens' Savings Scheme",
        "rate_key": "scss",
        "term": "5 years, extendable by 3",
        "limits": "₹1,000 – ₹30 lakh",
        "payout": "Quarterly interest, capital returned",
        "calc": "payout",
        "calc_years": 5,
        "calc_periods": 4,
        "intro": "Built for people over 60: a lump sum that pays interest every quarter and returns the capital at "
                 "the end. The highest rate among the schemes most retirees actually use.",
        "who": "Anyone aged 60 or above. Also available from 55 to 60 to those who retired on superannuation or "
               "under the VRS, subject to conditions.",
        "how": [
            "You deposit a lump sum and receive interest every quarter — the capital is not reduced.",
            "The deposit, plus the final quarter's interest, is repaid at maturity after five years.",
            "The account can be extended by three years at a time, with the rate in force at renewal.",
            "The maximum is ₹30 lakh per depositor, including any extension.",
        ],
        "rules": [
            "Premature closure is allowed after one year, with a penalty on the rate already paid.",
            "After the lock-in you can close without penalty for specified reasons such as medical treatment.",
            "Interest is credited to your savings account, not compounded inside the scheme.",
            "A joint account is allowed with a spouse.",
        ],
        "tax": "The deposit qualifies under 80C. The quarterly interest is taxable at your slab. TDS applies above "
               "the threshold.",
        "compare": "Against a five-year bank FD it usually pays more and is government-backed, but the age test is "
                   "the barrier — and the ₹30 lakh cap limits large corpora.",
        "compare_link": ("guides/scss-vs-fd.html", "SCSS vs bank FD"),
    },
    {
        "slug": "kisan-vikas-patra",
        "tag": "Government scheme",
        "name": "Kisan Vikas Patra",
        "rate_key": "kvp",
        "term": "About 115 months",
        "limits": "₹1,000 minimum, no maximum",
        "payout": "Lump sum at maturity",
        "calc": "lumpsum",
        "calc_years": 10,
        "intro": "A government certificate that doubles your money in a fixed period. No periodic payout, no "
                 "partial withdrawal — a single lump sum in, a single lump sum out.",
        "who": "Any resident individual, singly or jointly, and a guardian for a minor. Also trusts and "
               "institutions.",
        "how": [
            "You invest a lump sum and the certificate matures when the amount has doubled.",
            "At the notified rate, that takes about 115 months — roughly nine and a half years.",
            "The rate is notified quarterly, so the doubling period is set when you buy.",
            "It is available at post offices and can be transferred between them.",
        ],
        "rules": [
            "No partial withdrawal at any point.",
            "Premature encashment is allowed only after a specified lock-in, and at a lower rate.",
            "The certificate can be pledged as collateral for a loan.",
            "It can be held in joint names, which simplifies succession.",
        ],
        "tax": "There is no 80C benefit on the investment. The interest built into the maturity value is taxable at "
               "your slab.",
        "compare": "It looks attractive because it doubles — but the doubling takes about nine and a half years, "
                   "which is a lower annual rate than PPF at 7.10%, and it is taxed.",
        "compare_link": ("guides/small-savings-compared.html", "All schemes compared"),
    },
    {
        "slug": "post-office-monthly-income-scheme",
        "tag": "Government scheme",
        "name": "Post Office Monthly Income Scheme",
        "rate_key": "mis",
        "term": "5 years",
        "limits": "₹1,500 – ₹9 lakh (₹15 lakh joint)",
        "payout": "Monthly interest, capital returned",
        "calc": "payout",
        "calc_years": 5,
        "calc_periods": 12,
        "intro": "A lump sum that pays interest every month, with the capital returned at the end of five years. "
                 "The simplest monthly-income option at a post office.",
        "who": "Any resident individual, singly or jointly. A guardian may open one for a minor.",
        "how": [
            "You deposit a lump sum and receive the interest monthly — the capital stays intact.",
            "The deposit is repaid at the end of five years.",
            "The maximum is ₹9 lakh in a single account and ₹15 lakh in a joint account.",
            "The interest is credited to your savings account each month.",
        ],
        "rules": [
            "Premature closure is allowed after one year, with a deduction on the amount.",
            "Close in the first year and you get no interest, only the deposit back.",
            "Interest is not compounded inside the scheme — you receive it.",
            "A joint account can be held with a spouse or a blood relative.",
        ],
        "tax": "The deposit does not qualify under 80C. The monthly interest is taxable at your slab, and TDS can "
               "apply.",
        "compare": "Against SCSS it is available at any age, but pays less. Against a bank FD it is government-"
                   "backed, which matters above the ₹5 lakh DICGC limit.",
        "compare_link": ("guides/scss-vs-fd.html", "SCSS vs bank FD"),
    },
]


def _facts(scheme: dict, rate: str, as_of: str) -> str:
    rows = [
        ("Rate", rate),
        ("Term", scheme["term"]),
        ("Limits", scheme["limits"]),
        ("Payout", scheme["payout"]),
    ]
    inner = "".join(
        f'<div class="ssy-fact"><span>{esc(label)}</span><strong>{esc(value)}</strong></div>'
        for label, value in rows
    )
    return f'<div class="ssy-facts">{inner}</div>'


def page(scheme: dict, rates: dict) -> str:
    entry = rates.get(scheme["rate_key"]) or {}
    rate = entry.get("value", "—")
    as_of = entry.get("asOf", "—")
    rate_number = rate.replace("%", "").strip()

    calc = scheme["calc"]
    if calc == "recurring":
        amount_label = "Amount deposited each year"
        amount_placeholder = "e.g. 150000"
    else:
        amount_label = "Amount you deposit"
        amount_placeholder = "e.g. 100000"

    periods = scheme.get("calc_periods")
    config = json.dumps({"type": calc, "periods": periods, "term": scheme["calc_years"]})

    how = "".join(f"<li>{icon('check', 'icon icon-sm')}<span>{esc(item)}</span></li>" for item in scheme["how"])
    rules = "".join(f"<li>{icon('alert', 'icon icon-sm')}<span>{esc(item)}</span></li>" for item in scheme["rules"])
    link_href, link_label = scheme["compare_link"]

    return f"""
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="../index.html">Home</a></li><li><a href="../plans.html">Plans</a></li>
      <li aria-current="page">{esc(scheme['name'])}</li>
    </ol></nav>
    <h1>{esc(scheme['name'])}</h1>
    <p class="page-lede">{esc(scheme['intro'])}</p>
    <p class="page-meta">Rate {esc(rate)} · notified for the quarter beginning {esc(as_of)}</p>
  </div>
</section>

<section class="section">
  <div class="shell">{_facts(scheme, rate, as_of)}</div>
</section>

<section class="section section-tint" id="calculator">
  <div class="shell calc-layout">
    <form class="calc-form" id="plan-form">
      <fieldset class="calc-group">
        <legend>Work out the numbers</legend>
        <div class="calc-grid">
          <label class="field">
            <span class="field-label">{esc(amount_label)}</span>
            <span class="field-input"><input id="plan-amount" type="number" min="0" step="500" placeholder="{esc(amount_placeholder)}"><span class="field-suffix">₹</span></span>
          </label>
          <label class="field">
            <span class="field-label">Rate</span>
            <span class="field-input"><input id="plan-rate" type="number" min="0.5" max="20" step="0.05" value="{esc(rate_number)}"><span class="field-suffix">% a year</span></span>
          </label>
          <label class="field">
            <span class="field-label">Years</span>
            <span class="field-input"><input id="plan-years" type="number" min="1" max="30" value="{scheme['calc_years']}"><span class="field-suffix">years</span></span>
          </label>
        </div>
        <p class="field-hint">The rate is notified quarterly. Change it to see what a revision would do.</p>
      </fieldset>
      <div class="calc-actions">
        <button class="btn btn-primary" type="submit">Calculate</button>
        <button class="btn btn-ghost" type="reset" id="plan-reset">Reset</button>
      </div>
    </form>

    <aside class="calc-results">
      <div id="plan-output"><p class="calc-empty-text">Enter an amount to see the projection.</p></div>
    </aside>
  </div>
</section>

<section class="section">
  <div class="shell shell-narrow">
    <h2 class="guide-h2">Who can open one</h2>
    <p class="guide-p">{esc(scheme['who'])}</p>

    <h2 class="guide-h2">How the money works</h2>
    <ul class="check-list">{how}</ul>

    <h2 class="guide-h2">Rules worth knowing</h2>
    <ul class="check-list">{rules}</ul>

    <h2 class="guide-h2">Tax</h2>
    <p class="guide-p">{esc(scheme['tax'])}</p>

    <h2 class="guide-h2">How it compares</h2>
    <p class="guide-p">{esc(scheme['compare'])}</p>
    <p class="guide-cta">
      <a class="btn btn-ghost" href="../{esc(link_href)}">{esc(link_label)}</a>
      <a class="btn btn-ghost" href="../categories/government-schemes.html">All small-savings schemes</a>
    </p>

    <p class="guide-src">
      Rate {esc(rate)}, notified for the quarter beginning {esc(as_of)} —
      <a href="https://www.nsiindia.gov.in" target="_blank" rel="noopener noreferrer">National Savings Institute</a>.
      Scheme rules are published by India Post and the Ministry of Finance. Confirm at your post office before acting.
    </p>
  </div>
</section>

<script type="application/json" id="plan-config">{config}</script>
<script src="../assets/js/plan-calc.js" defer></script>
"""
