"""Beti Bachao Beti Padhao — a campaign, not a savings scheme.

Written honestly: it pays no interest and has no deposit, so it gets a guide
and no calculator. The savings counterpart is SSY, which is linked.
"""

from __future__ import annotations

from .site import icon


def page(rate: str, as_of: str) -> str:
    return f"""
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="../index.html">Home</a></li><li><a href="../plans.html">Plans</a></li>
      <li aria-current="page">Beti Bachao Beti Padhao</li>
    </ol></nav>
    <h1>Beti Bachao Beti Padhao</h1>
    <p class="page-lede">
      A national campaign for the survival, protection and education of the girl child. It is not a savings
      scheme — it pays no interest and accepts no deposit — so there is no calculator on this page. Here is
      what it actually does, and which scheme to use if you want to save for a daughter.
    </p>
    <p class="page-meta">Government of India campaign · launched 22 January 2015</p>
  </div>
</section>

<section class="section">
  <div class="shell shell-narrow">
    <div class="notice-strip">
      <strong>Not a money product.</strong>
      BBBP has no deposit, no interest rate and no maturity value. Any page that offers a "BBBP calculator"
      is showing you an illustration of something else.
    </div>

    <h2 class="guide-h2">What it is</h2>
    <p class="guide-p">
      A tri-ministerial effort launched at Panipat, Haryana, on 22 January 2015. The Ministry of Women and
      Child Development is the nodal ministry, working with the Ministry of Health and Family Welfare and the
      Ministry of Education. It is an implementation campaign — awareness, enforcement and delivery of
      existing services — not a financial instrument.
    </p>

    <h2 class="guide-h2">What it sets out to do</h2>
    <ul class="check-list">
      <li>{icon("check", "icon icon-sm")}<span>Prevent gender-biased sex selection, and improve the child sex ratio at birth.</span></li>
      <li>{icon("check", "icon icon-sm")}<span>Ensure the survival and protection of the girl child in the early years.</span></li>
      <li>{icon("check", "icon icon-sm")}<span>Ensure her education and participation — enrolment, retention and completion of schooling.</span></li>
      <li>{icon("check", "icon icon-sm")}<span>Change community attitudes through local campaigns, health workers and schools.</span></li>
    </ul>

    <h2 class="guide-h2">What it does not do</h2>
    <ul class="check-list">
      <li>{icon("alert", "icon icon-sm")}<span>It does not pay you any money. There is no cash transfer under the campaign itself.</span></li>
      <li>{icon("alert", "icon icon-sm")}<span>It does not open an account or give you a rate of return.</span></li>
      <li>{icon("alert", "icon icon-sm")}<span>It does not have a per-family benefit you apply for at a counter.</span></li>
      <li>{icon("alert", "icon icon-sm")}<span>Some states run their own girl-child cash schemes and use the BBBP name locally. Those are state schemes — check at your district office.</span></li>
    </ul>

    <h2 class="guide-h2">If you want to save for a daughter</h2>
    <p class="guide-p">
      The financial product built for that purpose is <strong>Sukanya Samriddhi Yojana</strong> — an account
      for a girl under ten, paying {rate} a year (notified for the quarter beginning {as_of}), with deposits,
      interest and maturity all tax-free. It is the scheme that BBBP enrolment drives most often point
      families towards.
    </p>
    <p class="guide-cta">
      <a class="btn btn-primary" href="sukanya-samriddhi.html">Sukanya Samriddhi guide and calculator</a>
      <a class="btn btn-ghost" href="../products/sukanya-samriddhi-yojana.html">Product record</a>
    </p>

    <h2 class="guide-h2">Where to verify</h2>
    <p class="guide-p">
      Campaign details, district-level implementation and state schemes are published by the Ministry of
      Women and Child Development. Rules and local benefits change, so confirm anything you plan to act on.
    </p>
    <ul class="source-links">
      <li><a href="https://wcd.nic.in" target="_blank" rel="noopener noreferrer">Ministry of Women and Child Development <span class="ext" aria-hidden="true">↗</span></a></li>
      <li><a href="https://www.india.gov.in" target="_blank" rel="noopener noreferrer">National Portal of India <span class="ext" aria-hidden="true">↗</span></a></li>
      <li><a href="https://www.nsiindia.gov.in" target="_blank" rel="noopener noreferrer">National Savings Institute — SSY rates <span class="ext" aria-hidden="true">↗</span></a></li>
    </ul>
  </div>
</section>
"""
