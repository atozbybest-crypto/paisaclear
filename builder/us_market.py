"""US market overview — indices, Treasury yields and the largest US funds."""

from __future__ import annotations

from .site import esc, icon


def _when(iso: str) -> str:
    from datetime import date
    try:
        d = date.fromisoformat(str(iso)[:10])
        return f"{d.day} {d.strftime('%b %Y')}"
    except (TypeError, ValueError):
        return str(iso or "—")


def _change(v) -> str:
    if v is None:
        return '<span class="muted">—</span>'
    cls = "is-up" if v >= 0 else "is-down"
    return f'<span class="{cls}">{v:+.2f}%</span>'


def page(data: dict) -> str:
    indices = data.get("indices", [])
    etfs = sorted(data.get("etfs", []), key=lambda x: x["label"])
    funds = sorted(data.get("funds", []), key=lambda x: x["label"])
    treasuries = data.get("treasuries", [])
    fetched = _when(data.get("fetchedAt", ""))

    cards = "".join(
        f"""<div class="us-card">
  <span class="us-name">{esc(i['label'])}</span>
  <strong class="us-value">{i['price']:,.2f}</strong>
  <span class="us-meta">day {_change(i.get('day'))} · 1 year {_change(i.get('year'))}</span>
  <span class="us-date">as of {esc(_when(i.get('asOf', '')))}</span>
</div>""" for i in indices
    )

    treasury_rows = "".join(
        f"<tr><td>{esc(t['label'].replace('Yr', 'year'))}</td>"
        f"<td class='mg-num'>{t['value']:.2f}%</td>"
        f"<td class='mg-num small'>{esc(t.get('asOf', ''))}</td></tr>"
        for t in treasuries
    ) or "<tr><td colspan='3' class='mg-empty'>Treasury feed unavailable.</td></tr>"

    def fund_rows(items: list[dict]) -> str:
        return "".join(
            f"<tr>"
            f"<td><span class='mg-co'>{esc(x['label'])}</span><span class='mg-sector'>{esc(x['ticker'])}</span></td>"
            f"<td class='mg-num'>{x['price']:,.2f}</td>"
            f"<td class='mg-num'>{_change(x.get('day'))}</td>"
            f"<td class='mg-num'>{_change(x.get('month'))}</td>"
            f"<td class='mg-num'>{_change(x.get('year'))}</td>"
            f"<td class='mg-num small'>{esc(_when(x.get('asOf', '')))}</td>"
            f"</tr>" for x in items
        ) or "<tr><td colspan='6' class='mg-empty'>No data.</td></tr>"

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
      The three main indices, the Treasury yield curve, and the largest US-listed funds — with the date every
      figure was observed. Prices in dollars; nothing here is a recommendation.
    </p>
    <p class="page-meta">Fetched {esc(fetched)} · refreshed at 09:00 and 21:30 IST</p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="us-grid">{cards}</div>
  </div>
</section>

<section class="section section-tint">
  <div class="shell">
    <h2 class="subhead">Treasury yield curve</h2>
    <div class="cmp-wrap"><table class="cmp-table">
      <thead><tr>
        <th scope="col">Maturity</th><th scope="col">Yield</th><th scope="col">Curve date</th>
      </tr></thead>
      <tbody>{treasury_rows}</tbody>
    </table></div>
    <p class="guide-src">
      Published by the US Department of the Treasury. A curve where the 2-year yields more than the 30-year is
      inverted, which historically precedes slower growth — this one is not.
    </p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <h2 class="subhead">Largest US ETFs</h2>
    <div class="cmp-wrap"><table class="cmp-table">
      <thead><tr>
        <th scope="col">Fund</th><th scope="col">Price</th><th scope="col">Day</th>
        <th scope="col">Month</th><th scope="col">1 year</th><th scope="col">As of</th>
      </tr></thead>
      <tbody>{fund_rows(etfs)}</tbody>
    </table></div>

    <h2 class="guide-h2">Index mutual funds</h2>
    <div class="cmp-wrap"><table class="cmp-table">
      <thead><tr>
        <th scope="col">Fund</th><th scope="col">NAV</th><th scope="col">Day</th>
        <th scope="col">Month</th><th scope="col">1 year</th><th scope="col">As of</th>
      </tr></thead>
      <tbody>{fund_rows(funds)}</tbody>
    </table></div>
    <p class="guide-src">
      Prices and NAV history from Yahoo Finance. Mutual fund NAVs are struck once a day after the US close;
      ETF prices move through the session.
    </p>

    <h2 class="guide-h2">The full list, by category</h2>
    <p class="guide-p">
      These are the largest funds only. The <a href="us-funds.html">US funds section</a> groups 62 mutual funds
      and ETFs into ten categories — index, bonds, money market, dividend, sector, target date, balanced and
      more — each with its own return history and the date attached.
      <a href="us-compare.html">Compare all of them in one table</a>.
    </p>

    <h2 class="guide-h2">Average US deposit rates</h2>
    <p class="guide-p">
      Deposit rates are set by each bank, not by a regulator, so there is no single national rate to publish.
      The FDIC publishes a weekly national average across insured institutions:
      <a href="https://www.fdic.gov/national-rates-and-rate-caps" target="_blank" rel="noopener noreferrer">
      FDIC national rates and rate caps ↗</a>.
    </p>
  </div>
</section>

<section class="section">
  <div class="shell shell-narrow">
    <div class="calc-notes">
      <h2>Before investing from India</h2>
      <ul class="check-list">
        <li>{icon("alert", "icon icon-sm")}<span>Remittances fall under the RBI's liberalised remittance scheme, with a TCS threshold that changes — check the current rule.</span></li>
        <li>{icon("alert", "icon icon-sm")}<span>US dividends are withheld at source; India gives a foreign tax credit, and the paperwork decides whether you actually get it.</span></li>
        <li>{icon("alert", "icon icon-sm")}<span><strong>Estate tax.</strong> US-situated shares held by a non-resident can be exposed above a low threshold. The <a href="us-investing-from-india.html">cross-border guide</a> explains it.</span></li>
        <li>{icon("alert", "icon icon-sm")}<span>Returns here are in dollars. Your return in rupees includes the exchange rate.</span></li>
      </ul>
    </div>
  </div>
</section>
"""
