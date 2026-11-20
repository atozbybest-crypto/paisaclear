"""US market page — indices, Treasury yields, ETFs, funds and deposit rates.

Aimed at an Indian reader looking at US markets, so every table carries its
observation date and a link to the source.
"""

from __future__ import annotations

from .site import esc, icon


def _when(iso: str) -> str:
    try:
        from datetime import date
        d = date.fromisoformat(iso)
        return f"{d.day} {d.strftime('%b %Y')}"
    except (TypeError, ValueError):
        return iso or "—"


def _change(v) -> str:
    if v is None:
        return "—"
    cls = "is-up" if v >= 0 else "is-down"
    return f'<span class="{cls}">{v:+.2f}%</span>'


def page(data: dict) -> str:
    fetched = _when((data.get("fetchedAt") or "")[:10])
    indices = data.get("indices", [])
    etfs = data.get("etfs", [])
    funds = data.get("funds", [])
    treasuries = data.get("treasuries", [])
    deposits = data.get("deposits", [])

    index_cards = "".join(
        f"""<div class="us-card">
  <span class="us-name">{esc(i['label'])}</span>
  <strong class="us-value">{i['price']:,.2f}</strong>
  <span class="us-meta">day {_change(i.get('day'))} · 1y {_change(i.get('year'))}</span>
  <span class="us-date">as of {esc(_when(i.get('asOf', '')))}</span>
</div>""" for i in indices
    )

    treasury_rows = "".join(
        f"<tr><td>{esc(t['label'])}</td><td class='mg-num'>{t['value']:.2f}%</td>"
        f"<td class='mg-num small'>{esc(t.get('asOf', ''))}</td></tr>" for t in treasuries
    ) or "<tr><td colspan='3' class='mg-empty'>Treasury feed unavailable — the last published curve is on treasury.gov.</td></tr>"

    def rows(items, show_year=True):
        return "".join(
            f"<tr><td><span class='mg-co'>{esc(x['label'])}</span><span class='mg-sector'>{esc(x['ticker'])}</span></td>"
            f"<td class='mg-num'>{x['price']:,.2f}</td>"
            f"<td class='mg-num'>{_change(x.get('day'))}</td>"
            f"<td class='mg-num'>{_change(x.get('month'))}</td>"
            f"{f'<td class=mg-num>{_change(x.get(chr(121)+chr(101)+chr(97)+chr(114)))}</td>' if show_year else ''}"
            f"<td class='mg-num small'>{esc(_when(x.get('asOf', '')))}</td></tr>"
            for x in items
        )

    deposit_rows = "".join(
        f"<tr><td>{esc(d['label'])}</td><td class='mg-num'>{d['value']:.2f}%</td></tr>" for d in deposits
    ) or "<tr><td colspan='2' class='mg-empty'>Deposit rate feed unavailable.</td></tr>"

    return f"""
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="index.html">Home</a></li><li aria-current="page">US market</li>
    </ol></nav>

    <div class="country-switch" role="group" aria-label="Choose a market">
      <a class="cs-chip" href="browse.html">India</a>
      <span class="cs-chip is-on" aria-current="page">United States</span>
    </div>

    <h1>US markets</h1>
    <p class="page-lede">
      The US side of the site: indices, Treasury yields, the largest ETFs and index funds, and average deposit
      rates. Every figure carries the date it was observed and a link to the source.
    </p>
    <p class="page-meta">Fetched {esc(fetched)} · prices are market data, not recommendations</p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="us-grid">{index_cards}</div>
  </div>
</section>

<section class="section section-tint">
  <div class="shell">
    <div class="split">
      <div class="split-main">
        <h2 class="subhead">Treasury yields</h2>
        <div class="cmp-wrap"><table class="cmp-table">
          <thead><tr><th scope="col">Maturity</th><th scope="col">Yield</th><th scope="col">Curve date</th></tr></thead>
          <tbody>{treasury_rows}</tbody>
        </table></div>
        <p class="guide-src">Source: US Department of the Treasury daily yield curve.</p>

        <h2 class="guide-h2">Browse by category</h2>
        <p class="guide-p">
          The <a href="us-funds.html">US funds section</a> groups 62 mutual funds and ETFs into ten categories —
          index, bonds, money market, dividend, sector, target date and more — each with its own return history.
          <a href="us-compare.html">Compare them side by side</a>.
        </p>

        <h2 class="guide-h2">Largest ETFs</h2>
        <div class="cmp-wrap"><table class="cmp-table">
          <thead><tr><th scope="col">Fund</th><th scope="col">Price</th><th scope="col">Day</th><th scope="col">Month</th><th scope="col">1 year</th><th scope="col">As of</th></tr></thead>
          <tbody>{rows(etfs)}</tbody>
        </table></div>

        <h2 class="guide-h2">Index mutual funds</h2>
        <div class="cmp-wrap"><table class="cmp-table">
          <thead><tr><th scope="col">Fund</th><th scope="col">NAV</th><th scope="col">Day</th><th scope="col">Month</th><th scope="col">1 year</th><th scope="col">As of</th></tr></thead>
          <tbody>{rows(funds)}</tbody>
        </table></div>
        <p class="guide-src">Prices and NAV history from Yahoo Finance. Mutual fund NAVs are struck once a day, after the US close.</p>
      </div>

      <aside class="split-aside">
        <div class="aside-card">
          <h2>Average deposit rates</h2>
          <table class="mg-table mg-small">
            <thead><tr><th>Product</th><th class="mg-num">Rate</th></tr></thead>
            <tbody>{deposit_rows}</tbody>
          </table>
          <p class="aside-note">Source: FDIC national rates. US deposit rates are set by each bank, not by the regulator — these are averages.</p>
        </div>

        <div class="aside-card">
          <h2>Before you invest from India</h2>
          <ul class="check-list">
            <li>{icon("alert", "icon icon-sm")}<span>Remitting money abroad falls under the RBI's liberalised remittance scheme, with a TCS threshold you should check for the current year.</span></li>
            <li>{icon("alert", "icon icon-sm")}<span>US dividends are taxed at source, and India gives a foreign tax credit — the paperwork matters.</span></li>
            <li>{icon("alert", "icon icon-sm")}<span><strong>Estate tax.</strong> US-situated shares held by a non-resident can be exposed to US estate tax above a low threshold. This catches Indian investors by surprise.</span></li>
            <li>{icon("alert", "icon icon-sm")}<span>Currency moves can wipe out a gain that looks good in dollars.</span></li>
          </ul>
        </div>
      </aside>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell shell-narrow">
    <div class="calc-notes">
      <h2>What this page is not</h2>
      <ul class="check-list">
        <li>{icon("alert", "icon icon-sm")}<span>Not a recommendation, and not a comparison of expense ratios, tracking error or liquidity.</span></li>
        <li>{icon("alert", "icon icon-sm")}<span>Not tax advice. Cross-border treatment depends on your residency and on rules that change.</span></li>
        <li>{icon("check", "icon icon-sm")}<span>Every figure carries its date. Prices move continuously; a page is a snapshot.</span></li>
      </ul>
      <p class="muted">
        Sources: <a href="https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve" target="_blank" rel="noopener noreferrer">US Treasury</a> ·
        <a href="https://www.fdic.gov/national-rates-and-rate-caps" target="_blank" rel="noopener noreferrer">FDIC</a> ·
        <a href="https://finance.yahoo.com" target="_blank" rel="noopener noreferrer">Yahoo Finance</a> ·
        <a href="https://www.sec.gov/edgar" target="_blank" rel="noopener noreferrer">SEC EDGAR</a>
      </p>
    </div>
  </div>
</section>
"""
