"""Sukanya Samriddhi Yojana — full guide with an inline calculator."""

from __future__ import annotations

import json

from .site import esc, icon


def page(rules: dict, rates: dict) -> str:
    rate = (rates.get("ssy") or {}).get("value", "—")
    as_of = (rates.get("ssy") or {}).get("asOf", "—")
    data = json.dumps({"rate": rate, "asOf": as_of}, ensure_ascii=False)

    return f"""
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="../index.html">Home</a></li><li><a href="../start.html">Start here</a></li>
      <li aria-current="page">Sukanya Samriddhi Yojana</li>
    </ol></nav>
    <h1>Sukanya Samriddhi Yojana</h1>
    <p class="page-lede">
      A government savings account for a girl child, paying the highest small-savings rate and entirely
      tax-free. Here is exactly how it works, what the rules allow, and what it becomes over 21 years.
    </p>
    <p class="page-meta">Rate {esc(rate)} · notified for the quarter beginning {esc(as_of)}</p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="ssy-facts">
      <div class="ssy-fact"><span>Rate</span><strong>{esc(rate)}</strong><em>per year, compounded annually</em></div>
      <div class="ssy-fact"><span>Who</span><strong>Girl under 10</strong><em>opened by a parent or guardian</em></div>
      <div class="ssy-fact"><span>Deposit years</span><strong>15</strong><em>then it keeps earning</em></div>
      <div class="ssy-fact"><span>Matures</span><strong>21 years</strong><em>from opening</em></div>
      <div class="ssy-fact"><span>Yearly limit</span><strong>₹250 – ₹1.5 L</strong><em>minimum ₹250</em></div>
      <div class="ssy-fact"><span>Tax</span><strong>Exempt</strong><em>deposit, interest and maturity</em></div>
    </div>
  </div>
</section>

<section class="section section-tint" id="calculator">
  <div class="shell calc-layout">
    <form class="calc-form" id="ssy-form">
      <fieldset class="calc-group">
        <legend>Work out the maturity value</legend>
        <div class="calc-grid">
          <label class="field">
            <span class="field-label">Amount deposited each year</span>
            <span class="field-input"><input id="ssy-amount" type="number" min="250" step="500" placeholder="e.g. 150000"><span class="field-suffix">₹</span></span>
          </label>
          <label class="field">
            <span class="field-label">Years you deposit</span>
            <span class="field-input"><input id="ssy-years" type="number" min="1" max="15" value="15"><span class="field-suffix">years</span></span>
          </label>
          <label class="field" data-only="shared">
            <span class="field-label">Rate</span>
            <span class="field-input"><input id="ssy-rate" type="number" min="1" max="15" step="0.05" value="{esc(rate.replace('%', ''))}"><span class="field-suffix">% a year</span></span>
          </label>
        </div>
        <p class="field-hint">The rate is notified each quarter. Change it to see how a revision would affect the result.</p>
      </fieldset>

      <div class="calc-actions">
        <button class="btn btn-primary" type="submit">Calculate</button>
        <button class="btn btn-ghost" type="reset" id="ssy-reset">Reset</button>
      </div>
    </form>

    <aside class="calc-results">
      <div id="ssy-output"><p class="calc-empty-text">Enter an amount to see the projection.</p></div>
    </aside>
  </div>
</section>

<section class="section">
  <div class="shell shell-narrow">
    <h2 class="guide-h2">Who can open one</h2>
    <p class="guide-p">
      A parent or legal guardian opens the account for a girl child who is a resident Indian and under ten
      years old. One account per girl. A family can hold a maximum of two accounts — three if the second
      birth produced twins or triplets, so that the later daughters are not excluded.
    </p>
    <p class="guide-p">
      The account is opened at a post office or an authorised bank with the child's birth certificate and the
      guardian's KYC. It is operated by the guardian until the girl turns 18.
    </p>

    <h2 class="guide-h2">How the money works</h2>
    <p class="guide-p">
      You deposit between ₹250 and ₹1.5 lakh in a financial year, for fifteen years. After that you stop
      depositing, but the balance keeps earning interest until the account matures at twenty-one years from
      opening. Interest is compounded annually and credited at the end of each year.
    </p>
    <p class="guide-p">
      The rate is not fixed for the life of the account. It is notified every quarter, and the balance earns
      whatever rate is in force — the same rule as PPF. At {esc(rate)} today, the projection below is what the
      account produces if that rate held for the whole term.
    </p>

    <h2 class="guide-h2">How it is taxed</h2>
    <ul class="check-list">
      <li>{icon("check", "icon icon-sm")}<span><strong>Deposits</strong> qualify under Section 80C, up to ₹1.5 lakh — old regime only.</span></li>
      <li>{icon("check", "icon icon-sm")}<span><strong>Interest</strong> is not taxed as it accrues.</span></li>
      <li>{icon("check", "icon icon-sm")}<span><strong>Maturity proceeds</strong> are not taxed.</span></li>
    </ul>
    <p class="guide-p">
      That combination is why the effective return beats a fixed deposit at a similar headline rate. An FD at
      8.2% in the 30% slab nets roughly 5.7% after tax. SSY keeps the full 8.2%.
    </p>

    <h2 class="guide-h2">When you can take money out</h2>
    <ul class="check-list">
      <li>{icon("alert", "icon icon-sm")}<span><strong>For education</strong> — up to 50% of the balance at the end of the previous financial year, once she turns 18 or passes Class 10, whichever is earlier. A document showing admission or a fee notice is required.</span></li>
      <li>{icon("alert", "icon icon-sm")}<span><strong>For marriage</strong> — the account can be closed after she turns 18, subject to the rules in force. Check at the counter before relying on it.</span></li>
      <li>{icon("alert", "icon icon-sm")}<span><strong>Full closure before maturity</strong> is not normally allowed. Only the two cases above, or on the death of the account holder.</span></li>
      <li>{icon("alert", "icon icon-sm")}<span><strong>Missed a year?</strong> A ₹50 penalty per defaulted year applies, and the account can be revived by paying the minimum plus the penalty.</span></li>
    </ul>

    <h2 class="guide-h2">SSY or PPF?</h2>
    <p class="guide-p">
      SSY pays more — {esc(rate)} against 7.10% — and has the same tax treatment. If you have a daughter under
      ten, it is the better home for that money. PPF is the option when you do not, or when you need the
      flexibility of partial withdrawal from year six.
    </p>
    <p class="guide-cta">
      <a class="btn btn-primary" href="../guides/ssy-vs-ppf.html">Compare SSY and PPF</a>
      <a class="btn btn-ghost" href="../products/sukanya-samriddhi-yojana.html">Product record</a>
    </p>

    <p class="guide-src">
      Rate {esc(rate)}, notified for the quarter beginning {esc(as_of)} —
      <a href="https://www.nsiindia.gov.in" target="_blank" rel="noopener noreferrer">National Savings Institute</a>.
      Scheme rules published by India Post and the Ministry of Finance. Rules change: confirm at your post
      office or bank before acting.
    </p>
  </div>
</section>

<script type="application/json" id="ssy-rules">{data}</script>
<script src="../assets/js/ssy.js" defer></script>
"""
