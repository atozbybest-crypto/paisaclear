"""Dividend history — one indexable page that answers the queries Google is
already testing us for ("<company> dividend", "dividend history India").

Per-company pages stay noindexed until AdSense is approved; this page carries
the data in one place: every company, its streak, and its last ten payments.
"""

from __future__ import annotations

from .site import esc


def _when(iso: str) -> str:
    try:
        from datetime import date
        d = date.fromisoformat(iso)
        return f"{d.day} {d.strftime('%b %Y')}"
    except (TypeError, ValueError):
        return iso or "—"


ARTICLE_SLUGS = {
    "ADANIENT": "dividend-adani-enterprises", "AMBUJACEM": "dividend-ambuja-cements",
    "ASIANPAINT": "dividend-asian-paints", "IOC": "dividend-indian-oil", "NTPC": "dividend-ntpc",
}


def page(records: list[dict]) -> str:
    records = sorted(records, key=lambda r: -r.get("streakYears", 0))
    total_payments = sum(len(r.get("dividends", [])) for r in records)

    rows = []
    for r in records:
        divs = r.get("dividends", [])
        last = divs[0] if divs else None
        recent = divs[:3]
        cells = "".join(
            f"<td class='mg-num'>{_when(d['date'])}<span class='dh-amt'>₹{d['amount']:.2f}</span></td>"
            for d in recent
        )
        while recent and len(recent) < 3:
            recent.append(None)
            cells += "<td class='mg-num muted'>—</td>"
        rows.append(
            f"<tr id='{esc(r['symbol'].lower())}'>"
            f"<td><span class='mg-co'>"
            + (f"<a href='{ARTICLE_SLUGS[r['symbol']]}.html'>{esc(r['name'])}</a>"
               if r["symbol"] in ARTICLE_SLUGS else esc(r["name"]))
            + "</span>"
            f"<span class='mg-sector'>{esc(r['symbol'])} · {esc(r.get('sector') or 'Listed company')}</span></td>"
            f"<td class='mg-num'>{r.get('streakYears', 0)}</td>"
            f"{cells}"
            f"<td class='mg-num small'>{_when(last['date']) if last else '—'}</td>"
            f"</tr>"
        )

    return f"""
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="index.html">Home</a></li><li aria-current="page">Dividend history</li>
    </ol></nav>
    <h1>Dividend history of {len(records)} Indian companies</h1>
    <p class="page-lede">
      Every company on PaisaClear with a long record of paying dividends, with the streak, the sector and the
      most recent payments. Companies like Adani Enterprises, Ambuja Cements, Asian Paints, Indian Oil and NTPC
      appear in the table below with the dates and amounts of their last ten dividends.
    </p>
    <p class="page-meta">
      {len(records)} companies · {total_payments} recorded payments · dividends in rupees per share
    </p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="cmp-wrap">
      <table class="cmp-table dh-table">
        <thead><tr>
          <th scope="col">Company</th>
          <th scope="col">Streak (years)</th>
          <th scope="col">Latest payment</th>
          <th scope="col">Previous</th>
          <th scope="col">Before that</th>
          <th scope="col">Last paid</th>
        </tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </div>
    <p class="guide-src">
      Payment dates and amounts come from public dividend records; the streak is computed from those payments
      and states the window it was verified over on each company page. A long record is history, not a promise —
      a company can cut or skip a dividend in any year.
    </p>
  </div>
</section>

<section class="section section-tint">
  <div class="shell shell-narrow">
    <div class="calc-notes">
      <h2>How to read a dividend record</h2>
      <p class="guide-p">
        Three things matter more than the streak itself. <strong>The direction:</strong> are the amounts rising,
        flat or slipping? A company paying ₹2, ₹2, ₹2.5, ₹3 over a decade is growing the payout; one paying
        ₹5, ₹5, ₹4, ₹3 is shrinking it while the record stays intact.
      </p>
      <p class="guide-p">
        <strong>The cover:</strong> dividends are paid from free cash flow, not from the record. A payout ratio
        above 80% of earnings leaves no room for a bad year. <strong>The price:</strong> a 4% dividend on a share
        that fell 20% is not income, it is a smaller loss.
      </p>
      <p class="guide-p">
        The full argument is in <a href="dividend-streak.html">what a 25-year dividend streak actually
        predicts</a>, and the tax treatment is in <a href="ppf-vs-fd-vs-nsc-tax.html">the after-tax
        comparison</a> — dividends are taxed at your slab.
      </p>
    </div>
  </div>
</section>
"""
