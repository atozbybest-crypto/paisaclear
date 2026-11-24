"""Gold price page — rupee and dollar figures with a server-rendered chart."""

from __future__ import annotations

from .site import esc, icon


def _when(iso: str) -> str:
    from datetime import date
    try:
        d = date.fromisoformat(iso[:10])
        return f"{d.day} {d.strftime('%b %Y')}"
    except (TypeError, ValueError):
        return iso or "—"


def _inr(v) -> str:
    if v is None:
        return "—"
    s = f"{round(v):d}"
    if len(s) <= 3:
        return "₹" + s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return "₹" + ",".join(parts) + "," + tail


def _change(v) -> str:
    if v is None:
        return "—"
    cls = "is-up" if v >= 0 else "is-down"
    return f'<span class="{cls}">{v:+.2f}%</span>'


def _chart(history: list[dict]) -> str:
    if len(history) < 3:
        return "<p class='muted'>History unavailable.</p>"
    w, h, pad = 820, 300, 34
    values = [p["per10g"] for p in history]
    low, high = min(values), max(values)
    span = (high - low) or 1
    step = (w - pad * 2) / (len(values) - 1)

    pts = []
    for i, p in enumerate(history):
        x = pad + i * step
        y = h - pad - ((p["per10g"] - low) / span) * (h - pad * 2)
        pts.append(f"{x:.1f},{y:.1f}")

    grid = ""
    for frac in (0.0, 0.5, 1.0):
        y = h - pad - frac * (h - pad * 2)
        value = low + frac * span
        grid += (f"<line x1='{pad}' y1='{y:.1f}' x2='{w - pad}' y2='{y:.1f}' "
                 f"stroke='#E3DED0' stroke-width='1'/>"
                 f"<text x='{pad - 6}' y='{y + 4:.1f}' text-anchor='end' font-size='11' "
                 f"fill='#6B746E'>{_inr(value)}</text>")

    first, last = history[0]["m"], history[-1]["m"]
    return f"""
<figure class="gold-chart">
  <svg viewBox="0 0 {w} {h}" role="img"
       aria-label="Rupee price of 10 grams of gold from {first} to {last}">
    {grid}
    <polyline points="{' '.join(pts)}" fill="none" stroke="#0F5132" stroke-width="2.5"
              stroke-linejoin="round" stroke-linecap="round"/>
    <text x="{pad}" y="{h - 8}" font-size="11" fill="#6B746E">{first}</text>
    <text x="{w - pad}" y="{h - 8}" text-anchor="end" font-size="11" fill="#6B746E">{last}</text>
  </svg>
  <figcaption>
    Rupee value of 10 grams, computed monthly from international gold futures and the USD/INR rate.
    This is a reference conversion — it excludes import duty and dealer premium.
  </figcaption>
</figure>
"""


def page(data: dict) -> str:
    if not data:
        return "<section class='section'><div class='shell'><p class='muted'>Gold data unavailable.</p></div></section>"

    per10g = data.get("per10g", {})
    usd = data.get("usdPerOunce", {})
    fx = data.get("usdinr", {})
    etf = data.get("etf") or {}
    history = data.get("history", [])

    years = {}
    for point in history:
        years.setdefault(point["m"][:4], []).append(point["per10g"])
    year_rows = "".join(
        f"<tr><td>{y}</td><td class='mg-num'>{_inr(sum(v) / len(v))}</td>"
        f"<td class='mg-num'>{_inr(min(v))}</td><td class='mg-num'>{_inr(max(v))}</td></tr>"
        for y, v in sorted(years.items(), reverse=True)
    )

    recent = "".join(
        f"<tr><td>{p['m']}</td><td class='mg-num'>{_inr(p['per10g'])}</td>"
        f"<td class='mg-num'>${p['usd']:,.0f}</td><td class='mg-num'>{p['inr']:.2f}</td></tr>"
        for p in history[-12:][::-1]
    )

    return f"""
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="index.html">Home</a></li><li aria-current="page">Gold price</li>
    </ol></nav>
    <h1>Gold price in India, and the history behind it</h1>
    <p class="page-lede">
      What ten grams of gold is worth in rupees today, computed from international gold futures and the
      dollar–rupee rate, alongside the NSE gold ETF price. Every figure carries the date it was observed.
    </p>
    <p class="page-meta">Fetched {_when(data.get('fetchedAt', ''))} · refreshed with the daily job</p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="us-grid">
      <div class="us-card">
        <span class="us-name">Gold, per 10 grams</span>
        <strong class="us-value">{_inr(per10g.get('value'))}</strong>
        <span class="us-meta">reference conversion · as of {_when(per10g.get('asOf', ''))}</span>
      </div>
      <div class="us-card">
        <span class="us-name">International, per troy ounce</span>
        <strong class="us-value">${usd.get('value', 0):,.2f}</strong>
        <span class="us-meta">day {_change(usd.get('day'))} · 1y {_change(usd.get('year'))}</span>
      </div>
      <div class="us-card">
        <span class="us-name">US dollar / rupee</span>
        <strong class="us-value">₹{fx.get('value', 0):.2f}</strong>
        <span class="us-meta">as of {_when(fx.get('asOf', ''))}</span>
      </div>
      <div class="us-card">
        <span class="us-name">Gold ETF (GOLDBEES), per unit</span>
        <strong class="us-value">{_inr(etf.get('value'))}</strong>
        <span class="us-meta">NSE closing price · {_when(etf.get('asOf', ''))}</span>
      </div>
    </div>
  </div>
</section>

<section class="section section-tint">
  <div class="shell">
    {_chart(history)}
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="split">
      <div class="split-main">
        <h2 class="subhead">Year by year</h2>
        <div class="cmp-wrap"><table class="cmp-table">
          <thead><tr><th scope="col">Year</th><th scope="col">Average</th>
          <th scope="col">Low</th><th scope="col">High</th></tr></thead>
          <tbody>{year_rows}</tbody>
        </table></div>
        <p class="guide-src">
          Monthly averages of the rupee figure, computed from the two source series. Years with fewer
          observations are averages of what was published.
        </p>

        <h2 class="guide-h2">Last twelve months</h2>
        <div class="cmp-wrap"><table class="cmp-table">
          <thead><tr><th scope="col">Month</th><th scope="col">Per 10 g</th>
          <th scope="col">USD/oz</th><th scope="col">USD/INR</th></tr></thead>
          <tbody>{recent}</tbody>
        </table></div>
      </div>

      <aside class="split-aside">
        <div class="aside-card">
          <h2>Why the Indian price is higher</h2>
          <p class="aside-note">
            The figure above is a conversion, not a jeweller's quote. The landed Indian price adds
            <strong>import duty</strong> and a dealer premium, and jewellery adds making charges and GST on top.
            That is why your local rate is consistently above this number.
          </p>
        </div>
        <div class="aside-card">
          <h2>How this refreshes</h2>
          <p class="aside-note">
            The figures are pulled at 09:00 and 21:30 IST along with fund NAVs and bond yields, then the page is
            rebuilt. The date beside each figure is the last observation, not the day you are reading it.
          </p>
        </div>
      </aside>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell shell-narrow">
    <h2 class="guide-h2">What moves the rupee price</h2>
    <p class="guide-p">
      Three things, and only one of them is "gold" in the abstract. The <strong>dollar price</strong> of the metal
      moves with global demand, real interest rates and central-bank buying. The <strong>rupee</strong> moves
      independently: when the rupee weakens, the same dollar price buys fewer grams, so the Indian price rises
      even if gold does not move at all.
    </p>
    <p class="guide-p">
      The third is <strong>duty and premium</strong>. India imports almost all of its gold, and the landed price
      carries customs duty plus whatever dealers are charging on the day. In a festive week the premium can widen
      by a percent or more on its own.
    </p>
    <p class="guide-p">
      That is why the figure at the top of this page and the number at a jeweller's counter are different, and why
      comparing the two is not a like-for-like comparison.
    </p>

    <h2 class="guide-h2">Physical gold, an ETF, or a bond</h2>
    <p class="guide-p">
      Physical gold carries making charges and a buy-sell spread that is often 5–10% round trip. A gold ETF
      tracks the metal with a small expense ratio and no locker, but you need a demat account and it is priced in
      rupees like a share. Sovereign gold bonds paid interest and were redeemed at the metal price, but new
      tranches are issued on the government's schedule rather than continuously.
    </p>
    <p class="guide-p">
      Each has a different cost structure, and the differences are larger than most people assume over a decade.
      This page gives you the price; the choice is yours, and it depends on why you want the metal at all.
    </p>

    <div class="calc-notes">
      <h2>What this page is and is not</h2>
      <ul class="check-list">
        <li>{icon("check", "icon icon-sm")}<span><strong>What it is:</strong> a dated, sourced record of the gold price in dollars, in rupees, and through a listed ETF.</span></li>
        <li>{icon("alert", "icon icon-sm")}<span><strong>Not a jeweller's rate.</strong> No import duty, no premium, no making charges, no GST.</span></li>
        <li>{icon("alert", "icon icon-sm")}<span><strong>Not advice.</strong> Nothing here says whether gold is cheap or expensive, or whether to hold it.</span></li>
        <li>{icon("alert", "icon icon-sm")}<span><strong>Sources:</strong> gold futures and USD/INR from Yahoo Finance; ETF price from the NSE listing. Futures move continuously — this page is a snapshot with a date on it.</span></li>
      </ul>
      <p class="muted">
        Related: <a href="rates.html">every rate this site tracks</a> ·
        <a href="us-market.html">US market data</a> ·
        <a href="articles.html">articles</a>
      </p>
    </div>
  </div>
</section>
"""
