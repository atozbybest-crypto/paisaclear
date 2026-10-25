"""Product page for Dividend Champions — dividend history instead of a rate."""

from __future__ import annotations

from .site import breadcrumb, esc, icon


def _date(iso: str) -> str:
    try:
        from datetime import date
        d = date.fromisoformat(iso)
        return f"{d.day} {d.strftime('%b %Y')}"
    except ValueError:
        return iso


def page(ctx: dict, product: dict) -> str:
    category = ctx["categories_by_id"][product["category"]]
    dividends = product.get("dividends", [])

    rows = "".join(
        f"<tr><td>{esc(_date(d['date']))}</td><td>₹{d['amount']:.2f}</td></tr>"
        for d in dividends
    )

    facts = [
        ("Company", esc(product["name"])),
        ("NSE symbol", esc(product.get("symbol", ""))),
        ("Sector", esc(product.get("sector") or "Not published in a verifiable source")),
        ("Dividend streak", f"{product.get('streakYears', 0)} consecutive years"),
        ("Series above", f"Last {len(dividends)} payments"),
    ]
    fact_rows = "".join(
        f'<div class="fact-row"><dt>{label}</dt><dd>{value}</dd></div>' for label, value in facts
    )

    sources = "".join(
        f'<li><a href="{esc(s["url"])}" target="_blank" rel="noopener noreferrer">{esc(s["label"])}'
        f'<span class="ext" aria-hidden="true">↗</span></a></li>'
        for s in product.get("sources", [])
    )

    return f"""
<section class="page-head">
  <div class="shell">
    {breadcrumb([("Home", "../index.html"), ("All products", "../browse.html"),
                 (category["name"], f"../categories/{category['slug']}.html"), (product["name"], "")])}
    <div class="prod-badges">
      <span class="chip chip-conditional">Market-linked</span>
      <span class="chip chip-risk-high">High risk</span>
      <span class="pcard-cat">{esc(category["short"])}</span>
    </div>
    <h1>{esc(product["name"])}</h1>
    <p class="page-lede">{esc(product.get("oneLiner", ""))}</p>
    <p class="page-meta">Dividend payments as recorded · last verified {esc(product["lastVerified"])}</p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="split">
      <div class="split-main">
        <h2 class="subhead">The last {len(dividends)} dividend payments</h2>
        <div class="cmp-wrap"><table class="cmp-table">
          <thead><tr><th scope="col">Ex-date</th><th scope="col">Amount per share</th></tr></thead>
          <tbody>{rows}</tbody>
        </table></div>
        <p class="guide-src">
          Dates and amounts from Yahoo Finance for {esc(product.get("symbol", ""))}.NS. Indian companies
          usually pay one or two dividends a year rather than quarterly, so the gaps between these rows are
          not equal.
        </p>

        <h2 class="guide-h2">What a streak does and does not mean</h2>
        <p class="guide-p">
          {product.get("streakYears", 0)} consecutive years of paying a dividend says the board has chosen to
          return cash every year for a long time. It does not say the next one is coming, or that the amount
          will hold. A company can cut a dividend in a bad year and keep the historic record intact.
        </p>
        <p class="guide-p">
          Dividends are quoted per share. What you actually receive depends on how many shares you hold, and
          the share price moves independently of the payout — a 4% dividend on a stock that fell 20% is not
          income, it's a smaller loss.
        </p>

        <h2 class="guide-h2">Official sources</h2>
        <ul class="source-links">{sources}</ul>
      </div>

      <aside class="split-aside">
        <div class="aside-card">
          <h2>Key facts</h2>
          <dl class="fact-list">{fact_rows}</dl>
        </div>
        <div class="aside-card">
          <h2>Check before you decide</h2>
          <ul class="check-list">
            {''.join(f'<li>{icon("check", "icon icon-sm")}<span>{esc(c)}</span></li>' for c in product.get("check", []))}
          </ul>
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
        <li>{icon("alert", "icon icon-sm")}<span>Not a recommendation. A long dividend record is history, not a forecast.</span></li>
        <li>{icon("alert", "icon icon-sm")}<span>Not investment advice, and not a view on whether the shares are cheap.</span></li>
        <li>{icon("check", "icon icon-sm")}<span>Payment dates come from Yahoo Finance; streak length comes from a list supplied to PaisaClear and is not independently verified.</span></li>
      </ul>
      <p class="muted"><a href="../categories/dividend-champions.html">All Dividend Champions →</a></p>
    </div>
  </div>
</section>
"""
