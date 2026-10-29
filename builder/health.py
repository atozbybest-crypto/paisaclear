"""Private health insurance pages.

The features on each page are the insurer's own description of the plan. We
have not verified waiting periods, sub-limits or network counts, and the page
says so — that is the difference between a directory and an endorsement.
"""

from __future__ import annotations

from .site import breadcrumb, esc, icon


def page(ctx: dict, product: dict) -> str:
    category = ctx["categories_by_id"][product["category"]]
    highlights = product.get("highlights", [])
    checks = product.get("check", [])

    feature_rows = "".join(
        f'<li>{icon("check", "icon icon-sm")}<span>{esc(item)}</span></li>' for item in highlights
    )
    check_rows = "".join(
        f'<li>{icon("alert", "icon icon-sm")}<span>{esc(item)}</span></li>' for item in checks
    )

    facts = [
        ("Insurer", esc(product["provider"])),
        ("Plan", esc(product.get("plan", ""))),
        ("Type", "Health indemnity / family floater"),
        ("Premium", "Set by the insurer, by age, city and cover"),
        ("Term", "One year, renewable"),
    ]
    fact_rows = "".join(f'<div class="fact-row"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in facts)

    return f"""
<section class="page-head">
  <div class="shell">
    {breadcrumb([("Home", "../index.html"), ("All products", "../browse.html"),
                 (category["name"], f"../categories/{category['slug']}.html"), (product["name"], "")])}
    <div class="prod-badges">
      <span class="chip chip-conditional">Conditional</span>
      <span class="chip chip-risk-low">Protection</span>
      <span class="pcard-cat">{esc(category["short"])}</span>
    </div>
    <h1>{esc(product["name"])}</h1>
    <p class="page-lede">{esc(product.get("oneLiner", ""))}</p>
    <p class="page-meta">Plan features as described by the insurer · last checked {esc(product["lastVerified"])}</p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="split">
      <div class="split-main">
        <h2 class="subhead">What the insurer highlights</h2>
        <ul class="check-list">{feature_rows}</ul>

        <h2 class="guide-h2">What to check before you buy</h2>
        <ul class="check-list">{check_rows}</ul>

        <h2 class="guide-h2">Why the details matter more than the headline</h2>
        <p class="guide-p">
          Health policies are sold on the sum insured and the premium, but the claim is decided by the small
          print: waiting periods for pre-existing conditions, room-rent limits, co-payment, sub-limits on
          specific treatments, and whether the hospital you would use is in the network.
        </p>
        <p class="guide-p">
          Two policies with identical cover can behave very differently at claim time. Read the policy wording
          — not the brochure — and check the exclusions list before paying.
        </p>

        <h2 class="guide-h2">Where to verify</h2>
        <ul class="source-links">
          <li><a href="{esc(product['source']['url'])}" target="_blank" rel="noopener noreferrer">
            {esc(product['provider'])} — health insurance <span class="ext" aria-hidden="true">↗</span></a></li>
          <li><a href="https://www.irdai.gov.in" target="_blank" rel="noopener noreferrer">
            IRDAI — insurer and product registration <span class="ext" aria-hidden="true">↗</span></a></li>
        </ul>
        <p class="guide-src">
          Confirm the UIN, sum insured, waiting periods and network on the insurer's own page. PaisaClear has
          not independently verified these features, and a listing here is not a recommendation.
        </p>
      </div>

      <aside class="split-aside">
        <div class="aside-card">
          <h2>Key facts</h2>
          <dl class="fact-list">{fact_rows}</dl>
        </div>
        <div class="aside-card">
          <h2>Not the right place to start?</h2>
          <p class="aside-note">
            If you are choosing cover for the first time, the <a href="../answers.html">answers page</a> explains
            waiting periods and what a family floater is before you compare premiums.
          </p>
        </div>
      </aside>
    </div>
  </div>
</section>

<section class="section section-tint">
  <div class="shell shell-narrow">
    <div class="calc-notes">
      <h2>What this page is not</h2>
      <ul class="check-list">
        <li>{icon("alert", "icon icon-sm")}<span>Not a recommendation, and not a comparison of premiums — those depend on your age, city and cover.</span></li>
        <li>{icon("alert", "icon icon-sm")}<span>The features are the insurer's own claims, reproduced. We have not tested a claim with them.</span></li>
        <li>{icon("check", "icon icon-sm")}<span>Every insurer's policy wording, not this page, is what applies when you claim.</span></li>
      </ul>
      <p class="muted"><a href="../categories/health-insurance.html">All private health insurers →</a></p>
    </div>
  </div>
</section>
"""
