"""US funds section — same structure as the Indian catalogue.

Hub → category → product, plus a comparison table. Fund records are fetched
from market data; nothing here is a recommendation.
"""

from __future__ import annotations

from .site import breadcrumb, esc, icon


def slugify(text: str) -> str:
    out = []
    for ch in text.lower():
        out.append(ch if ch.isalnum() else "-")
    return "-".join(filter(None, "".join(out).split("-")))


def _pct(v) -> str:
    if v is None:
        return '<span class="muted">—</span>'
    return f'<span class="{"is-up" if v >= 0 else "is-down"}">{v:+.2f}%</span>'


def _money(v) -> str:
    return f"${v:,.2f}"


def hub(data: dict) -> str:
    records = data.get("records", [])
    cats = data.get("categories", [])
    fetched = (data.get("fetchedAt") or "")[:10]

    from collections import Counter
    counts = Counter(r["category"] for r in records)

    cards = "".join(
        f"""<a class="plan-card" href="us-funds/{slugify(c)}.html">
  <span class="plan-tag">{counts[c]} funds</span>
  <span class="plan-name">{esc(c)}</span>
  <span class="plan-line">{_sample(records, c)}</span>
  <span class="plan-cta">Browse {esc(c.lower())} →</span>
</a>""" for c in cats
    )

    return f"""
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="index.html">Home</a></li><li aria-current="page">US funds</li>
    </ol></nav>
    <div class="country-switch" role="group" aria-label="Choose a market">
      <a class="cs-chip" href="browse.html">India</a>
      <span class="cs-chip is-on" aria-current="page">United States</span>
    </div>
    <h1>US funds and ETFs</h1>
    <p class="page-lede">
      {len(records)} US-listed funds across {len(cats)} categories — index, bond, money market, dividend, sector,
      target date and balanced. Prices are market data and every record states the date it was observed.
    </p>
    <p class="page-meta">Fetched {esc(fetched)} · refreshed with the daily job · not a recommendation</p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="plan-grid">{cards}</div>

    <p class="guide-cta">
      <a class="btn btn-primary" href="us-compare.html">Compare all {len(records)} side by side</a>
    </p>

    <div class="calc-notes">
      <h2>What is here, and what is deliberately not</h2>
      <ul class="check-list">
        <li>{icon("check", "icon icon-sm")}<span><strong>Mutual funds and ETFs</strong> that a retail investor can actually buy, with NAV or price history pulled from market data.</span></li>
        <li>{icon("alert", "icon icon-sm")}<span><strong>No collective investment trusts, stable-value funds or variable annuities.</strong> These are not publicly priced: a CIT is available only inside a retirement plan, stable value is a plan-level product, and a variable annuity's value depends on a contract. Publishing a "NAV" for them would be inventing a number.</span></li>
        <li>{icon("alert", "icon icon-sm")}<span><strong>No stocks.</strong> Company pages were removed on 20 November; this section is funds only.</span></li>
        <li>{icon("alert", "icon icon-sm")}<span>Returns are computed from price or NAV history and are past performance. Expense ratios are not in this data — check the fund's prospectus.</span></li>
      </ul>
    </div>
  </div>
</section>
"""


def _sample(records: list[dict], category: str) -> str:
    names = [r["name"] for r in records if r["category"] == category][:3]
    return " · ".join(names)


def category_page(data: dict, category: str) -> str:
    records = [r for r in data["records"] if r["category"] == category]
    fetched = (data.get("fetchedAt") or "")[:10]
    cards = "".join(
        f"""<a class="plan-card" href="{esc(r['ticker'].lower())}.html">
  <span class="plan-tag">{esc(r['kind'])} · {esc(r['ticker'])}</span>
  <span class="plan-name">{esc(r['name'])}</span>
  <span class="plan-line">{_money(r['price'])} · 1y {('%.2f' % r['c1']) if r['c1'] is not None else '—'}% · 3y {('%.2f' % r['c3']) if r['c3'] is not None else '—'}%</span>
  <span class="plan-meta">as of {esc(r['asOf'])}</span>
</a>""" for r in records
    )

    return f"""
<section class="page-head">
  <div class="shell">
    {breadcrumb([("Home", "../index.html"), ("US funds", "../us-funds.html"), (category, "")])}
    <div class="country-switch" role="group" aria-label="Choose a market">
      <a class="cs-chip" href="../browse.html">India</a>
      <a class="cs-chip" href="../us-market.html">US market</a>
    </div>
    <h1>{esc(category)}</h1>
    <p class="page-lede">{len(records)} US-listed funds in this category, with the return history shown for each.</p>
    <p class="page-meta">Fetched {esc(fetched)}</p>
  </div>
</section>

<section class="section">
  <div class="shell"><div class="plan-grid">{cards}</div></div>
</section>
"""


def product_page(record: dict) -> str:
    rows = [
        ("Ticker", esc(record["ticker"])),
        ("Type", esc(record["kind"])),
        ("Category", esc(record["category"])),
        ("Price / NAV", _money(record["price"])),
        ("As of", esc(record["asOf"])),
    ]
    fact_rows = "".join(f'<div class="fact-row"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows)

    return f"""
<section class="page-head">
  <div class="shell">
    {breadcrumb([("Home", "../index.html"), ("US funds", "../us-funds.html"),
                 (record["category"], f"../us-funds/{slugify(record['category'])}.html"),
                 (record["name"], "")])}
    <h1>{esc(record["name"])}</h1>
    <p class="page-provider">{esc(record["ticker"])} · {esc(record["kind"])} · {esc(record["category"])}</p>
    <p class="page-meta">Price as of {esc(record["asOf"])} · returns computed from price history</p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="split">
      <div class="split-main">
        <h2 class="subhead">Return history</h2>
        <div class="cmp-wrap"><table class="cmp-table">
          <thead><tr><th scope="col">Period</th><th scope="col">Annualised return</th></tr></thead>
          <tbody>
            <tr><td>1 year</td><td class="mg-num">{_pct(record.get('c1'))}</td></tr>
            <tr><td>3 years</td><td class="mg-num">{_pct(record.get('c3'))}</td></tr>
            <tr><td>5 years</td><td class="mg-num">{_pct(record.get('c5'))}</td></tr>
            <tr><td>Distribution yield (trailing 12m)</td><td class="mg-num">{_pct(record.get('yield'))}</td></tr>
          </tbody>
        </table></div>
        <p class="guide-src">
          Computed from monthly price or NAV history. Distribution yield is the trailing twelve months of
          payouts divided by the current price — for a money market fund, which holds NAV near $1, that yield is
          the return that matters.
        </p>

        <h2 class="guide-h2">What to check before buying</h2>
        <ul class="check-list">
          <li>{icon("alert", "icon icon-sm")}<span><strong>Expense ratio.</strong> Not in this data. A 0.03% index ETF and a 1% active fund can hold identical assets and deliver very different outcomes.</span></li>
          <li>{icon("alert", "icon icon-sm")}<span><strong>Tax for an Indian resident.</strong> US dividends are withheld at source; gains are taxed in India. The <a href="../us-investing-from-india.html">cross-border guide</a> sets out the detail.</span></li>
          <li>{icon("alert", "icon icon-sm")}<span><strong>Currency.</strong> Returns here are in dollars. Your return in rupees includes the exchange rate.</span></li>
          <li>{icon("alert", "icon icon-sm")}<span><strong>Liquidity.</strong> ETFs trade during market hours; mutual funds price once a day after the close.</span></li>
        </ul>
      </div>

      <aside class="split-aside">
        <div class="aside-card">
          <h2>Key facts</h2>
          <dl class="fact-list">{fact_rows}</dl>
        </div>
        <div class="aside-card">
          <h2>Source</h2>
          <p class="aside-note">
            <a href="https://finance.yahoo.com/quote/{esc(record['ticker'])}" target="_blank" rel="noopener noreferrer">
              {esc(record['ticker'])} on Yahoo Finance ↗</a>
          </p>
        </div>
      </aside>
    </div>
  </div>
</section>
"""


def compare_page(data: dict) -> str:
    records = sorted(data["records"], key=lambda r: (r["category"], r["name"]))
    body = "".join(
        f"<tr data-cat='{esc(r['category'])}'>"
        f"<td><a href='us-funds/{esc(r['ticker'].lower())}.html'><span class='mg-co'>{esc(r['name'])}</span>"
        f"<span class='mg-sector'>{esc(r['ticker'])} · {esc(r['kind'])}</span></a></td>"
        f"<td>{esc(r['category'])}</td>"
        f"<td class='mg-num'>{_money(r['price'])}</td>"
        f"<td class='mg-num'>{_pct(r.get('c1'))}</td>"
        f"<td class='mg-num'>{_pct(r.get('c3'))}</td>"
        f"<td class='mg-num'>{_pct(r.get('c5'))}</td>"
        f"<td class='mg-num'>{_pct(r.get('yield'))}</td>"
        f"<td class='mg-num small'>{esc(r['asOf'])}</td></tr>"
        for r in records
    )
    cats = "".join(f'<option value="{esc(c)}">{esc(c)}</option>' for c in data["categories"])

    return f"""
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="index.html">Home</a></li>
      <li><a href="us-funds.html">US funds</a></li><li aria-current="page">Compare</li>
    </ol></nav>
    <h1>Compare US funds</h1>
    <p class="page-lede">
      All {len(records)} funds in one table: price, one, three and five-year returns, and distribution yield.
      Filter by category, or sort by any column.
    </p>
    <p class="page-meta">Fetched {(data.get('fetchedAt') or '')[:10]} · returns are past performance, not a forecast</p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="browse-filters">
      <label class="field">
        <span class="field-label">Category</span>
        <span class="field-input"><select id="us-cat">
          <option value="">All categories</option>{cats}
        </select></span>
      </label>
    </div>

    <div class="cmp-wrap"><table class="cmp-table" id="us-table">
      <thead><tr>
        <th scope="col">Fund</th><th scope="col">Category</th><th scope="col">Price</th>
        <th scope="col">1y</th><th scope="col">3y</th><th scope="col">5y</th>
        <th scope="col">Yield</th><th scope="col">As of</th>
      </tr></thead>
      <tbody>{body}</tbody>
    </table></div>

    <p class="calc-fineprint">
      Returns are annualised and computed from price or NAV history. Expense ratios are not included. A fund
      with a higher past return may simply have taken more risk.
    </p>
  </div>
</section>

<script>
(function () {{
  var sel = document.getElementById("us-cat");
  if (!sel) return;
  sel.addEventListener("change", function () {{
    var v = sel.value;
    document.querySelectorAll("#us-table tbody tr").forEach(function (tr) {{
      tr.hidden = v !== "" && tr.getAttribute("data-cat") !== v;
    }});
  }});
}})();
</script>
"""
