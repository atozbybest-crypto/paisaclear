"""The salary calculator page."""

from __future__ import annotations

import json

from .site import esc, icon, page


def _field(name: str, label: str, value: str, *, suffix: str = "", hint: str = "", kind: str = "number") -> str:
    hint_html = f'<span class="field-hint">{esc(hint)}</span>' if hint else ""
    suffix_html = f'<span class="field-suffix">{esc(suffix)}</span>' if suffix else ""
    return f"""<label class="field" for="calc-{name}">
  <span class="field-label">{esc(label)}</span>
  <span class="field-input">
    <input id="calc-{name}" name="{name}" type="{kind}" value="{esc(value)}" inputmode="decimal" autocomplete="off">
    {suffix_html}
  </span>
  {hint_html}
</label>"""


def salary_calculator(rules: dict) -> str:
    d = rules["defaults"]
    fields_left = "".join([
        _field("ctc", "Annual CTC", f"{d['ctc']}", suffix="₹", hint="Cost to company — everything the employer spends on you"),
        _field("basic", "Basic salary", f"{d['basicPct']}", suffix="% of CTC", hint="Usually 35–50% of CTC"),
        _field("hra", "HRA", f"{d['hraPct']}", suffix="% of basic"),
        _field("rent", "Monthly rent paid", f"{d['rent']}", suffix="₹", hint="Used for the HRA exemption under the old regime"),
    ])
    fields_right = "".join([
        _field("sec80c", "80C investments", f"{d['sec80c']}", suffix="₹", hint="PPF, ELSS, life insurance, tuition. Employee PF is added automatically. Cap ₹1.5 lakh"),
        _field("sec80d", "80D health premium", f"{d['sec80d']}", suffix="₹", hint="Self and family. Cap ₹25,000 here"),
        _field("home", "Home loan interest", f"{d['homeLoanInterest']}", suffix="₹", hint="Section 24(b). Cap ₹2 lakh"),
        _field("pt", "Professional tax", f"{d['professionalTax']}", suffix="₹/yr", hint="State levy; ₹2,400 is common"),
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
    </div>
  </div>
</section>

<script type="application/json" id="tax-rules">{json.dumps(rules, ensure_ascii=False).replace("</", "<\\/")}</script>
<script src="../assets/js/salary.js" defer></script>
"""
