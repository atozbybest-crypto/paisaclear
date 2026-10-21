"""The 'start here' page — the landing page for social and ad traffic."""

from __future__ import annotations

from .site import esc, icon


def start_here(ctx: dict) -> str:
    cats = ctx["categories"]
    counts = ctx["counts_by_category"]
    total = len(ctx["products"])

    cat_cards = "".join(
        f"""<a class="start-card" href="categories/{esc(c['slug'])}.html">
  <span class="start-count">{counts.get(c['id'], 0)} products</span>
  <span class="start-name">{esc(c['name'])}</span>
  <span class="start-desc">{esc(c['tagline'])}</span>
</a>"""
        for c in cats
    )

    return f"""
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="index.html">Home</a></li><li aria-current="page">Start here</li>
    </ol></nav>
    <h1>Start here</h1>
    <p class="page-lede">
      {total} Indian financial products, explained in plain language. Three routes in: pick what you are
      trying to do, look up a product, or work out a number first.
    </p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="start-grid">
      <a class="start-route" href="browse.html">
        <span class="start-step">1</span>
        <h2>Look something up</h2>
        <p>Search or filter the whole catalogue by category, risk, lock-in, payout or minimum investment.</p>
        <span class="start-cta">Browse all products {icon("arrow", "icon icon-sm")}</span>
      </a>
      <a class="start-route" href="calculators/salary.html">
        <span class="start-step">2</span>
        <h2>Work out a number</h2>
        <p>Take-home pay, savings growth, loan EMI, an emergency fund, or what retirement would need.</p>
        <span class="start-cta">Open the calculators {icon("arrow", "icon icon-sm")}</span>
      </a>
      <a class="start-route" href="how-we-work.html">
        <span class="start-step">3</span>
        <h2>Check how we work</h2>
        <p>Where every figure comes from, how a record is reviewed, and what this site deliberately does not do.</p>
        <span class="start-cta">Read the method {icon("arrow", "icon icon-sm")}</span>
      </a>
    </div>
  </div>
</section>

<section class="section section-tint">
  <div class="shell">
    {'' if not cats else ''}
    <h2 class="section-title">Or pick a category</h2>
    <div class="start-grid start-grid-cats">{cat_cards}</div>
  </div>
</section>

<section class="section">
  <div class="shell shell-narrow">
    <h2 class="section-title">The one thing worth knowing first</h2>
    <p class="start-body">
      Indian financial products promise three different kinds of return, and mixing them up is where most
      beginners get hurt. A <strong>guaranteed</strong> product fixes the figure in a contract — the risk is
      that the rate is low and your money is locked. A <strong>conditional</strong> product pays only if
      conditions are met. A <strong>market-linked</strong> product has no promised return at all, and its value
      moves with a market you do not control.
    </p>
    <p class="start-body">
      Every product page here says which of the three applies, when the figure was last checked, and where it
      came from. If a figure varies by tenure or provider, we link to the provider instead of inventing one.
    </p>
    <p style="margin-top:22px">
      <a class="btn btn-primary" href="browse.html">Browse the catalogue</a>
      <a class="btn btn-ghost" href="how-we-work.html#returns">The three return types</a>
    </p>
  </div>
</section>
"""
