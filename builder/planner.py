"""The spending planner page.

A tracker, not advice: it reports what the user logged and lists products whose
minimum they can already meet. All state lives in the browser's localStorage.
"""

from __future__ import annotations

import json

from .site import esc, icon


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
            "t": product.get("tenure") or "",
            "y": product.get("payout") or "",
        })
    rows.sort(key=lambda r: r["m"])
    return rows


def planner_page(products: list) -> str:
    data = json.dumps(_catalog(products), ensure_ascii=False).replace("</", "<\\/")

    return """
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="../index.html">Home</a></li><li aria-current="page">Spending planner</li>
    </ol></nav>
    <h1>Where the month goes</h1>
    <p class="page-lede">
      Put in what you have, log what you spend, and see which categories take the most. Everything stays in
      this browser — nothing is uploaded, and there is no account.
    </p>
    <p class="page-meta">Saved on this device only · a tracker, not financial advice</p>
  </div>
</section>

<section class="section">
  <div class="shell planner-layout">

    <div class="planner-main">
      <fieldset class="calc-group">
        <legend>Starting point</legend>
        <div class="calc-grid">
          <label class="field">
            <span class="field-label">Money you have now</span>
            <span class="field-input"><input id="pl-start" type="number" min="0" placeholder="Amount"><span class="field-suffix">₹</span></span>
          </label>
          <label class="field">
            <span class="field-label">Expected monthly income</span>
            <span class="field-input"><input id="pl-income" type="number" min="0" placeholder="Optional"><span class="field-suffix">₹ optional</span></span>
          </label>
        </div>
      </fieldset>

      <form class="calc-group" id="expense-form">
        <legend>Add a spend</legend>
        <div class="calc-grid">
          <label class="field">
            <span class="field-label">Amount</span>
            <span class="field-input"><input id="pl-amount" type="number" min="1" step="0.01" required placeholder="0"><span class="field-suffix">₹</span></span>
          </label>
          <label class="field">
            <span class="field-label">Category</span>
            <span class="field-input">
              <select id="pl-category">
                <option>Rent</option>
                <option>Food and groceries</option>
                <option>Transport</option>
                <option>Bills and utilities</option>
                <option>Shopping</option>
                <option>Health</option>
                <option>Education</option>
                <option>Entertainment</option>
                <option>Family and gifts</option>
                <option>Other</option>
              </select>
            </span>
          </label>
          <label class="field">
            <span class="field-label">Date</span>
            <span class="field-input"><input id="pl-date" type="date"></span>
          </label>
          <label class="field">
            <span class="field-label">Note</span>
            <span class="field-input"><input id="pl-note" type="text" placeholder="optional"></span>
          </label>
        </div>
        <div class="calc-actions">
          <button class="btn btn-primary" type="submit">Add spend</button>
          <button class="btn btn-ghost" type="button" id="pl-clear">Clear all</button>
        </div>
      </form>

      <div class="calc-group">
        <legend>Logged spends</legend>
        <p class="planner-empty" id="pl-empty">Nothing logged yet. Add your first spend above.</p>
        <ul class="expense-list" id="pl-list"></ul>
      </div>
    </div>

    <aside class="calc-results">
      <div class="planner-summary">
        <p class="calc-headline-label">Left of your money</p>
        <p class="calc-headline-value" id="pl-balance">₹0</p>
        <p class="calc-headline-note" id="pl-note-line">Enter what you have to begin.</p>
        <div class="calc-totals">
          <div class="calc-total-row"><span>Starting amount</span><strong id="pl-start-out">₹0</strong></div>
          <div class="calc-total-row"><span>Total spent</span><strong id="pl-spent">₹0</strong></div>
          <div class="calc-total-row"><span>Average per day</span><strong id="pl-daily">₹0</strong></div>
          <div class="calc-total-row is-grand"><span>Next 30 days at this pace</span><strong id="pl-proj">₹0</strong></div>
        </div>
      </div>

      <div class="planner-breakdown">
        <h3>By category</h3>
        <div id="pl-bars"><p class="planner-empty">No spends yet.</p></div>
      </div>

      <div class="planner-suggest" id="pl-suggest" hidden>
        <h3>Products your balance can already start</h3>
        <p class="planner-suggest-note" id="pl-suggest-note"></p>
        <ul class="suggest-list" id="pl-suggest-list"></ul>
      </div>
    </aside>
  </div>
</section>

<section class="section section-tint">
  <div class="shell shell-narrow">
    <div class="calc-notes">
      <h2>What this is, and isn't</h2>
      <ul class="check-list">
        <li>""" + icon("check", "icon icon-sm") + """<span>Your entries are stored in this browser only. Nothing is sent anywhere, and there is no account.</span></li>
        <li>""" + icon("alert", "icon icon-sm") + """<span>Clearing your browser data deletes the list — there is no copy on a server.</span></li>
        <li>""" + icon("alert", "icon icon-sm") + """<span>The product list shows what your balance can reach by minimum investment. It is not a recommendation, and it ignores your goals, tax position and risk capacity.</span></li>
        <li>""" + icon("alert", "icon icon-sm") + """<span>Categories are a simple aid to seeing patterns, not a budget you have to keep.</span></li>
      </ul>
      <p class="muted"><a href="savings.html">Savings calculator →</a> · <a href="salary.html">Salary calculator →</a></p>
    </div>
  </div>
</section>

<script type="application/json" id="pl-catalog">""" + data + """</script>
"""
