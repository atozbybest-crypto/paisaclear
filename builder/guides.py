"""Comparison guides built from data the site already holds."""

from __future__ import annotations

from .site import esc, icon


def _rate(rates: dict, key: str) -> str:
    entry = rates.get(key) or {}
    return entry.get("value", "—")


def _asof(rates: dict, key: str) -> str:
    entry = rates.get(key) or {}
    return entry.get("asOf", "—")


def _head(title: str, lede: str, meta: str) -> str:
    return f"""
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="../index.html">Home</a></li><li><a href="../start.html">Start here</a></li>
      <li aria-current="page">{esc(title)}</li>
    </ol></nav>
    <h1>{esc(title)}</h1>
    <p class="page-lede">{lede}</p>
    <p class="page-meta">{esc(meta)}</p>
  </div>
</section>"""


def _compare_table(headers: list[str], rows: list[list[str]]) -> str:
    head = "".join(f"<th scope=\"col\">{esc(h)}</th>" for h in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows
    )
    return (
        '<div class="cmp-wrap"><table class="cmp-table">'
        f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>"
    )


def ppf_vs_fd_vs_nsc(ctx: dict, rates: dict) -> str:
    ppf, nsc = _rate(rates, "ppf"), _rate(rates, "nsc")
    asof = _asof(rates, "ppf")
    return _head(
        "PPF vs FD vs NSC",
        "Three safe places for long-term money, and they are not interchangeable. What each promises, how long it locks the money, and how it is taxed.",
        "Official rates as of " + asof,
    ) + f"""
<section class="section">
  <div class="shell shell-narrow">
    {_compare_table(
        ["", "PPF", "Bank FD", "NSC"],
        [
            ["<strong>Rate</strong>", f"<strong>{esc(ppf)}</strong> a year, notified quarterly", "Set by each bank, varies by tenure", f"<strong>{esc(nsc)}</strong> a year, notified quarterly"],
            ["<strong>Who pays</strong>", "Government of India", "The bank, insured up to the DICGC limit", "Government of India"],
            ["<strong>Term</strong>", "15 years, extendable in 5-year blocks", "7 days to 10 years, typically", "5 years"],
            ["<strong>Access</strong>", "Partial withdrawal after 5 years, with conditions", "Breakable any time, usually at a penalty", "Locked for 5 years"],
            ["<strong>Tax on interest</strong>", "Tax-free", "Taxed at your slab every year", "Taxed at your slab every year"],
            ["<strong>Section 80C</strong>", "Yes", "Only the 5-year tax-saver FD", "Yes"],
            ["<strong>Best fit</strong>", "Retirement, long compounding", "Money needed at a known date", "A 5-year block with 80C"],
        ],
    )}

    <h2 class="guide-h2">The tax difference is bigger than the rate difference</h2>
    <p class="guide-p">
      PPF interest is exempt at all three stages — you get a deduction on what you put in, the interest is not
      taxed as it builds, and the maturity amount is not taxed. An FD paying a higher headline rate can still
      leave you with less, because its interest is taxed at your slab every year.
    </p>
    <p class="guide-p">
      At a 30% slab, an FD needs to pay roughly 10.1% to match a 7.10% tax-free PPF. No bank FD currently
      pays that. For anyone in the 20% or 30% bracket, PPF wins on after-tax return unless the money must stay
      reachable.
    </p>

    <h2 class="guide-h2">When an FD is the right answer anyway</h2>
    <ul class="check-list">
      <li>{icon("check", "icon icon-sm")}<span>You need the money in two or three years. PPF's 15-year term and 5-year lock make it unsuitable for that.</span></li>
      <li>{icon("check", "icon icon-sm")}<span>You want a fixed rate for a known period. PPF's rate is re-notified every quarter.</span></li>
      <li>{icon("check", "icon icon-sm")}<span>You are in a low tax bracket, where the tax drag is small.</span></li>
    </ul>

    <h2 class="guide-h2">What NSC adds</h2>
    <p class="guide-p">
      NSC sits between the two: a government-backed 5-year certificate at {esc(nsc)}, with 80C on the
      investment, but the interest is taxable. It suits someone who wants a five-year block and has 80C room
      left after PPF.
    </p>

    <p class="guide-src">
      Rates: {esc(ppf)} for PPF and {esc(nsc)} for NSC, notified for the quarter beginning {esc(asof)} —
      <a href="https://www.nsiindia.gov.in" target="_blank" rel="noopener noreferrer">National Savings Institute</a>.
      Bank FD rates vary by bank and tenure, so each bank's record links to its own rate card.
    </p>
    <p class="guide-cta">
      <a class="btn btn-primary" href="../products/public-provident-fund.html">PPF details</a>
      <a class="btn btn-ghost" href="../products/national-savings-certificate.html">NSC details</a>
    </p>
  </div>
</section>"""


def sip_vs_lump_sum(ctx: dict, rates: dict) -> str:
    return _head(
        "SIP vs lump sum",
        "Same fund, same money, very different experience. What each does to your risk, and which one suits which situation.",
        "Illustrative arithmetic · no return is forecast",
    ) + """
<section class="section">
  <div class="shell shell-narrow">
    """ + _compare_table(
        ["", "SIP", "Lump sum"],
        [
            ["<strong>How it works</strong>", "A fixed amount invested every month", "Everything invested on one day"],
            ["<strong>Price paid</strong>", "Averages out — some units bought high, some low", "One price, on one day"],
            ["<strong>Timing risk</strong>", "Spread over months", "Concentrated on the day you invest"],
            ["<strong>Cash needed</strong>", "A monthly commitment", "The full amount upfront"],
            ["<strong>Suits</strong>", "Salary income, building a habit", "A bonus, maturity or inheritance"],
            ["<strong>Risk of stopping</strong>", "SIPs get paused when money is tight", "None — the money is already in"],
        ],
    ) + """

    <h2 class="guide-h2">The arithmetic, with assumptions stated</h2>
    <p class="guide-p">
      ₹10,000 a month for 10 years at a constant 12% a year grows to about <strong>₹23.2 lakh</strong>, on
      ₹12 lakh invested. A single ₹1 lakh invested at the same 12% for 10 years becomes about
      <strong>₹3.1 lakh</strong>.
    </p>
    <p class="guide-p">
      Those are arithmetic results, not forecasts. No fund returns 12% every year, and the order of returns
      matters: a lump sum invested just before a 30% fall takes years to recover, while a SIP keeps buying
      through it.
    </p>

    <h2 class="guide-h2">What actually decides it</h2>
    <ul class="check-list">
      <li>""" + icon("check", "icon icon-sm") + """<span><strong>Do you have the money now, or does it arrive monthly?</strong> Most people do not have a lump sum to invest — the question answers itself.</span></li>
      <li>""" + icon("check", "icon icon-sm") + """<span><strong>How long until you need it?</strong> Under three years, neither structure fixes the real risk, which is equity itself.</span></li>
      <li>""" + icon("check", "icon icon-sm") + """<span><strong>Would you panic and redeem?</strong> A lump sum that falls 25% in month two tests that harder than a SIP.</span></li>
      <li>""" + icon("check", "icon icon-sm") + """<span><strong>Lump sum in a falling market</strong> is the case for staggering — spreading the entry over 6–12 months, which is a SIP with a fixed number of instalments.</span></li>
    </ul>

    <p class="guide-src">
      Run the numbers on your own figures in the
      <a href="../calculators/savings.html">savings calculator</a> — it shows the monthly-investing and
      one-time routes side by side, including the value in today's money.
    </p>
    <p class="guide-cta">
      <a class="btn btn-primary" href="../calculators/savings.html">Open the calculator</a>
      <a class="btn btn-ghost" href="../categories/mutual-funds.html">Mutual funds</a>
    </p>
  </div>
</section>"""


def old_vs_new_regime(ctx: dict, rates: dict, rules: dict) -> str:
    new = rules["regimes"]["new"]
    old = rules["regimes"]["old"]

    def slabs(regime: dict) -> str:
        rows, previous = [], 0
        for slab in regime["slabs"]:
            ceiling = slab["upTo"]
            label = (
                f"Above ₹{previous:,}" if ceiling is None
                else f"₹{previous:,} – ₹{ceiling:,}"
            )
            rows.append([label, f"{slab['rate'] * 100:.0f}%"])
            previous = ceiling if ceiling is not None else previous
        return _compare_table(["Income slice", "Rate"], rows)

    return _head(
        "Old vs new tax regime",
        "The new regime is the default and has lower slabs, but almost no deductions. Here is the trade-off, with the numbers behind it.",
        "Rules as of FY " + rules["financialYear"],
    ) + f"""
<section class="section">
  <div class="shell shell-narrow">
    <h2 class="guide-h2">The two slab tables</h2>
    <div class="guide-split">
      <div>
        <p class="guide-label">New regime — the default</p>
        {slabs(new)}
        <p class="guide-note">Standard deduction ₹{new['standardDeduction']:,} · rebate up to ₹{new['rebate']['maxRebate']:,} makes taxable income up to ₹{new['rebate']['taxableLimit']:,} tax-free</p>
      </div>
      <div>
        <p class="guide-label">Old regime — you must opt in</p>
        {slabs(old)}
        <p class="guide-note">Standard deduction ₹{old['standardDeduction']:,} · rebate up to ₹{old['rebate']['maxRebate']:,} up to ₹{old['rebate']['taxableLimit']:,}</p>
      </div>
    </div>

    <h2 class="guide-h2">A worked example</h2>
    <p class="guide-p">
      Take a ₹15,00,000 salary. Under the new regime, taxable income after the ₹75,000 standard deduction is
      ₹14,25,000, and the tax comes to about <strong>₹97,500</strong> including cess.
    </p>
    <p class="guide-p">
      Under the old regime the same salary needs deductions to compete. With ₹1.5 lakh of 80C, ₹1.5 lakh of
      HRA exemption, ₹25,000 of 80D and ₹25,000 of home-loan interest — ₹3.5 lakh in total — taxable income
      falls to ₹11,00,000 and the tax is about <strong>₹1,48,200</strong>. The new regime is still ahead by
      roughly ₹50,000.
    </p>
    <p class="guide-p">
      The old regime only pulls ahead when the deductions are large: a big HRA claim in a metro city, a large
      home loan, and the full 80C. For most salaried people without those, the new regime wins despite the
      higher-sounding deductions.
    </p>

    <h2 class="guide-h2">What the old regime still allows</h2>
    <ul class="check-list">
      <li>""" + icon("check", "icon icon-sm") + """<span>HRA exemption, if you pay rent — usually the biggest single item</span></li>
      <li>""" + icon("check", "icon icon-sm") + """<span>80C up to ₹1.5 lakh: PPF, ELSS, life insurance, principal on a home loan</span></li>
      <li>""" + icon("check", "icon icon-sm") + """<span>80D health insurance, 24(b) home-loan interest, 80E education-loan interest</span></li>
      <li>""" + icon("check", "icon icon-sm") + """<span>80CCD(1B) — an extra ₹50,000 for NPS, still available under the new regime too</span></li>
    </ul>

    <p class="guide-src">
      The <a href="../calculators/salary.html">salary calculator</a> does this comparison on your actual
      numbers, including HRA, 80C, 80D and home-loan interest.
    </p>
    <p class="guide-cta">
      <a class="btn btn-primary" href="../calculators/salary.html">Compare on your salary</a>
      <a class="btn btn-ghost" href="../calculators/savings.html">Savings calculator</a>
    </p>
  </div>
</section>"""


def small_savings_compared(ctx: dict, rates: dict) -> str:
    rows_data = [
        ("Public Provident Fund", "ppf", "15 years", "₹500 – ₹1.5 lakh", "Tax-free", "Partial after 5 years"),
        ("Sukanya Samriddhi Yojana", "ssy", "21 years", "₹250 – ₹1.5 lakh", "Tax-free", "On maturity / rules"),
        ("Senior Citizens' Savings", "scss", "5 years", "₹1,000 – ₹30 lakh", "Taxed; 80C", "Quarterly payout"),
        ("National Savings Certificate", "nsc", "5 years", "₹1,000+", "Taxed; 80C", "Locked 5 years"),
        ("Kisan Vikas Patra", "kvp", "~115 months", "₹1,000+", "Taxed", "Locked"),
        ("Post Office MIS", "mis", "5 years", "₹1,500 – ₹9 lakh", "Taxed", "Monthly payout"),
        ("Post Office Time Deposit (5y)", "po-td-5y", "5 years", "₹1,000+", "Taxed; 80C on 5y", "Locked, penalty on exit"),
        ("Post Office Savings", "po-savings", "None", "₹500+", "Taxed", "Any time"),
    ]
    rows = [
        [f"<strong>{esc(name)}</strong>", f"<strong>{esc(_rate(rates, key))}</strong>", term, limit, tax, access]
        for name, key, term, limit, tax, access in rows_data
    ]

    return _head(
        "Small savings schemes compared",
        "Nine government-backed schemes, one table. The notified rate, the term, the limits and what each one costs you in tax.",
        "Rates notified for the quarter beginning " + _asof(rates, "ppf"),
    ) + f"""
<section class="section">
  <div class="shell">
    {_compare_table(["Scheme", "Rate", "Term", "Limits", "Tax", "Access"], rows)}

    <div class="guide-body">
      <h2 class="guide-h2">How to read this table</h2>
      <p class="guide-p">
        Every rate here is notified by the government and revised every quarter, unlike a bank FD rate which
        the bank sets itself. A scheme's rate can change after you open it — new contributions earn the rate in
        force at the time, while PPF balances earn the rate as revised.
      </p>
      <p class="guide-p">
        The tax column is where these diverge sharply. PPF and SSY are exempt at all three stages. SCSS, NSC,
        KVP, MIS and the time deposits are taxable at your slab, with 80C available on some.
      </p>

      <h2 class="guide-h2">Which one for which purpose</h2>
      <ul class="check-list">
        <li>{icon("check", "icon icon-sm")}<span><strong>Long-term, tax-free:</strong> PPF for anyone, SSY for a daughter under 10.</span></li>
        <li>{icon("check", "icon icon-sm")}<span><strong>Regular income:</strong> SCSS pays quarterly and is built for people over 60; MIS pays monthly for anyone.</span></li>
        <li>{icon("check", "icon icon-sm")}<span><strong>A fixed five-year block:</strong> NSC, with 80C on the way in.</span></li>
        <li>{icon("check", "icon icon-sm")}<span><strong>Everyday cash:</strong> the Post Office savings account, at {esc(_rate(rates, "po-savings"))}.</span></li>
      </ul>

      <p class="guide-src">
        Rates as of {esc(_asof(rates, "ppf"))}. Source:
        <a href="https://www.nsiindia.gov.in" target="_blank" rel="noopener noreferrer">National Savings Institute</a>.
        Each scheme page carries its own dated figure and source link.
      </p>
      <p class="guide-cta">
        <a class="btn btn-primary" href="../categories/government-schemes.html">All 17 schemes</a>
        <a class="btn btn-ghost" href="ppf-vs-fd-vs-nsc.html">PPF vs FD vs NSC</a>
      </p>
    </div>
  </div>
</section>"""
