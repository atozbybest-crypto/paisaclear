"""Income-tax calculator page — mirrors the Income Tax Department's layout."""

from __future__ import annotations

import json

from .site import icon


def income_tax(rules: dict) -> str:
    data = json.dumps(rules, ensure_ascii=False).replace("</", "<\\/")

    return """
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="../index.html">Home</a></li><li aria-current="page">Income tax calculator</li>
    </ol></nav>
    <h1>Income tax calculator</h1>
    <p class="page-lede">
      Enter your net taxable income and see the tax, rebate, surcharge and cess. Individual, HUF, firm,
      company and local authority, for the 2026-27 tax year.
    </p>
    <p class="page-meta">As per the Income-tax Act, 2025 (amended by Finance Act, 2026)</p>
  </div>
</section>

<section class="section">
  <div class="shell it-layout">
    <form class="it-form" id="it-form">
      <div class="it-row">
        <label class="it-label" for="it-year">Tax year <span>*</span></label>
        <select id="it-year" class="it-input"><option>2026-27</option></select>
      </div>

      <div class="it-row">
        <label class="it-label" for="it-entity">Tax payer <span>*</span></label>
        <select id="it-entity" class="it-input">
          <option value="individual">Individual</option>
          <option value="huf">HUF</option>
          <option value="firm">Firm / LLP</option>
          <option value="company">Domestic company</option>
          <option value="local">Local authority</option>
        </select>
      </div>

      <div class="it-row" id="row-age">
        <label class="it-label" for="it-age">Category (age) <span>*</span></label>
        <select id="it-age" class="it-input">
          <option value="below60">Less than 60 years</option>
          <option value="senior">60 to 80 years</option>
          <option value="superSenior">Above 80 years</option>
        </select>
      </div>

      <div class="it-row" id="row-status">
        <label class="it-label" for="it-status">Residential status <span>*</span></label>
        <select id="it-status" class="it-input">
          <option value="resident">Resident</option>
          <option value="nonresident">Non-resident</option>
        </select>
      </div>

      <div class="it-row" id="row-regime">
        <label class="it-label" for="it-regime">Opting out of the new regime (s.202(1))? <span>*</span></label>
        <select id="it-regime" class="it-input">
          <option value="new">No — new regime</option>
          <option value="old">Yes — old regime</option>
        </select>
      </div>

      <div class="it-row" id="row-turnover">
        <label class="it-label" for="it-turnover">Annual turnover <span>*</span></label>
        <select id="it-turnover" class="it-input">
          <option value="small">Up to ₹400 crore</option>
          <option value="large">Above ₹400 crore</option>
        </select>
      </div>

      <div class="it-row">
        <label class="it-label" for="it-income">Net taxable income <span>*</span></label>
        <div class="it-input-wrap">
          <span class="it-rupee">₹</span>
          <input id="it-income" class="it-input" type="number" min="0" step="1000" placeholder="Net taxable income" inputmode="numeric">
        </div>
      </div>

      <div class="it-actions">
        <button class="btn btn-primary" type="submit">Calculate</button>
        <button class="btn btn-ghost" type="reset" id="it-reset">Reset</button>
      </div>
    </form>

    <aside class="it-results" aria-live="polite">
      <h2 class="it-results-title">Results</h2>
      <div id="it-output"></div>
    </aside>
  </div>
</section>

<section class="section section-tint">
  <div class="shell shell-narrow">
    <div class="calc-notes">
      <h2>What this covers, and what it doesn't</h2>
      <ul class="check-list">
        <li>""" + icon("check", "icon icon-sm") + """<span>Individual and HUF under both regimes, with the higher exemption for senior citizens under the old regime.</span></li>
        <li>""" + icon("check", "icon icon-sm") + """<span>Firm/LLP, domestic company and local authority at their flat rates, with surcharge and 4% cess.</span></li>
        <li>""" + icon("alert", "icon icon-sm") + """<span>It takes <strong>net taxable income</strong>, not gross salary — deduct exemptions and 80C-80U first. The <a href="salary.html">salary calculator</a> does that part for salaried people.</span></li>
        <li>""" + icon("alert", "icon icon-sm") + """<span>Marginal relief on surcharge is not applied, and co-operative societies, trusts and special-rate incomes (capital gains, 115BBH and similar) are not handled.</span></li>
      </ul>
      <p class="muted">
        Rule set dated """ + rules["asOf"] + """. Verify at the
        <a href="https://www.incometaxindia.gov.in/income-tax-calculator" target="_blank" rel="noopener noreferrer">Income Tax Department calculator</a>.
      </p>
      <p class="muted"><a href="salary.html">Salary and take-home calculator →</a> · <a href="savings.html">Savings calculator →</a></p>
    </div>
  </div>
</section>

<script type="application/json" id="it-rules">""" + data + """</script>
"""
