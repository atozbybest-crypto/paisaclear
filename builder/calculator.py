"""The salary calculator page."""

from __future__ import annotations

import json

from .site import esc, icon, page


def _field(name: str, label: str, value: str, *, suffix: str = "", hint: str = "", kind: str = "number") -> str:
    hint_html = f'<span class="field-hint">{esc(hint)}</span>' if hint else ""
    suffix_html = f'<span class="field-suffix">{esc(suffix)}</span>' if suffix else ""
    value_attr = f' value="{esc(value)}"' if value else ""
    return f"""<label class="field" for="calc-{name}">
  <span class="field-label">{esc(label)}</span>
  <span class="field-input">
    <input id="calc-{name}" name="{name}" type="{kind}"{value_attr} placeholder="0" inputmode="decimal" autocomplete="off">
    {suffix_html}
  </span>
  {hint_html}
</label>"""


def salary_calculator(rules: dict) -> str:
    d = rules["defaults"]
    fields_left = "".join([
        _field("ctc", "Annual CTC", "", suffix="₹", hint="Cost to company — everything the employer spends on you"),
        _field("basic", "Basic salary", "", suffix="% of CTC", hint="Usually 35–50% of CTC"),
        _field("hra", "HRA", "", suffix="% of basic"),
        _field("rent", "Monthly rent paid", "", suffix="₹", hint="Used for the HRA exemption under the old regime"),
    ])
    fields_right = "".join([
        _field("sec80c", "80C investments", "", suffix="₹", hint="PPF, ELSS, life insurance, tuition. Employee PF is added automatically. Cap ₹1.5 lakh"),
        _field("sec80d", "80D health premium", "", suffix="₹", hint="Self and family. Cap ₹25,000 here"),
        _field("home", "Home loan interest", "", suffix="₹", hint="Section 24(b). Cap ₹2 lakh"),
        _field("pt", "Professional tax", "", suffix="₹/yr", hint="State levy; ₹2,400 is common"),
    ])

    return f"""
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="../index.html">Home</a></li><li aria-current="page">Salary calculator</li>
    </ol></nav>
    <h1>Salary &amp; take-home calculator</h1>
    <p class="page-lede">
      Put in your CTC and see what actually reaches your bank account, under both the new and the old
      tax regime — and which one leaves you with more.
    </p>
    <p class="page-meta">Rules as of FY {esc(rules['financialYear'])} · verify at the Income Tax Department</p>
  </div>
</section>

<section class="section calc-section">
  <div class="shell calc-layout">

    <form class="calc-form" id="salary-form" novalidate>
      <fieldset class="calc-group">
        <legend>Your salary</legend>
        <div class="calc-grid">
          {fields_left}
          <label class="field field-check" for="calc-metro">
            <span class="field-label">Metro city</span>
            <span class="check-row">
              <input id="calc-metro" name="metro" type="checkbox" {"checked" if d["metro"] else ""}>
              <span>Delhi, Mumbai, Kolkata or Chennai</span>
            </span>
          </label>
        </div>
      </fieldset>

      <fieldset class="calc-group">
        <legend>Deductions you claim</legend>
        <p class="calc-group-note">These only reduce tax under the <strong>old</strong> regime, except professional tax.</p>
        <div class="calc-grid">
          {fields_right}
          <label class="field field-check" for="calc-pf-in-ctc">
            <span class="field-label">Employer PF</span>
            <span class="check-row">
              <input id="calc-pf-in-ctc" name="pfInCtc" type="checkbox" {"checked" if d["employerPfInCtc"] else ""}>
              <span>Employer's 12% PF is part of my CTC</span>
            </span>
          </label>
        </div>
      </fieldset>

      <div class="calc-actions">
        <button class="btn btn-primary" type="submit">Calculate</button>
        <button class="btn btn-ghost" type="reset" id="calc-reset">Reset</button>
      </div>
    </form>

    <aside class="calc-results" id="calc-results" aria-live="polite">
      <div class="calc-empty" id="calc-empty">
        <p>Enter your CTC to see the breakdown.</p>
      </div>
      <div id="calc-output" hidden></div>
    </aside>
  </div>
</section>

<section class="section section-tint">
  <div class="shell shell-narrow">
    <div class="calc-notes">
      <h2>The rates behind the numbers</h2>
      <p class="muted">New regime, FY {esc(rules['financialYear'])}. Old regime slabs are 2.5 / 5 / 10 lakh at 5% / 20% / 30%.</p>
      <table class="calc-slab-table">
        <thead><tr><th scope="col">Income slice</th><th scope="col">Rate</th></tr></thead>
        <tbody>
          <tr><td>Up to ₹4,00,000</td><td>Nil</td></tr>
          <tr><td>₹4,00,001 – ₹8,00,000</td><td>5%</td></tr>
          <tr><td>₹8,00,001 – ₹12,00,000</td><td>10%</td></tr>
          <tr><td>₹12,00,001 – ₹16,00,000</td><td>15%</td></tr>
          <tr><td>₹16,00,001 – ₹20,00,000</td><td>20%</td></tr>
          <tr><td>₹20,00,001 – ₹24,00,000</td><td>25%</td></tr>
          <tr><td>Above ₹24,00,000</td><td>30%</td></tr>
        </tbody>
      </table>
      <p class="muted">Standard deduction ₹75,000 · Section 87A rebate up to ₹60,000, which makes taxable income up to ₹12,00,000 tax-free · 4% cess · surcharge above ₹50 lakh.</p>

      <h2>What this does and doesn't do</h2>
      <ul class="check-list">
        <li>{icon("check", "icon icon-sm")}<span>Compares the two regimes on the same salary, so the difference is like for like.</span></li>
        <li>{icon("check", "icon icon-sm")}<span>Uses the slabs in force for FY {esc(rules['financialYear'])}, including the standard deduction, rebate, surcharge and 4% cess.</span></li>
        <li>{icon("alert", "icon icon-sm")}<span>It is an estimate, not a tax computation. It ignores marginal relief on surcharge, gratuity, LTA, employer NPS, leave encashment and any income outside salary.</span></li>
        <li>{icon("alert", "icon icon-sm")}<span>HRA uses the standard three-part test. Special cases — your own house, shared rent, non-metro city definitions — need a tax adviser.</span></li>
        <li>{icon("alert", "icon icon-sm")}<span>Slabs change with each Budget. The date above is the version encoded here.</span></li>
      </ul>
      <p class="muted">
        Source for the rules: <a href="{esc(rules['sourceUrl'])}" target="_blank" rel="noopener noreferrer">{esc(rules['sourceLabel'])} ↗</a>
      </p>
      <p class="muted"><a href="savings.html">Savings, SIP and deposit calculator →</a> · <a href="spending.html">Spending planner →</a></p>
    </div>
  </div>
</section>

<script type="application/json" id="tax-rules">{json.dumps(rules, ensure_ascii=False).replace("</", "<\\/")}</script>
<script src="../assets/js/salary.js" defer></script>
"""

def money_calculator() -> str:
    return """
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="../index.html">Home</a></li><li aria-current="page">Savings calculator</li>
    </ol></nav>
    <h1>What will it grow to?</h1>
    <p class="page-lede">
      Monthly investing, a one-time amount, or a deposit at a fixed rate. Every result is arithmetic on the
      numbers you type — not a prediction of what any fund will do.
    </p>
    <p class="page-meta">Illustrative only · no fund returns are forecast here</p>
  </div>
</section>

<section class="section">
  <div class="shell calc-layout">
    <form class="calc-form" id="money-form" novalidate>
      <div class="seg-toggle seg-wide" role="group" aria-label="What are you calculating">
        <button type="button" data-money-tab="sip" class="is-on">Monthly investing</button>
        <button type="button" data-money-tab="lump">One-time</button>
        <button type="button" data-money-tab="deposit">Deposit</button>
      </div>

      <fieldset class="calc-group">
        <legend>Your numbers</legend>
        <div class="calc-grid">
          <label class="field" data-only="sip">
            <span class="field-label">Monthly amount</span>
            <span class="field-input"><input id="m-monthly" type="number" placeholder="Monthly amount" min="0"><span class="field-suffix">₹</span></span>
          </label>
          <label class="field" data-only="sip">
            <span class="field-label">Annual step-up</span>
            <span class="field-input"><input id="m-stepup" type="number" placeholder="0" min="0" max="50"><span class="field-suffix">% a year</span></span>
          </label>

          <label class="field" data-only="lump">
            <span class="field-label">One-time amount</span>
            <span class="field-input"><input id="m-amount" type="number" placeholder="One-time amount" min="0"><span class="field-suffix">₹</span></span>
          </label>

          <label class="field" data-only="deposit">
            <span class="field-label">Deposit amount</span>
            <span class="field-input"><input id="m-principal" type="number" placeholder="Deposit amount" min="0"><span class="field-suffix">₹</span></span>
          </label>
          <label class="field" data-only="deposit">
            <span class="field-label">Or monthly addition</span>
            <span class="field-input"><input id="m-addmonthly" type="number" placeholder="0" min="0"><span class="field-suffix">₹</span></span>
          </label>
          <label class="field" data-only="deposit">
            <span class="field-label">Compounding</span>
            <span class="field-input">
              <select id="m-compounding">
                <option value="quarterly">Quarterly (most FDs)</option>
                <option value="monthly">Monthly</option>
                <option value="half-yearly">Half-yearly</option>
                <option value="annual">Annual (PPF, NSC)</option>
                <option value="simple">Simple interest</option>
              </select>
            </span>
          </label>

          <label class="field" data-only="shared">
            <span class="field-label">For how long</span>
            <span class="field-input"><input id="m-years" type="number" placeholder="Years" min="1" max="40"><span class="field-suffix">years</span></span>
          </label>
          <label class="field" data-only="shared">
            <span class="field-label">Expected return / rate</span>
            <span class="field-input"><input id="m-rate" type="number" placeholder="%" min="0" max="30" step="0.1"><span class="field-suffix">% a year</span></span>
          </label>
          <label class="field" data-only="shared">
            <span class="field-label">Inflation</span>
            <span class="field-input"><input id="m-inflation" type="number" placeholder="% inflation" min="0" max="20" step="0.1"><span class="field-suffix">% a year</span></span>
          </label>
        </div>
      </fieldset>
    </form>

    <aside class="calc-results">
      <div id="money-output"></div>
    </aside>
  </div>
</section>

<section class="section section-tint">
  <div class="shell shell-narrow">
    <div class="calc-notes">
      <h2>Read this before trusting the number</h2>
      <ul class="check-list">
        <li>""" + icon("check", "icon icon-sm") + """<span>The arithmetic is exact: compounded at the rate you typed, for the term you typed.</span></li>
        <li>""" + icon("alert", "icon icon-sm") + """<span>No fund earns the same rate every year. A 12% average can include a 30% fall.</span></li>
        <li>""" + icon("alert", "icon icon-sm") + """<span>Tax, exit loads and expense ratios are not deducted. A 6% deposit and a 12% fund are not comparable until they are.</span></li>
        <li>""" + icon("alert", "icon icon-sm") + """<span>Deposit rates change. Check the bank's rate card for the tenure you actually want.</span></li>
      </ul>
      <p class="muted"><a href="salary.html">Salary and take-home calculator →</a></p>
    </div>
  </div>
</section>
"""
