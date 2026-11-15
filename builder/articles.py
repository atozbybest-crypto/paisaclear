"""Long-form articles — the pages that only this site could publish."""

from __future__ import annotations

from .site import esc


def _shell(title: str, lede: str, meta: str, body: str, base: str = "") -> str:
    return f"""
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="{base}index.html">Home</a></li>
      <li><a href="{base}articles.html">Articles</a></li>
      <li aria-current="page">{esc(title)}</li>
    </ol></nav>
    <h1>{esc(title)}</h1>
    <p class="page-lede">{lede}</p>
    <p class="page-meta">{esc(meta)}</p>
  </div>
</section>

<section class="section">
  <div class="shell shell-narrow">
    {body}
    <p class="guide-src">
      Written for PaisaClear. Every figure here carries the date it applied and links to its source. If
      something is wrong, <a href="{base}feedback.html">tell us</a> — corrections come first.
    </p>
  </div>
</section>
"""


HEALTH = _shell(
    "How to read a health insurance policy: the five clauses that decide your claim",
    "The premium is what you pay. These five clauses decide what you get back — and none of them are on the brochure.",
    "Reviewed 15 November 2026",
    """
    <p class="guide-p">
      Two health policies can quote the same sum insured, the same premium and the same hospital network, and
      behave completely differently when you claim. The difference lives in five clauses buried in the policy
      wording. Read them before you pay, in this order.
    </p>

    <h2 class="guide-h2">1. The waiting period — and what counts as pre-existing</h2>
    <p class="guide-p">
      Most policies exclude treatment for pre-existing conditions for two to four years. The question that
      matters is not the number of years but what the insurer counts as pre-existing: a condition diagnosed
      before the policy started, or one whose symptoms existed even if it was never diagnosed.
    </p>
    <p class="guide-p">
      A policy that defines pre-existing as "diagnosed or treated" is safer than one that says "diagnosed,
      treated, or for which medical advice was sought". The second version lets an insurer argue that a cough
      you mentioned to a doctor in 2021 was an undeclared condition.
    </p>
    <p class="guide-p">
      Also look for the specific waiting periods on named procedures. Cataract, hernia, joint replacement and
      maternity usually have their own clocks — often longer than the general pre-existing period.
    </p>

    <h2 class="guide-h2">2. Room rent limits — the clause that costs the most</h2>
    <p class="guide-p">
      A policy capping room rent at 1% of sum insured per day does more damage than people expect. When your
      room exceeds the cap, most insurers apply a <em>proportionate deduction</em> to the entire bill, not just
      the room charge.
    </p>
    <p class="guide-p">
      On a ₹5 lakh cover, a 1% cap is ₹5,000 a day. Admit yourself to a ₹8,000 room and the insurer may reduce
      the whole claim by the same ratio — paying 62% of the surgeon's fee, the ICU charge, everything. The
      clause with the smallest print has the largest effect on what you receive.
    </p>
    <p class="guide-p">
      Single private room without a cap is worth paying for. If the choice is ₹4 lakh with no room cap or ₹6
      lakh with a 1% cap, the smaller policy with no cap often settles more.
    </p>

    <h2 class="guide-h2">3. Sub-limits on specific treatments</h2>
    <p class="guide-p">
      A ₹10 lakh policy does not mean ₹10 lakh for everything. Cataract surgery may be capped at ₹40,000 per
      eye; maternity at ₹50,000; cardiac procedures at a percentage of sum insured. These are separate
      ceilings inside the main one.
    </p>
    <p class="guide-p">
      Ask for the sub-limit table in writing. If an insurer will not give it before you buy, that is your
      answer.
    </p>

    <h2 class="guide-h2">4. Co-payment and deductible</h2>
    <p class="guide-p">
      A co-payment is the share of every claim you pay — 10% or 20% is common in senior-citizen policies. A
      deductible is a fixed amount you pay before cover starts, for example the first ₹25,000 each year.
    </p>
    <p class="guide-p">
      Neither is unreasonable on its own, and both reduce the premium. But they compound: a 20% co-payment plus
      a ₹25,000 deductible on a ₹2 lakh bill leaves you paying ₹65,000. Work that arithmetic with your own
      likely bill before choosing the cheaper premium.
    </p>

    <h2 class="guide-h2">5. Restoration and recharge</h2>
    <p class="guide-p">
      Restoration puts the sum insured back after you have used it, usually once a year and usually only for a
      different illness. Some policies restore automatically and without limit; others restore only once, and
      only if the second claim is unrelated to the first.
    </p>
    <p class="guide-p">
      For a family floater, this clause matters more than the headline sum insured. One hospitalisation can
      exhaust a ₹5 lakh cover; whether it comes back decides if the policy is useful for the rest of the year.
    </p>

    <h2 class="guide-h2">What to do with this</h2>
    <p class="guide-p">
      Ask for the policy wording — not the brochure — before you buy, and search it for four words: waiting,
      room, sub-limit, co-pay. Those four sections take twenty minutes to read and decide whether the policy
      pays when you need it.
    </p>
    <p class="guide-p">
      The <a href="categories/health-insurance.html">health insurance records</a> on this site list what each
      insurer says about its own plan, with the date it was checked. They are a starting point for that
      reading, not a substitute for it.
    </p>
    """,
)

TAX = _shell(
    "PPF vs FD vs NSC: the tax arithmetic, done properly",
    "Three products, one headline rate each. After tax they are not the same product at all.",
    "Reviewed 15 November 2026",
    """
    <p class="guide-p">
      Almost every comparison of PPF, fixed deposits and National Savings Certificates uses the headline rate.
      That number is misleading for two of the three, because they are taxed differently. Here is the arithmetic,
      with the assumptions stated.
    </p>

    <h2 class="guide-h2">The numbers used here</h2>
    <ul class="check-list">
      <li><span><strong>PPF:</strong> 7.10%, notified for the quarter beginning 1 October 2026 — exempt, exempt, exempt.</span></li>
      <li><span><strong>Bank FD:</strong> 7.10% assumed, for comparison. Interest taxed at your slab.</span></li>
      <li><span><strong>NSC:</strong> 7.70%, notified for the same quarter. Interest taxed at your slab.</span></li>
    </ul>

    <h2 class="guide-h2">The only number that matters: after-tax yield</h2>
    <p class="guide-p">
      After-tax yield = headline rate × (1 − your slab). At the 30% slab, with 4% cess on the tax:
    </p>
    <p class="guide-p">
      PPF 7.10% × 1.00 = <strong>7.10%</strong><br>
      FD 7.10% × (1 − 0.312) = <strong>4.88%</strong><br>
      NSC 7.70% × (1 − 0.312) = <strong>5.30%</strong>
    </p>
    <p class="guide-p">
      A fixed deposit needs a headline rate of about <strong>10.3%</strong> to match a tax-free 7.10%. That
      number does not exist in the Indian deposit market. This is the entire argument for PPF, and it has
      nothing to do with which product is "better" in the abstract.
    </p>

    <h2 class="guide-h2">At the 5% and 20% slabs</h2>
    <p class="guide-p">
      The gap narrows as your slab falls, but it does not close:
    </p>
    <ul class="check-list">
      <li><span><strong>5% slab:</strong> FD at 7.10% keeps 6.74%; NSC at 7.70% keeps 7.31%. PPF still wins against the FD.</span></li>
      <li><span><strong>20% slab:</strong> FD at 7.10% keeps 5.63%; NSC at 7.70% keeps 6.11%. PPF wins clearly.</span></li>
    </ul>
    <p class="guide-p">
      One exception is worth knowing: if your total income is below the taxable threshold, no tax is due on FD
      interest at all. In that case a higher-rate taxable product genuinely pays more.
    </p>

    <h2 class="guide-h2">What the comparison leaves out</h2>
    <p class="guide-p">
      <strong>Liquidity.</strong> PPF locks the money for fifteen years, with a loan from year three and
      partial withdrawal from year six. An FD breaks in a day with a small penalty. If you may need the money,
      PPF's higher after-tax return is irrelevant.
    </p>
    <p class="guide-p">
      <strong>Rate revision.</strong> Neither rate is fixed for the life of the product. PPF's rate is notified
      quarterly and applies to the balance; an FD's rate is fixed when you book it. In a falling-rate
      environment the FD protects your rate; in a rising one, PPF follows it up.
    </p>
    <p class="guide-p">
      <strong>The 80C illusion.</strong> All three qualify for 80C, so the deduction is identical and cancels
      out of the comparison. It is a reason to hold one of them, not a reason to choose between them.
    </p>

    <h2 class="guide-h2">A worked example</h2>
    <p class="guide-p">
      ₹1,50,000 a year for fifteen years, at the rates above and the 30% slab:
    </p>
    <p class="guide-p">
      PPF at 7.10% tax-free: about <strong>₹40.7 lakh</strong> at maturity, tax already settled.<br>
      FD at 7.10% compounded and taxed annually: about <strong>₹33.1 lakh</strong> in hand after tax.<br>
      NSC at 7.70%, five-year certificates rolled over, taxed annually: about <strong>₹35.4 lakh</strong>.
    </p>
    <p class="guide-p">
      The differences are not rounding. They come from one clause in the tax code, not from the interest rate.
    </p>

    <h2 class="guide-h2">So which one</h2>
    <p class="guide-p">
      If you are in the 20% or 30% slab and will not need the money for a decade, PPF. If you need access, an FD
      — and accept the lower after-tax return as the price of liquidity. If you want a fixed rate rather than a
      floating one, NSC does that, at the cost of tax on the interest.
    </p>
    <p class="guide-p">
      Use the <a href="calculators/savings.html">savings calculator</a> to run your own numbers, and check the
      current rates on the <a href="rates.html">rates page</a> — each figure there carries the date it applied.
    </p>
    """,
)


def about_editorial(base: str = "") -> tuple[str, str, str]:
    """Content for the articles index."""
    return HEALTH, TAX, ""


ARTICLES = [
    ("health-insurance-policy-clauses.html",
     "How to read a health insurance policy",
     "The five clauses that decide your claim — waiting periods, room rent, sub-limits, co-pay, restoration.",
     "15 November 2026"),
    ("ppf-vs-fd-vs-nsc-tax.html",
     "PPF vs FD vs NSC: the tax arithmetic",
     "Same headline rate, different money. The after-tax maths, with a worked fifteen-year example.",
     "15 November 2026"),
]


def index() -> str:
    from .site import esc as _esc
    cards = "".join(
        f'<a class="plan-card" href="{slug}">'
        f'<span class="plan-tag">Article · {when}</span>'
        f'<span class="plan-name">{_esc(name)}</span>'
        f'<span class="plan-line">{_esc(line)}</span>'
        f'<span class="plan-cta">Read →</span></a>'
        for slug, name, line, when in ARTICLES
    )
    return f"""
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="index.html">Home</a></li><li aria-current="page">Articles</li>
    </ol></nav>
    <h1>Articles</h1>
    <p class="page-lede">
      Longer pieces that would not fit on a product page — the tax arithmetic, the policy clauses, the parts
      of a product that decide whether it works for you.
    </p>
    <p class="page-meta">{len(ARTICLES)} articles · new ones added as the site grows</p>
  </div>
</section>

<section class="section">
  <div class="shell"><div class="plan-grid">{cards}</div></div>
</section>
"""
