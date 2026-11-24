"""Gold price page — candlestick chart and ordered monthly tables."""

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


def _month(m: str) -> str:
    from datetime import date
    try:
        d = date.fromisoformat(m + "-01")
        return d.strftime("%b %Y")
    except ValueError:
        return m


def _candles(months: list[dict], count: int = 36) -> str:
    data = months[-count:]
    if len(data) < 3:
        return "<p class='muted'>Chart unavailable.</p>"

    w, h, pad_l, pad_r, pad_t, pad_b = 900, 360, 74, 16, 18, 42
    highs = [m["inr"]["h"] for m in data]
    lows = [m["inr"]["l"] for m in data]
    top, bottom = max(highs), min(lows)
    span = (top - bottom) or 1

    plot_w = w - pad_l - pad_r
    plot_h = h - pad_t - pad_b
    slot = plot_w / len(data)
    body_w = max(3.0, slot * 0.58)

    def y_of(value: float) -> float:
        return pad_t + (top - value) / span * plot_h

    parts = []
    # horizontal gridlines with rupee labels
    for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
        value = top - frac * span
        y = pad_t + frac * plot_h
        parts.append(f"<line x1='{pad_l}' y1='{y:.1f}' x2='{w - pad_r}' y2='{y:.1f}' "
                     f"stroke='#E7E1D2' stroke-width='1'/>")
        parts.append(f"<text x='{pad_l - 8}' y='{y + 4:.1f}' text-anchor='end' font-size='12' "
                     f"fill='#6B746E'>{_inr(value)}</text>")

    for i, m in enumerate(data):
        cx = pad_l + slot * (i + 0.5)
        o, hi, lo, c = m["inr"]["o"], m["inr"]["h"], m["inr"]["l"], m["inr"]["c"]
        up = c >= o
        colour = "#0F5132" if up else "#B42318"
        y_open, y_close, y_high, y_low = y_of(o), y_of(c), y_of(hi), y_of(lo)

        body_top = min(y_open, y_close)
        body_h = max(2.0, abs(y_close - y_open))
        tip = (f"{_month(m['m'])} · open {_inr(o)} · high {_inr(hi)} · low {_inr(lo)} · "
               f"close {_inr(c)} · ${m['usd']['c']:,.0f}/oz @ {m['fx']:.2f}")
        parts.append(
            f"<g><title>{tip}</title>"
            f"<line x1='{cx:.1f}' y1='{y_high:.1f}' x2='{cx:.1f}' y2='{y_low:.1f}' "
            f"stroke='{colour}' stroke-width='1.4'/>"
            f"<rect x='{cx - body_w / 2:.1f}' y='{body_top:.1f}' width='{body_w:.1f}' "
            f"height='{body_h:.1f}' fill='{colour}' rx='1'/>"
            f"<rect x='{cx - slot / 2:.1f}' y='{pad_t}' width='{slot:.1f}' height='{plot_h}' "
            f"fill='transparent'/></g>"
        )

    # x labels every 6th month
    for i, m in enumerate(data):
        if i % 6 == 0 or i == len(data) - 1:
            cx = pad_l + slot * (i + 0.5)
            parts.append(f"<text x='{cx:.1f}' y='{h - 14}' text-anchor='middle' font-size='12' "
                         f"fill='#6B746E'>{_month(m['m'])}</text>")

    return f"""
<figure class="gold-chart">
  <svg viewBox="0 0 {w} {h}" role="img" preserveAspectRatio="xMidYMid meet"
       aria-label="Monthly gold price in rupees per 10 grams, {_month(data[0]['m'])} to {_month(data[-1]['m'])}">
    <rect x="{pad_l}" y="{pad_t}" width="{plot_w}" height="{plot_h}" fill="#FBFAF5"/>
    {''.join(parts)}
  </svg>
  <figcaption>
    Each candle is one month: the vertical line spans that month's high and low, the body spans the open and
    close. Green means the month closed higher than it opened. Rupees per 10 grams, computed from dollar gold
    and the dollar–rupee rate — before import duty and dealer premium.
  </figcaption>
</figure>
"""


def page(data: dict) -> str:
    months = data.get("months", [])
    if not months:
        return "<section class='section'><div class='shell'><p class='muted'>Gold data unavailable.</p></div></section>"

    per10g = data.get("per10g", {})
    usd = data.get("usdPerOunce", {})
    fx = data.get("usdinr", {})
    latest = months[-1]

    # monthly table, newest first, with all four prices
    monthly_rows = "".join(
        f"<tr><td>{_month(m['m'])}</td>"
        f"<td class='mg-num'>{_inr(m['inr']['o'])}</td>"
        f"<td class='mg-num'>{_inr(m['inr']['h'])}</td>"
        f"<td class='mg-num'>{_inr(m['inr']['l'])}</td>"
        f"<td class='mg-num'><strong>{_inr(m['inr']['c'])}</strong></td>"
        f"<td class='mg-num small'>${m['usd']['c']:,.0f}</td>"
        f"<td class='mg-num small'>{m['fx']:.2f}</td></tr>"
        for m in months[-24:][::-1]
    )

    # year table from monthly closes
    by_year: dict[str, list[float]] = {}
    for m in months:
        by_year.setdefault(m["m"][:4], []).append(m["inr"]["c"])
    year_rows = "".join(
        f"<tr><td>{year}</td>"
        f"<td class='mg-num'>{_inr(sum(vals) / len(vals))}</td>"
        f"<td class='mg-num'>{_inr(min(vals))}</td>"
        f"<td class='mg-num'>{_inr(max(vals))}</td>"
        f"<td class='mg-num small'>{len(vals)}</td></tr>"
        for year, vals in sorted(by_year.items(), reverse=True)
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
      dollar–rupee rate, with a monthly candlestick history. Every figure carries the date it was observed.
    </p>
    <p class="page-meta">Fetched {_when(data.get('fetchedAt', ''))} · refreshed at 09:00 and 21:30 IST</p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="us-grid">
      <div class="us-card">
        <span class="us-name">Gold, per 10 grams</span>
        <strong class="us-value">{_inr(per10g.get('value'))}</strong>
        <span class="us-meta">reference conversion · {_when(per10g.get('asOf', ''))}</span>
      </div>
      <div class="us-card">
        <span class="us-name">This month</span>
        <strong class="us-value">{_inr(latest['inr']['c'])}</strong>
        <span class="us-meta">open {_inr(latest['inr']['o'])} ·
          high {_inr(latest['inr']['h'])} · low {_inr(latest['inr']['l'])}</span>
      </div>
      <div class="us-card">
        <span class="us-name">International, per troy ounce</span>
        <strong class="us-value">${usd.get('value', 0):,.2f}</strong>
        <span class="us-meta">1 month {usd.get('month', 0):+.2f}% · 1 year {usd.get('year', 0):+.2f}%</span>
      </div>
      <div class="us-card">
        <span class="us-name">US dollar / rupee</span>
        <strong class="us-value">₹{fx.get('value', 0):.2f}</strong>
        <span class="us-meta">as of {_when(fx.get('asOf', ''))}</span>
      </div>
    </div>
  </div>
</section>

<section class="section section-tint">
  <div class="shell">
    {_candles(months)}
  </div>
</section>

<section class="section">
  <div class="shell">
    <h2 class="subhead">Month by month, last 24 months</h2>
    <p class="table-note">
      The four price columns are <strong>rupees per 10 grams</strong>. The last two show the source figures used
      for the conversion: the dollar price of an ounce, and the dollar–rupee rate.
    </p>
    <div class="cmp-wrap"><table class="cmp-table table-grid">
      <thead><tr>
        <th scope="col">Month</th>
        <th scope="col" class="mg-num">Open<br><span class="th-unit">₹ per 10 g</span></th>
        <th scope="col" class="mg-num">High<br><span class="th-unit">₹ per 10 g</span></th>
        <th scope="col" class="mg-num">Low<br><span class="th-unit">₹ per 10 g</span></th>
        <th scope="col" class="mg-num">Close<br><span class="th-unit">₹ per 10 g</span></th>
        <th scope="col" class="mg-num">USD/oz</th>
        <th scope="col" class="mg-num">USD/INR</th>
      </tr></thead>
      <tbody>{monthly_rows}</tbody>
    </table></div>
    <p class="guide-src">
      Newest first. Open, high, low and close are the month's own prices in rupees per 10 grams; the last two
      columns are the source dollar price and exchange rate used for the conversion.
    </p>

    <h2 class="guide-h2">Year by year</h2>
    <div class="cmp-wrap"><table class="cmp-table table-grid">
      <thead><tr>
        <th scope="col">Year</th>
        <th scope="col" class="mg-num">Average close<br><span class="th-unit">₹ per 10 g</span></th>
        <th scope="col" class="mg-num">Lowest close<br><span class="th-unit">₹ per 10 g</span></th>
        <th scope="col" class="mg-num">Highest close<br><span class="th-unit">₹ per 10 g</span></th>
        <th scope="col" class="mg-num">Months</th>
      </tr></thead>
      <tbody>{year_rows}</tbody>
    </table></div>
    <p class="guide-src">
      Each figure is built from that year's monthly closing prices — so the "low" is the weakest month-end of
      the year, not the lowest price touched during it. The month count tells you how much of the year is
      included; the current year is partial.
    </p>

    <h2 class="guide-h2">What moves the rupee price</h2>
    <p class="guide-p">
      Three things, and only one of them is "gold" in the abstract. The <strong>dollar price</strong> of the
      metal moves with global demand, real interest rates and central-bank buying. The <strong>rupee</strong>
      moves independently: when the rupee weakens, the same dollar price buys fewer grams, so the Indian price
      rises even if gold does not move at all.
    </p>
    <p class="guide-p">
      The third is <strong>duty and premium</strong>. India imports almost all of its gold, and the landed price
      carries customs duty plus whatever dealers are charging on the day. In a festive week the premium can
      widen by a percent or more on its own — which is why the figure at the top of this page and the number at
      a jeweller's counter are not the same number.
    </p>

    <h2 class="guide-h2">Physical gold, an ETF, or a bond</h2>
    <p class="guide-p">
      Physical gold carries making charges and a buy-sell spread that is often 5–10% round trip. A gold ETF
      tracks the metal with a small expense ratio and no locker, but you need a demat account and it trades in
      rupees like a share. Sovereign gold bonds paid interest and were redeemed at the metal price, but new
      tranches appear on the government's schedule rather than continuously.
    </p>
    <p class="guide-p">
      Each has a different cost structure, and the differences are larger than most people assume over a
      decade. This page gives you the price; the choice is yours, and it depends on why you want the metal.
    </p>

    <div class="calc-notes">
      <h2>What this page is and is not</h2>
      <ul class="check-list">
        <li>{icon("check", "icon icon-sm")}<span><strong>What it is:</strong> a dated, sourced record of gold in dollars, in rupees, month by month.</span></li>
        <li>{icon("alert", "icon icon-sm")}<span><strong>Not a jeweller's rate.</strong> No import duty, no premium, no making charges, no GST.</span></li>
        <li>{icon("alert", "icon icon-sm")}<span><strong>Not advice.</strong> Nothing here says whether gold is cheap or expensive.</span></li>
        <li>{icon("alert", "icon icon-sm")}<span><strong>Sources:</strong> gold futures and USD/INR from Yahoo Finance. Monthly candles are that month's own open, high, low and close.</span></li>
      </ul>
      <p class="muted">
        Related: <a href="rates.html">every rate this site tracks</a> ·
        <a href="us-market.html">US market data</a> · <a href="articles.html">articles</a>
      </p>
    </div>
  </div>
</section>
"""
