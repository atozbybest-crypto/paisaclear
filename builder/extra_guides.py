"""Live rates hub plus four more comparison pages."""

from __future__ import annotations

from .site import esc, icon


def _r(rates: dict, key: str) -> str:
    return (rates.get(key) or {}).get("value", "—")


def _d(rates: dict, key: str) -> str:
    return (rates.get(key) or {}).get("asOf", "—")


def _head(title: str, lede: str, meta: str, base: str = "../") -> str:
    return f"""
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="{base}index.html">Home</a></li><li><a href="{base}start.html">Start here</a></li>
      <li aria-current="page">{esc(title)}</li>
    </ol></nav>
    <h1>{esc(title)}</h1>
    <p class="page-lede">{lede}</p>
    <p class="page-meta">{esc(meta)}</p>
  </div>
</section>"""


def _table(headers: list[str], rows: list[list[str]]) -> str:
    head = "".join(f'<th scope="col">{esc(h)}</th>' for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f'<div class="cmp-wrap"><table class="cmp-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def rates_hub(rates: dict) -> str:
    small = [
        ("Public Provident Fund", "ppf", "15 years", "Tax-free"),
        ("Sukanya Samriddhi Yojana", "ssy", "21 years", "Tax-free"),
        ("Senior Citizens' Savings Scheme", "scss", "5 years", "Taxed, 80C"),
        ("National Savings Certificate", "nsc", "5 years", "Taxed, 80C"),
        ("Kisan Vikas Patra", "kvp", "~115 months", "Taxed"),
        ("Post Office Monthly Income", "mis", "5 years", "Taxed"),
        ("Post Office Time Deposit (5 years)", "po-td-5y", "5 years", "Taxed, 80C"),
        ("Post Office Time Deposit (3 years)", "po-td-3y", "3 years", "Taxed"),
        ("Post Office Savings Account", "po-savings", "None", "Taxed"),
    ]
    small_rows = [
        [f"<strong>{esc(name)}</strong>", f"<strong>{esc(_r(rates, key))}</strong>", term, tax]
        for name, key, term, tax in small
    ]

    gsecs = [
        ("6.20% Government Security 2029", "gs-2029"),
        ("6.36% Government Security 2031", "gs-2031"),
        ("6.94% Government Security 2036", "gs-2036"),
        ("7.06% Government Security 2041", "gs-2041"),
        ("7.63% Government Security 2056", "gs-2056"),
    ]
    gsec_rows = [
        [f"<strong>{esc(name)}</strong>", f"<strong>{esc(_r(rates, key))}</strong>", esc(_d(rates, key))]
        for name, key in gsecs
    ]

    tbills = [
        ("91-Day Treasury Bill", "tbill-91"),
        ("182-Day Treasury Bill", "tbill-182"),
        ("364-Day Treasury Bill", "tbill-364"),
    ]
    tbill_rows = [
        [f"<strong>{esc(name)}</strong>", f"<strong>{esc(_r(rates, key))}</strong>", esc(_d(rates, key))]
        for name, key in tbills
    ]

    asof = _d(rates, "ppf")

    return _head(
        "Today's rates, in one place",
        "Every rate this site tracks, with the date it applied. Small savings are notified quarterly; "
        "bond yields move daily.",
        "Small savings as of " + asof + " · bond yields refresh daily",
        base="",
    ) + f"""
<section class="section">
  <div class="shell">
    <h2 class="guide-h2" id="small-savings">Small savings</h2>
    {_table(["Scheme", "Rate", "Term", "Tax"], small_rows)}

    <h2 class="guide-h2" id="bonds">Government bonds — market yield</h2>
    {_table(["Security", "Yield", "As of"], gsec_rows)}

    <h2 class="guide-h2" id="t-bills">Treasury bills — cut-off yield</h2>
    {_table(["Bill", "Yield", "As of"], tbill_rows)}

    <p class="guide-src">
      Small-savings rates come from the National Savings Institute and change every quarter; bond yields
      from the RBI. Each product page carries its own dated figure and a link to the source.
    </p>
    <p class="guide-cta">
      <a class="btn btn-primary" href="categories/government-schemes.html">All small-savings schemes</a>
      <a class="btn btn-ghost" href="guides/small-savings-compared.html">Compare them</a>
    </p>
  </div>
</section>"""


def ssy_vs_ppf(rates: dict) -> str:
    return _head(
        "SSY vs PPF",
        "Both are tax-free and government-backed. They differ in who can open one, and in how long the money stays.",
        "Rates as of " + _d(rates, "ppf"),
    ) + f"""
<section class="section">
  <div class="shell shell-narrow">
    {_table(["", "Sukanya Samriddhi", "PPF"], [
        ["<strong>Rate</strong>", f"<strong>{esc(_r(rates, 'ssy'))}</strong>", f"<strong>{esc(_r(rates, 'ppf'))}</strong>"],
        ["<strong>Who</strong>", "A daughter under 10, opened by a parent or guardian", "Any resident individual"],
        ["<strong>Term</strong>", "21 years from opening", "15 years, extendable in 5-year blocks"],
        ["<strong>Yearly limit</strong>", "₹250 to ₹1.5 lakh", "₹500 to ₹1.5 lakh"],
        ["<strong>Tax</strong>", "Exempt at all three stages", "Exempt at all three stages"],
        ["<strong>Access</strong>", "Restricted; rules for marriage and education", "Partial withdrawal from year 6"],
    ])}
    <p class="guide-p">
      SSY pays {esc(_r(rates, 'ssy'))} against PPF's {esc(_r(rates, 'ppf'))}, and the higher rate is the
      entire reason it exists — a long horizon with no early access. If you have a daughter under ten, SSY is
      usually the better home for that money.
    </p>
    <p class="guide-p">
      If you do not, the question is moot. PPF is available to anyone, and the 15-year term is the trade-off
      you accept for tax-free compounding.
    </p>
    <p class="guide-src">Source: National Savings Institute, quarter beginning {esc(_d(rates, "ppf"))}.</p>
    <p class="guide-cta">
      <a class="btn btn-primary" href="../products/sukanya-samriddhi-yojana.html">SSY details</a>
      <a class="btn btn-ghost" href="../products/public-provident-fund.html">PPF details</a>
    </p>
  </div>
</section>"""


def scss_vs_fd(rates: dict) -> str:
    return _head(
        "SCSS vs bank FD",
        "Both pay a fixed rate. One is for people over 60 and pays quarterly; the other is open to anyone and is insured up to ₹5 lakh.",
        "SCSS rate as of " + _d(rates, "scss"),
    ) + f"""
<section class="section">
  <div class="shell shell-narrow">
    {_table(["", "Senior Citizens' Savings Scheme", "Bank FD"], [
        ["<strong>Rate</strong>", f"<strong>{esc(_r(rates, 'scss'))}</strong> quarterly payout", "Set by each bank, varies by tenure"],
        ["<strong>Who</strong>", "60+, or 55+ for specified retirees", "Any resident individual"],
        ["<strong>Term</strong>", "5 years, extendable by 3", "7 days to 10 years"],
        ["<strong>Safety</strong>", "Government of India", "Bank, insured to ₹5 lakh by DICGC"],
        ["<strong>Tax</strong>", "Interest taxed; 80C on the deposit", "Interest taxed; 80C only on 5-year tax-saver"],
        ["<strong>Access</strong>", "Premature closure with rules", "Breakable with a rate penalty"],
    ])}
    <p class="guide-p">
      SCSS pays quarterly, which is what most retirees actually need, and at {esc(_r(rates, 'scss'))} it usually
      beats a comparable five-year FD. Its limits are the age test and the ₹30 lakh cap.
    </p>
    <p class="guide-p">
      An FD is the flexible option: no age limit, any tenure, and ₹5 lakh of insurance if the bank fails. If you
      are under 60, it is the only one of the two you can open.
    </p>
    <p class="guide-src">SCSS rate from the National Savings Institute, quarter beginning {esc(_d(rates, "scss"))}. FD rates vary by bank and are linked, not published, on this site.</p>
    <p class="guide-cta">
      <a class="btn btn-primary" href="../products/senior-citizens-savings-scheme.html">SCSS details</a>
      <a class="btn btn-ghost" href="../categories/bank-deposits.html">Bank deposits</a>
    </p>
  </div>
</section>"""


def sip_vs_fd(rates: dict) -> str:
    return _head(
        "SIP vs FD",
        "One promises a number and cannot fall. The other promises nothing and can. Choosing between them is a question about time, not about which is better.",
        "Illustrative arithmetic · no return is forecast",
    ) + f"""
<section class="section">
  <div class="shell shell-narrow">
    {_table(["", "SIP into an equity fund", "Bank FD"], [
        ["<strong>Return</strong>", "None promised; moves with the market", "Fixed by contract for the term"],
        ["<strong>Can it fall?</strong>", "Yes — 20-40% falls are normal", "No, unless the bank fails"],
        ["<strong>Liquidity</strong>", "Redeem any business day, exit load may apply", "Breakable with a penalty"],
        ["<strong>Tax</strong>", "Equity rates by holding period", "Interest taxed at your slab every year"],
        ["<strong>Suits</strong>", "7+ years, money you will not touch", "Money needed at a known date"],
    ])}
    <p class="guide-p">
      A SIP of ₹10,000 a month for ten years at a constant 12% reaches about ₹23 lakh on ₹12 lakh invested. An
      FD at 7% over the same decade roughly doubles your money and is taxed along the way. Those figures are
      arithmetic on assumptions, and the fund's 12% is not guaranteed for a single year of it.
    </p>
    <p class="guide-p">
      The honest split: money you need in under three years belongs in a deposit. Money you can leave alone for
      a decade is the only money that should see equity at all.
    </p>
    <p class="guide-src">Run both paths on the <a href="../calculators/savings.html">savings calculator</a>.</p>
    <p class="guide-cta">
      <a class="btn btn-primary" href="../calculators/savings.html">Compare the numbers</a>
      <a class="btn btn-ghost" href="../categories/mutual-funds.html">Mutual funds</a>
    </p>
  </div>
</section>"""


def nps_vs_ppf(rates: dict) -> str:
    return _head(
        "NPS vs PPF",
        "PPF is a guaranteed, tax-free account. NPS is a market-linked pension with a lock-in until 60. They are not substitutes.",
        "PPF rate as of " + _d(rates, "ppf"),
    ) + f"""
<section class="section">
  <div class="shell shell-narrow">
    {_table(["", "National Pension System", "PPF"], [
        ["<strong>Return</strong>", "Market-linked, no guarantee", f"<strong>{esc(_r(rates, 'ppf'))}</strong>, notified quarterly"],
        ["<strong>Lock-in</strong>", "Until 60 (Tier I)", "15 years, partial access from year 6"],
        ["<strong>Tax on exit</strong>", "60% of the corpus is tax-free, 40% must buy an annuity", "Entirely tax-free"],
        ["<strong>Extra deduction</strong>", "80CCD(1B): ₹50,000 beyond 80C, in both regimes", "Within the ₹1.5 lakh 80C cap, old regime only"],
        ["<strong>Risk</strong>", "Yours", "None beyond the government's own"],
    ])}
    <p class="guide-p">
      NPS exists for a specific reason: it is the only route to an extra ₹50,000 deduction under 80CCD(1B), and
      it stays available under the new regime. That is a real benefit if you are in the 30% bracket.
    </p>
    <p class="guide-p">
      But 40% of the corpus must buy an annuity at 60, and the annuity rate is whatever it is that day. PPF gives
      you a smaller, certain, entirely tax-free amount with no forced purchase at the end.
    </p>
    <p class="guide-src">Rules per the PFRDA and the Income-tax Act; PPF rate from the National Savings Institute, quarter beginning {esc(_d(rates, "ppf"))}.</p>
    <p class="guide-cta">
      <a class="btn btn-primary" href="../products/national-pension-system.html">NPS details</a>
      <a class="btn btn-ghost" href="../products/public-provident-fund.html">PPF details</a>
    </p>
  </div>
</section>"""
