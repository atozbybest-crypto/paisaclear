"""Dividend articles for the five companies Google already shows us for.

Each page is built from that company's own payment record plus a written
analysis of what the record does and does not show. The table is the data; the
paragraphs are the judgement.
"""

from __future__ import annotations

from .site import esc, icon

ANALYSIS = {
    "ADANIENT": {
        "context": "Adani Enterprises is the group's incubator: airports, roads, green hydrogen, data centres and mining, most of it built rather than bought. Companies in that phase consume cash, so a small dividend is the logical policy, not a stingy one.",
        "slug": "dividend-adani-enterprises",
        "title": "Adani Enterprises dividend history: 25 years of small payouts",
        "lede": "Adani Enterprises has paid a dividend every year since 2002 — but the amount is a rounding error "
                "against the share price. The record is real; the income is not.",
        "angle": [
            "The payout has grown slowly: ₹0.97 in 2021 to ₹1.30 in 2026, a rise of about 34% over five years "
            "while the business expanded far faster than that. This is a company that keeps its cash for "
            "building ports, airports, roads and data centres rather than distributing it.",
            "That is not a criticism — a growing conglomerate should reinvest. It does mean the dividend is a "
            "signal of consistency rather than a source of income. Anyone buying this for yield would be "
            "misreading the record.",
        ],
        "watch": "The dividend policy follows the group's capital expenditure cycle. A year of heavy investment "
                 "can keep the payout flat for several years without anything being wrong.",
    },
    "AMBUJACEM": {
        "context": 'Cement earnings move with construction demand, fuel costs and regional pricing power. Ambuja operates in the north and west, where capacity additions have been heavy — which is why the payout has flattened while plants are being built.',
        "slug": "dividend-ambuja-cements",
        "title": "Ambuja Cements dividend history: the cut inside a 25-year record",
        "lede": "Ambuja has paid every year since 2002, yet its dividend has fallen from ₹6.30 to ₹2.00. A streak "
                "counts years with a payment — it does not promise the amount holds.",
        "angle": [
            "The clearest example on this site of why a streak is not a yield. In 2022 the company paid ₹6.30; "
            "since 2024 it has paid ₹2.00, flat. The record survived. The income fell by two thirds.",
            "Cement is cyclical and the company has been through a change of control and a large capacity "
            "expansion. Dividends in this sector follow the capex cycle and the cement price cycle, not the "
            "length of the record.",
        ],
        "watch": "Watch capacity expansion announcements. A year of heavy plant building usually means a flat "
                 "or lower payout, whatever the streak says.",
    },
    "ASIANPAINT": {
        "context": 'Decorative paints is a high-margin, distribution-heavy business. Asian Paints built its position on a dealer network that competitors have spent a decade trying to replicate, and the payout has historically tracked that profitability rather than growth spending.',
        "slug": "dividend-asian-paints",
        "title": "Asian Paints dividend history: two payments a year, and what they show",
        "lede": "Asian Paints pays twice a year — a final dividend after results and an interim later — which is "
                "why its payment history looks denser than most Indian companies.",
        "angle": [
            "The pattern matters more than any single figure: ₹28.15 final in 2024, ₹4.25 interim in November "
            "2024, ₹20.55 final in 2025, ₹4.50 interim, ₹23.00 final in June 2026 and ₹5.75 in November 2026. "
            "The final dividend carries most of the payout; the interim is a top-up.",
            "Total payout has been broadly flat to slightly lower over three years, in a period when the company "
            "faced new competition in decorative paints. That is the number to watch, not the streak.",
        ],
        "watch": "The two-payment structure means a single year's tally can look volatile when you only look at "
                 "one payment. Add the final and the interim together before comparing years.",
    },
    "IOC": {
        "context": "Indian Oil refines, pipelines and retails fuel across the country, with a fourth of India's refining capacity. Its dividend is a function of refining spreads, inventory gains and the government's compensation for selling cooking fuel below cost.",
        "slug": "dividend-indian-oil",
        "title": "Indian Oil dividend history: the longest streak on this site",
        "lede": "Indian Oil has paid a dividend for 30 consecutive years — the longest record we track — and the "
                "amount has ranged from ₹1.25 to ₹7.00 in the last three years alone.",
        "angle": [
            "Refining margins decide this dividend. When crude spreads are wide and the rupee is stable, the "
            "payout is generous: ₹7.00 in July 2024. When margins compress, it falls to ₹1.25 by August 2026. "
            "The record never broke; the income halved and halved again.",
            "As a public-sector refiner, the company also balances dividend policy against the government's "
            "capital needs. That makes the payout partly a policy decision rather than purely a commercial one.",
        ],
        "watch": "Refining margins and any compensation mechanism for under-recoveries on cooking fuel. Both "
                 "move the dividend more than the streak does.",
    },
    "NTPC": {
        "context": "NTPC generates roughly a fifth of India's electricity, mostly coal with a growing renewable book. Returns are regulated, which is why the payout is steadier than any other company on this list — and why the upside is capped in the same way.",
        "slug": "dividend-ntpc",
        "title": "NTPC dividend history: steady payouts from a regulated business",
        "lede": "NTPC has paid a dividend for 22 straight years, and unlike most of the companies here the amount "
                "has been remarkably stable — ₹2.50 to ₹3.50 across the last two years.",
        "angle": [
            "Power generation earns a regulated return on equity, which makes cash flow predictable and the "
            "dividend correspondingly steady. That is the structural reason this record looks calmer than a "
            "refiner's or a cement maker's.",
            "The risk sits in the other direction: regulated returns cap the upside, and the company's capital "
            "expenditure on renewables decides how much cash is left for shareholders in any year.",
        ],
        "watch": "Regulated equity base and capex guidance. The dividend follows the first and is constrained by "
                 "the second.",
    },
}

THEMES = {
    "ADANIENT": "Trading - Minerals",
    "AMBUJACEM": "Cement",
    "ASIANPAINT": "Paints",
    "IOC": "Refining and marketing",
    "NTPC": "Power generation",
}


def _when(iso: str) -> str:
    from datetime import date
    try:
        d = date.fromisoformat(iso)
        return f"{d.day} {d.strftime('%b %Y')}"
    except (TypeError, ValueError):
        return iso


def article(record: dict) -> str:
    symbol = record["symbol"]
    meta = ANALYSIS[symbol]
    divs = record.get("dividends", [])
    amounts = [d["amount"] for d in divs]
    low, high = (min(amounts), max(amounts)) if amounts else (0, 0)
    latest = divs[0] if divs else {"date": "", "amount": 0}

    rows = "".join(
        f"<tr><td>{_when(d['date'])}</td><td class='mg-num'>₹{d['amount']:.2f}</td></tr>" for d in divs
    )

    angle = "".join(f"<p class='guide-p'>{esc(p)}</p>" for p in meta["angle"])
    context = meta.get("context", "")

    # computed statistics: unique to this company, no writing required
    total = sum(amounts)
    avg = total / len(amounts) if amounts else 0
    by_year = {}
    for d in divs:
        year = d["date"][:4]
        by_year[year] = by_year.get(year, 0) + d["amount"]
    year_rows = "".join(
        f"<tr><td>{y}</td><td class='mg-num'>₹{by_year[y]:.2f}</td></tr>"
        for y in sorted(by_year, reverse=True)
    )
    hundred = round(sum(by_year.values()) / max(1, len(by_year)) * 100)

    return f"""
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="index.html">Home</a></li>
      <li><a href="dividend-history.html">Dividend history</a></li>
      <li aria-current="page">{esc(record['name'])}</li>
    </ol></nav>
    <h1>{esc(meta['title'])}</h1>
    <p class="page-lede">{esc(meta['lede'])}</p>
    <p class="page-meta">
      {esc(record['symbol'])} · {esc(record.get('sector') or THEMES.get(symbol, 'Listed company'))} ·
      {record['streakYears']} consecutive years of payments
    </p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="split">
      <div class="split-main">
        <h2 class="subhead">The last {len(divs)} payments</h2>
        <div class="cmp-wrap"><table class="cmp-table">
          <thead><tr><th scope="col">Ex-date</th><th scope="col">Dividend per share</th></tr></thead>
          <tbody>{rows}</tbody>
        </table></div>
        <p class="guide-src">
          Dates and amounts from public dividend records. Between the low of ₹{low:.2f} and the high of
          ₹{high:.2f}, the record shows how much the payout moves from year to year.
        </p>

        <h2 class="guide-h2">What the record shows</h2>
        <p class="guide-p">{esc(context)}</p>
        {angle}

        <h2 class="guide-h2">The arithmetic</h2>
        <p class="guide-p">
          Across these {len(divs)} payments the company has paid a total of <strong>₹{total:.2f} per share</strong>
          — an average of ₹{avg:.2f} each time, with a low of ₹{low:.2f} and a high of ₹{high:.2f}. On a holding
          of 100 shares, that is about ₹{hundred} a year at the average rate, before tax.
        </p>
        <div class="cmp-wrap"><table class="cmp-table">
          <thead><tr><th scope="col">Calendar year</th><th scope="col">Total paid per share</th></tr></thead>
          <tbody>{year_rows}</tbody>
        </table></div>
        <p class="guide-src">
          Calendar-year totals, summed from the ex-dates above. A year with one payment and a year with two are
          not comparable until you look at this column rather than the individual payments.
        </p>

        <h2 class="guide-h2">What it does not tell you</h2>
        <p class="guide-p">
          A streak counts years in which <em>something</em> was paid. It says nothing about whether the next
          payment is safe. Two numbers decide that: the payout ratio against earnings, and free cash flow
          against the dividend. If the payout exceeds free cash flow for two years running, the record is being
          funded by the balance sheet.
        </p>
        <p class="guide-p">{esc(meta['watch'])}</p>

        <h2 class="guide-h2">Tax</h2>
        <p class="guide-p">
          Dividends are taxed at your slab. The company deducts TDS above ₹5,000 in a year, and you claim the
          credit when you file. In the 30% slab a ₹1,000 dividend leaves about ₹688 — which is why comparing a
          dividend yield with a tax-free small-savings rate needs the post-tax number, not the headline.
        </p>

        <h2 class="guide-h2">Related</h2>
        <ul class="check-list">
          <li>{icon("check", "icon icon-sm")}<span><a href="dividend-history.html">Dividend history of all {78} companies</a> on this site.</span></li>
          <li>{icon("check", "icon icon-sm")}<span><a href="dividend-streak.html">What a 25-year dividend streak actually predicts</a>.</span></li>
          <li>{icon("check", "icon icon-sm")}<span><a href="ppf-vs-fd-vs-nsc-tax.html">The after-tax comparison</a> that decides whether a dividend beats a tax-free rate.</span></li>
        </ul>
      </div>

      <aside class="split-aside">
        <div class="aside-card">
          <h2>At a glance</h2>
          <dl class="fact-list">
            <div class="fact-row"><dt>Streak</dt><dd>{record['streakYears']} years</dd></div>
            <div class="fact-row"><dt>Latest payment</dt><dd>₹{latest['amount']:.2f} on {_when(latest['date'])}</dd></div>
            <div class="fact-row"><dt>Range (10 payments)</dt><dd>₹{low:.2f} – ₹{high:.2f}</dd></div>
            <div class="fact-row"><dt>Sector</dt><dd>{esc(record.get('sector') or THEMES.get(symbol, '—'))}</dd></div>
          </dl>
        </div>
        <div class="aside-card">
          <h2>Source</h2>
          <p class="aside-note">
            <a href="https://finance.yahoo.com/quote/{esc(symbol)}.NS/history" target="_blank" rel="noopener noreferrer">
              {esc(symbol)} dividend history ↗</a>
          </p>
        </div>
      </aside>
    </div>
  </div>
</section>
"""


SLUGS = {k: v["slug"] for k, v in ANALYSIS.items()}
TITLES = {k: v["title"] for k, v in ANALYSIS.items()}
LEDES = {k: v["lede"] for k, v in ANALYSIS.items()}
