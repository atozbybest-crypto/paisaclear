"""US company pages built from SEC EDGAR data."""

from __future__ import annotations

from .site import breadcrumb, esc, icon


def _money(value) -> str:
    if value is None:
        return "—"
    if abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:,.1f}bn"
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:,.0f}m"
    return f"${value:,.0f}"


def _fy(rows) -> str:
    return rows[0]["fy"] if rows else "—"


def hub(companies: list[dict]) -> str:
    rows = "".join(
        f"<tr><td><a href='us-companies/{esc(c['ticker'].lower())}.html'>"
        f"<span class='mg-co'>{esc(c['name'])}</span>"
        f"<span class='mg-sector'>{esc(c['ticker'])} · {esc(c['sic'])}</span></a></td>"
        f"<td class='mg-num'>{_money(c['revenue'][0]['value']) if c['revenue'] else '—'}</td>"
        f"<td class='mg-num'>{_fy(c['revenue'])}</td>"
        f"<td class='mg-num'>{_money(c['income'][0]['value']) if c['income'] else '—'}</td>"
        f"<td class='mg-num small'>{len(c['filings'])}</td></tr>"
        for c in companies
    )

    return f"""
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="index.html">Home</a></li>
      <li><a href="us-market.html">US market</a></li><li aria-current="page">Companies</li>
    </ol></nav>
    <div class="country-switch" role="group" aria-label="Choose a market">
      <a class="cs-chip" href="browse.html">India</a>
      <a class="cs-chip" href="us-market.html">US market</a>
      <span class="cs-chip is-on" aria-current="page">US companies</span>
    </div>
    <h1>US companies, from their own filings</h1>
    <p class="page-lede">
      {len(companies)} of the largest listed US companies, with revenue, net income and the filings that
      produced them. Every figure comes from the company's own SEC filing — not from a data vendor's summary.
    </p>
    <p class="page-meta">Source: SEC EDGAR · figures as filed · not investment research</p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="cmp-wrap"><table class="cmp-table">
      <thead><tr><th scope="col">Company</th><th scope="col">Revenue</th><th scope="col">FY</th>
      <th scope="col">Net income</th><th scope="col">Filings</th></tr></thead>
      <tbody>{rows}</tbody>
    </table></div>
    <p class="guide-src">
      Revenue and net income are annual figures tagged in each company's XBRL filing. Where a company tags
      several revenue lines, the most specific one is shown. Fiscal years differ between companies.
    </p>
  </div>
</section>
"""


def detail(company: dict) -> str:
    def series(rows, label, money=True):
        if not rows:
            return f"<tr><td>{label}</td><td class='mg-num'>—</td><td class='mg-num'>—</td></tr>"
        return "".join(
            f"<tr><td>{label if i == 0 else ''}</td>"
            f"<td class='mg-num'>{_money(r['value']) if money else r['value']}</td>"
            f"<td class='mg-num small'>FY{r['fy']} · {esc(r['end'])}</td></tr>"
            for i, r in enumerate(rows)
        )

    filings = "".join(
        f"<tr><td><a href='{esc(f['url'])}' target='_blank' rel='noopener noreferrer'>{esc(f['form'])}</a></td>"
        f"<td class='mg-num'>{esc(f['date'])}</td></tr>"
        for f in company["filings"]
    ) or "<tr><td colspan='2' class='mg-empty'>No recent filings in the index.</td></tr>"

    return f"""
<section class="page-head">
  <div class="shell">
    {breadcrumb([("Home", "../index.html"), ("US market", "../us-market.html"),
                 ("US companies", "../us-companies.html"), (company["name"], "")])}
    <h1>{esc(company["name"])}</h1>
    <p class="page-lede">
      {esc(company["ticker"])} · {esc(company.get("sic") or "Listed company")} · CIK {esc(str(company["cik"]))}
    </p>
    <p class="page-meta">Figures as filed with the SEC · fiscal year ends {esc(company.get("fiscalYearEnd") or "—")}</p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="split">
      <div class="split-main">
        <h2 class="subhead">Revenue and net income, as filed</h2>
        <div class="cmp-wrap"><table class="cmp-table">
          <thead><tr><th scope="col">Line</th><th scope="col">Value</th><th scope="col">Period</th></tr></thead>
          <tbody>
            {series(company["revenue"], "Revenue")}
            {series(company["income"], "Net income")}
            {series(company["eps"], "Diluted EPS", money=False)}
          </tbody>
        </table></div>
        <p class="guide-src">
          Values are the XBRL facts tagged by the company in its 10-K. They are not adjusted, restated or
          normalised — what the company reported is what appears here.
        </p>

        <h2 class="guide-h2">Recent filings</h2>
        <div class="cmp-wrap"><table class="cmp-table">
          <thead><tr><th scope="col">Form</th><th scope="col">Filed</th></tr></thead>
          <tbody>{filings}</tbody>
        </table></div>
        <p class="guide-src">
          Links go directly to the document on sec.gov. A 10-K is the annual report, 10-Q the quarterly,
          8-K a material event.
        </p>
      </div>

      <aside class="split-aside">
        <div class="aside-card">
          <h2>Read this before the numbers</h2>
          <ul class="check-list">
            <li>{icon("alert", "icon icon-sm")}<span>Revenue is not profit, and profit is not cash. The cash-flow statement is where a business is actually judged.</span></li>
            <li>{icon("alert", "icon icon-sm")}<span>Fiscal years differ. Apple's year ends in September, most others in December — comparisons across companies need care.</span></li>
            <li>{icon("alert", "icon icon-sm")}<span>One-off items can flatter or sink a year. Read the filing, not this table.</span></li>
          </ul>
        </div>
        <div class="aside-card">
          <h2>Primary source</h2>
          <p class="aside-note">
            <a href="https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={esc(str(company['cik']))}&type=10-K"
               target="_blank" rel="noopener noreferrer">All {esc(company['ticker'])} filings on EDGAR ↗</a>
          </p>
        </div>
      </aside>
    </div>
  </div>
</section>

<section class="section section-tint">
  <div class="shell shell-narrow">
    <div class="calc-notes">
      <h2>What this page is not</h2>
      <ul class="check-list">
        <li>{icon("alert", "icon icon-sm")}<span>Not research, not a rating, and not a view on the share price.</span></li>
        <li>{icon("alert", "icon icon-sm")}<span>Not adjusted for accounting changes, and not a like-for-like comparison with another company.</span></li>
        <li>{icon("check", "icon icon-sm")}<span>A faithful copy of what the company filed, with a link to the filing itself.</span></li>
      </ul>
      <p class="muted"><a href="../us-companies.html">All US companies →</a></p>
    </div>
  </div>
</section>
"""
