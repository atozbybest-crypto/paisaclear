"""Emergency-fund and retirement planners.

Both are arithmetic on figures the visitor enters. Nothing is assumed and
nothing is recommended: the product list shows what their own numbers can
already reach.
"""

from __future__ import annotations

import json

from .site import icon


def _catalog(products: list) -> list:
    rows = []
    for product in products:
        minimum = product.get("minInvestment")
        if not isinstance(minimum, int):
            continue
        rows.append({
            "s": product["slug"],
            "n": product["name"],
            "p": product["providerShort"],
            "c": product["category"],
            "r": product["returnType"],
            "m": minimum,
        })
    rows.sort(key=lambda r: r["m"])
    return rows


def plan_page(products: list) -> str:
    data = json.dumps(_catalog(products), ensure_ascii=False).replace("</", "<\\/")

    return """
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="../index.html">Home</a></li><li aria-current="page">Planners</li>
    </ol></nav>
    <h1>Emergency fund and retirement</h1>
    <p class="page-lede">
      Every figure below is yours to set — we do not assume a savings rate, a return or how many months of
      cover you need. The result is the arithmetic of your own numbers, and the products shown are only
      those your amount can already reach.
    </p>
    <p class="page-meta">Illustrative arithmetic · not financial advice</p>
  </div>
</section>

<section class="section">
  <div class="shell calc-layout">
    <form class="calc-form" id="plan-form" novalidate>
      <div class="seg-toggle" role="group" aria-label="Which planner">
        <button type="button" data-plan-tab="emergency" class="is-on">Emergency fund</button>
        <button type="button" data-plan-tab="retire">Retirement</button>
      </div>

      <fieldset class="calc-group" data-only="emergency">
        <legend>Your emergency fund</legend>
        <div class="calc-grid">
          <label class="field">
            <span class="field-label">Essential monthly expenses</span>
            <span class="field-input"><input id="e-expenses" type="number" min="0" placeholder="Monthly"><span class="field-suffix">₹</span></span>
          </label>
          <label class="field">
            <span class="field-label">Months of cover you want</span>
            <span class="field-input"><input id="e-months" type="number" min="1" max="36" placeholder="Months"><span class="field-suffix">months</span></span>
          </label>
          <label class="field">
            <span class="field-label">Already set aside</span>
            <span class="field-input"><input id="e-saved" type="number" min="0" placeholder="0"><span class="field-suffix">₹</span></span>
          </label>
          <label class="field">
            <span class="field-label">You can put away each month</span>
            <span class="field-input"><input id="e-monthly" type="number" min="0" placeholder="Monthly"><span class="field-suffix">₹</span></span>
          </label>
        </div>
      </fieldset>

      <fieldset class="calc-group" data-only="retire">
        <legend>Your retirement numbers</legend>
        <div class="calc-grid">
          <label class="field">
            <span class="field-label">Your age now</span>
            <span class="field-input"><input id="r-age" type="number" min="15" max="80" placeholder="Age"><span class="field-suffix">years</span></span>
          </label>
          <label class="field">
            <span class="field-label">Age you want to stop</span>
            <span class="field-input"><input id="r-retire" type="number" min="30" max="85" placeholder="Retire at"><span class="field-suffix">years</span></span>
          </label>
          <label class="field">
            <span class="field-label">Monthly expenses today</span>
            <span class="field-input"><input id="r-expenses" type="number" min="0" placeholder="Monthly"><span class="field-suffix">₹</span></span>
          </label>
          <label class="field">
            <span class="field-label">Inflation you expect</span>
            <span class="field-input"><input id="r-inflation" type="number" min="0" max="20" step="0.1" placeholder="%"><span class="field-suffix">% a year</span></span>
          </label>
          <label class="field">
            <span class="field-label">Return before retirement</span>
            <span class="field-input"><input id="r-grow" type="number" min="0" max="30" step="0.1" placeholder="%"><span class="field-suffix">% a year</span></span>
          </label>
          <label class="field">
            <span class="field-label">Return after retirement</span>
            <span class="field-input"><input id="r-post" type="number" min="0" max="30" step="0.1" placeholder="%"><span class="field-suffix">% a year</span></span>
          </label>
          <label class="field">
            <span class="field-label">Years you want covered</span>
            <span class="field-input"><input id="r-years" type="number" min="1" max="50" placeholder="Years"><span class="field-suffix">years</span></span>
          </label>
          <label class="field">
            <span class="field-label">Saved so far</span>
            <span class="field-input"><input id="r-saved" type="number" min="0" placeholder="0"><span class="field-suffix">₹</span></span>
          </label>
          <label class="field">
            <span class="field-label">Investing each month</span>
            <span class="field-input"><input id="r-monthly" type="number" min="0" placeholder="Monthly"><span class="field-suffix">₹</span></span>
          </label>
        </div>
      </fieldset>
    </form>

    <aside class="calc-results" id="plan-results">
      <div id="plan-output"></div>
    </aside>
  </div>
</section>

<section class="section section-tint">
  <div class="shell shell-narrow">
    <div class="calc-notes">
      <h2>How to read these numbers</h2>
      <ul class="check-list">
        <li>""" + icon("check", "icon icon-sm") + """<span>Every input is yours. Change the months of cover, the returns, the inflation — the result follows immediately.</span></li>
        <li>""" + icon("check", "icon icon-sm") + """<span>The product list is filtered by minimum investment only: your amount either reaches it or it doesn't.</span></li>
        <li>""" + icon("alert", "icon icon-sm") + """<span>No return is promised. A 10% assumption is an assumption, and a bad year is not averaged away.</span></li>
        <li>""" + icon("alert", "icon icon-sm") + """<span>Tax is ignored. So are charges, exit loads and the years when a fund falls.</span></li>
      </ul>
      <p class="muted"><a href="spending.html">Spending planner →</a> · <a href="savings.html">Savings calculator →</a> · <a href="salary.html">Salary calculator →</a></p>
    </div>
  </div>
</section>

<script type="application/json" id="plan-catalog">""" + data + """</script>
"""
