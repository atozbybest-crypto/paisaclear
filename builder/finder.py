"""Smart Scheme Finder — filters the catalogue by what the visitor needs."""

from __future__ import annotations

import json

from .site import icon


def _catalog(products: list) -> list:
    rows = []
    for product in products:
        rows.append({
            "s": product["slug"],
            "n": product["name"],
            "p": product["providerShort"],
            "c": product["category"],
            "r": product["returnType"],
            "l": product.get("riskLevel", ""),
            "m": product.get("minInvestment") if isinstance(product.get("minInvestment"), int) else None,
            "k": bool(product.get("lockIn")),
            "y": (product.get("payoutFrequency") or "").lower(),
            "t": product.get("tenure") or "",
            "o": product.get("collections", []),
            "b": product.get("bucket", ""),
        })
    return rows


def finder(products: list) -> str:
    data = json.dumps(_catalog(products), ensure_ascii=False).replace("</", "<\\/")

    return """
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="index.html">Home</a></li><li aria-current="page">Scheme finder</li>
    </ol></nav>
    <h1>PaisaDiscover</h1>
    <p class="page-lede">
      Answer five questions and we will narrow the catalogue to products whose terms match. Each result says
      why it appeared — and none of them is a recommendation.
    </p>
    <p class="page-meta">Filters only · not financial advice</p>
  </div>
</section>

<section class="section">
  <div class="shell finder-layout">
    <form class="finder-form" id="finder-form">
      <div class="finder-q">
        <label class="finder-label" for="f-goal">1. What should the money do?</label>
        <select id="f-goal" class="it-input">
          <option value="income">Pay me a regular income</option>
          <option value="grow">Grow over several years</option>
          <option value="tax">Save tax</option>
          <option value="safe">Stay safe and reachable</option>
          <option value="child">Build for a child's future</option>
        </select>
      </div>

      <div class="finder-q">
        <label class="finder-label" for="f-amount">2. How much can you start with?</label>
        <div class="it-input-wrap">
          <span class="it-rupee">₹</span>
          <input id="f-amount" class="it-input" type="number" min="0" step="500" placeholder="Amount">
        </div>
      </div>

      <div class="finder-q">
        <label class="finder-label" for="f-lock">3. How long can it stay locked?</label>
        <select id="f-lock" class="it-input">
          <option value="none">It should stay reachable</option>
          <option value="short">Up to a year is fine</option>
          <option value="mid">One to five years</option>
          <option value="long">Five years or more</option>
        </select>
      </div>

      <div class="finder-q">
        <label class="finder-label" for="f-risk">4. How much movement can you accept?</label>
        <select id="f-risk" class="it-input">
          <option value="none">None — the value should not fall</option>
          <option value="some">Some ups and downs</option>
          <option value="any">Market swings are fine</option>
        </select>
      </div>

      <div class="finder-q">
        <label class="finder-label" for="f-tax">5. Do you need a tax deduction?</label>
        <select id="f-tax" class="it-input">
          <option value="no">No, or not sure</option>
          <option value="yes">Yes — 80C matters to me</option>
        </select>
      </div>

      <div class="it-actions">
        <button class="btn btn-primary" type="submit">Show matching products</button>
        <button class="btn btn-ghost" type="reset" id="finder-reset">Reset</button>
      </div>
    </form>

    <div class="finder-results" id="finder-results" aria-live="polite">
      <p class="finder-placeholder">Answer the five questions and press the button.</p>
    </div>
  </div>
</section>

<section class="section section-tint">
  <div class="shell shell-narrow">
    <div class="calc-notes">
      <h2>How this works, and what it is not</h2>
      <ul class="check-list">
        <li>""" + icon("check", "icon icon-sm") + """<span>It filters on facts we hold: minimum investment, lock-in, payout frequency, risk type and tax treatment.</span></li>
        <li>""" + icon("check", "icon icon-sm") + """<span>Every result states the reason it appeared, so you can disagree with the logic rather than trust a black box.</span></li>
        <li>""" + icon("alert", "icon icon-sm") + """<span>It does not know your income, debts, dependants or goals. It cannot tell you what to buy, and it does not try.</span></li>
        <li>""" + icon("alert", "icon icon-sm") + """<span>A product appearing here is not a suitability judgement. Read the tax, lock-in and risk sections on its page.</span></li>
      </ul>
      <p class="muted"><a href="browse.html">Browse everything →</a> · <a href="calculators/savings.html">Savings calculator →</a></p>
    </div>
  </div>
</section>

<script type="application/json" id="finder-catalog">""" + data + """</script>
"""
