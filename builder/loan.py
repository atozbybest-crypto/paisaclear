"""Loan EMI calculator page."""

from __future__ import annotations

from .site import icon


def loan_page() -> str:
    return """
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="../index.html">Home</a></li><li aria-current="page">Loan EMI</li>
    </ol></nav>
    <h1>Loan EMI and repayment</h1>
    <p class="page-lede">
      Enter the amount, the rate and the term to see the monthly payment, what the loan costs in total, and
      how much of each year goes to interest rather than principal.
    </p>
    <p class="page-meta">Arithmetic on your inputs · not a lender quote</p>
  </div>
</section>

<section class="section">
  <div class="shell calc-layout">
    <form class="calc-form" id="loan-form" novalidate>
      <fieldset class="calc-group">
        <legend>Your loan</legend>
        <div class="calc-grid">
          <label class="field">
            <span class="field-label">Loan amount</span>
            <span class="field-input"><input id="l-amount" type="number" min="1000" step="1000" value="2000000"><span class="field-suffix">₹</span></span>
          </label>
          <label class="field">
            <span class="field-label">Interest rate</span>
            <span class="field-input"><input id="l-rate" type="number" min="0" max="40" step="0.05" value="8.5"><span class="field-suffix">% a year</span></span>
          </label>
          <label class="field">
            <span class="field-label">Term</span>
            <span class="field-input"><input id="l-years" type="number" min="1" max="40" value="20"><span class="field-suffix">years</span></span>
          </label>
          <label class="field">
            <span class="field-label">Extra payment each month</span>
            <span class="field-input"><input id="l-extra" type="number" min="0" step="500" value="0"><span class="field-suffix">₹ optional</span></span>
          </label>
        </div>
      </fieldset>

      <div class="calc-note-block">
        <p>
          The EMI is fixed by the amount, rate and term. An extra payment does not change the EMI — it shortens
          the loan and cuts the interest, which is what the second column below shows.
        </p>
      </div>
    </form>

    <aside class="calc-results">
      <div id="loan-output"></div>
    </aside>
  </div>
</section>

<section class="section section-tint">
  <div class="shell shell-narrow">
    <div class="calc-notes">
      <h2>What this does not include</h2>
      <ul class="check-list">
        <li>""" + icon("alert", "icon icon-sm") + """<span>Processing fees, insurance, stamp duty and any pre-payment penalty.</span></li>
        <li>""" + icon("alert", "icon icon-sm") + """<span>Floating rates. Most home loans reset with the repo rate, so the EMI or the term changes part-way.</span></li>
        <li>""" + icon("alert", "icon icon-sm") + """<span>Tax deductions on interest or principal — those depend on the loan type and your regime.</span></li>
        <li>""" + icon("check", "icon icon-sm") + """<span>The schedule assumes payments are made on time, every month, with no missed instalments.</span></li>
      </ul>
      <p class="muted"><a href="planning.html">Emergency & retirement planners →</a> · <a href="savings.html">Savings calculator →</a></p>
    </div>
  </div>
</section>
"""
