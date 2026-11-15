"""Final expansion pass — takes every article to roughly 2,000 words."""

POLICY = """
    <h2 class="guide-h2">A worked claim, start to finish</h2>
    <p class="guide-p">
      A 41-year-old with a ₹8 lakh family floater, bought four years ago, admitted for gallbladder surgery.
      Bill: ₹2.6 lakh, five nights, single private room at ₹9,000 a night. The policy has no room cap, a
      ₹50,000 sub-limit on laparoscopic surgery, and 60 days of post-hospitalisation cover.
    </p>
    <p class="guide-p">
      The insurer pays the room in full. It pays the surgery within the sub-limit, so ₹50,000 of the ₹1.1 lakh
      surgical charge is covered and ₹60,000 falls to the insured. Consumables of ₹18,000 are excluded. The
      final settlement is about ₹1.8 lakh, and the family pays ₹80,000.
    </p>
    <p class="guide-p">
      Nothing here was a surprise to a reader of the wording. The sub-limit and the consumables exclusion were
      both in the schedule, in plain text. This is the ordinary shape of a "covered" claim: the insurer pays
      most of it, and the insured pays a share that was knowable in advance.
    </p>

    <h2 class="guide-h2">Five myths worth killing</h2>
    <ul class="check-list">
      <li><span><strong>"Pre-existing means diagnosed."</strong> Most wordings include symptoms and advice sought, not just diagnosis.</span></li>
      <li><span><strong>"A higher sum insured means more cover for each thing."</strong> Sub-limits and caps are per treatment, not per policy size.</span></li>
      <li><span><strong>"Cashless means free."</strong> Cashless means the insurer settles with the hospital; exclusions and co-pay are still yours.</span></li>
      <li><span><strong>"The agent knows the policy."</strong> The agent knows the brochure. The wording is the contract.</span></li>
      <li><span><strong>"Claim rejection means the insurer cheated."</strong> Most rejections trace to non-disclosure or a waiting period that was printed and unread.</span></li>
    </ul>

    <h2 class="guide-h2">A checklist you can carry to the counter</h2>
    <p class="guide-p">
      Ask for, in writing, before paying: the policy wording PDF, the schedule of sub-limits, the list of
      waiting periods by condition, the co-payment clause, the network hospital list for your city, and the
      claim settlement ratio for the last three years. Six documents, all of which the insurer already has.
    </p>
"""

TAX2 = """
    <h2 class="guide-h2">The five-year comparison, in rupees</h2>
    <p class="guide-p">
      ₹1,50,000 a year for five years, 30% slab, at the notified rates:
    </p>
    <p class="guide-p">
      PPF at 7.10%: about <strong>₹8.96 lakh</strong> at the end of five years, tax settled.<br>
      FD at 7.10%, interest taxed annually: about <strong>₹8.46 lakh</strong> after tax.<br>
      NSC at 7.70%, interest taxed annually: about <strong>₹8.58 lakh</strong> after tax.
    </p>
    <p class="guide-p">
      Over five years the gap is modest — under ₹50,000. Over fifteen years it is over ₹7 lakh, because the
      advantage compounds. This is why the comparison matters more the longer you hold, and why a five-year
      view can mislead you into choosing the wrong instrument.
    </p>

    <h2 class="guide-h2">Three saver profiles</h2>
    <p class="guide-p">
      <strong>Salaried, 30% slab, 15-year horizon.</strong> PPF to the ₹1.5 lakh limit every year. The
      combination of 80C and tax-free compounding is hard to beat with anything carrying similar risk.
    </p>
    <p class="guide-p">
      <strong>Freelancer, variable income, 20% slab.</strong> Keep a year of expenses liquid first. Then NSC
      for the fixed rate, because a fixed return matters more than the last 40 basis points when income varies.
    </p>
    <p class="guide-p">
      <strong>Retiree, 65, needs income.</strong> SCSS for the guaranteed quarterly payout and the sovereign
      guarantee above ₹5 lakh — not PPF, which pays nothing out for fifteen years.
    </p>

    <h2 class="guide-h2">The mistake that costs the most</h2>
    <p class="guide-p">
      Breaking a PPF in year four for a house deposit. The penalty is the interest rate applied to the
      premature closure, plus the loss of the entire tax-free compounding that motivated the account. If there
      is any chance you need the money inside ten years, it does not belong in PPF — and that decision is made
      when you open the account, not when you close it.
    </p>
"""

DIVIDEND2 = """
    <h2 class="guide-h2">A worked case with real numbers</h2>
    <p class="guide-p">
      A company with a twenty-five-year record, a share price of ₹400, and a dividend of ₹16 last year. Yield:
      4%. Earnings per share are ₹18, so the payout ratio is 89%. Free cash flow per share is ₹14 — less than
      the dividend paid.
    </p>
    <p class="guide-p">
      Read the three numbers together and the picture is clear: the company is paying out more than it
      generates, funding the gap from the balance sheet. The streak is intact, the yield looks attractive, and
      the dividend is at risk. A dividend investor who only read the record would buy this.
    </p>
    <p class="guide-p">
      Now change one number. If free cash flow per share were ₹30, the same 89% payout would be comfortable,
      and the 4% yield would be genuinely safe. Same yield, same streak, opposite conclusion.
    </p>

    <h2 class="guide-h2">Tax, worked through</h2>
    <p class="guide-p">
      ₹2 lakh of dividends in a year, 30% slab with cess. Tax is about ₹62,400. The net dividend income is
      ₹1.38 lakh, not ₹2 lakh. TDS at 10% will already have been deducted by the company, so the additional tax
      payable is about ₹42,400. Anyone planning income from dividends should plan on the post-tax number, which
      is a third smaller than the headline.
    </p>

    <h2 class="guide-h2">What the streak is genuinely good for</h2>
    <p class="guide-p">
      As a first filter that removes companies with no record of returning cash at all. That is a real and
      useful function: it cuts a universe of hundreds to a shortlist of dozens. It just cannot be the last
      filter, because it measures the past and does not describe the balance sheet in front of you.
    </p>
"""

SCSS2 = """
    <h2 class="guide-h2">The tax filing detail that returns money</h2>
    <p class="guide-p">
      Interest from SCSS is taxable, and the post office or bank will deduct TDS above the threshold. If your
      total income is below the taxable limit — common for retirees living on interest and a small pension —
      submit Form 15H so no TDS is deducted at all. If TDS was already deducted, file the return and claim it
      back.
    </p>
    <p class="guide-p">
      This is not a technicality. On ₹30 lakh at 8.20%, the annual interest is ₹2.46 lakh. A 10% TDS is
      ₹24,600 withheld each year — real money for a household on a fixed income, and routinely left unclaimed.
    </p>

    <h2 class="guide-h2">SCSS against the alternatives, in one table</h2>
    <p class="guide-p">
      <strong>Rate:</strong> SCSS 8.20% · PPF 7.10% · senior FD typically 7.25–7.75% · debt fund variable.<br>
      <strong>Guarantee:</strong> SCSS sovereign · PPF sovereign · FD bank (₹5 lakh insured) · fund none.<br>
      <strong>Payout:</strong> SCSS quarterly · PPF at maturity · FD quarterly or at maturity · fund at
      redemption.<br>
      <strong>Liquidity:</strong> SCSS after one year with penalty · PPF from year six · FD immediate with
      penalty · fund 1–2 days.<br>
      <strong>Tax:</strong> SCSS taxable · PPF exempt · FD taxable · fund taxed at slab or 12.5% LTCG.
    </p>

    <h2 class="guide-h2">The decision in one sentence</h2>
    <p class="guide-p">
      If you are over 60, need the income now, and will not touch the capital for five years, SCSS is the
      default — and the only question left is how much of your corpus should be locked rather than how much
      should be in SCSS.
    </p>
"""

PARENTS2 = """
    <h2 class="guide-h2">The family conversation</h2>
    <p class="guide-p">
      Most policies for parents are bought by adult children, and the decision usually involves money that is
      not entirely the buyer's. Two things are worth settling before you compare premiums: who pays the annual
      premium if it rises by 20% at 70, and who is the nominee. Both are easier to agree in a calm year than
      during a hospital admission.
    </p>

    <h2 class="guide-h2">A worked cost comparison</h2>
    <p class="guide-p">
      Policy A: ₹10 lakh, 20% co-payment, ₹38,000 premium. Policy B: ₹10 lakh, no co-payment, ₹52,000 premium.
      One hospitalisation of ₹4 lakh in the next five years:
    </p>
    <p class="guide-p">
      A pays ₹3.2 lakh and the family pays ₹80,000. B pays ₹4 lakh. Over five years A costs ₹1.9 lakh in
      premium, B costs ₹2.6 lakh. A single admission wipes out A's saving and then some.
    </p>
    <p class="guide-p">
      The arithmetic only works in favour of the cheaper premium if nobody is hospitalised — which is not a bet
      worth making on a parent over 65.
    </p>

    <h2 class="guide-h2">Three documents to keep</h2>
    <p class="guide-p">
      The proposal form you signed, the policy schedule, and the renewal receipts. At claim time the insurer
      will ask what was declared; the proposal form is the only record that settles it. Photograph all three
      and keep them in one folder that the whole family can reach.
    </p>
"""

RATES2 = """
    <h2 class="guide-h2">How a notification is actually made</h2>
    <p class="guide-p">
      The Finance Ministry issues a gazette notification, usually in the last week of the quarter, setting the
      rate for each small-savings instrument for the following quarter. The National Savings Institute publishes
      the same table for savers. Between notifications, the rate cannot change — so a rate quoted without the
      quarter it belongs to is ambiguous by definition.
    </p>

    <h2 class="guide-h2">What the bond market is telling you now</h2>
    <p class="guide-p">
      The ten-year government bond yield is the reference point. When it falls below the level implied by the
      current small-savings rate, the formula points to a cut; when it rises, to an increase. The government has
      historically moved slowly in both directions, so a large gap between the formula and the notified rate is
      usually closed over several quarters rather than at once.
    </p>
    <p class="guide-p">
      The practical use of this: watch the yield for direction, not for the exact next number. If yields have
      fallen for two quarters and the small-savings rate has not moved, a cut is more likely than an increase —
      which is the moment to consider locking a fixed rate through NSC or SCSS.
    </p>

    <h2 class="guide-h2">Why the headline table is not enough</h2>
    <p class="guide-p">
      A table of rates tells you what you earn this quarter. It does not tell you whether the rate floats, when
      it resets, or what happens to money already deposited. Those three facts decide which product is right,
      and none of them appear in the table. That is the gap this site's plan pages are built to close.
    </p>
"""

EMERGENCY2 = """
    <h2 class="guide-h2">Where to hold it, worked through</h2>
    <p class="guide-p">
      ₹3 lakh of emergency fund, held in a savings account at 3%: ₹9,000 a year before tax. In a liquid fund
      at 6.5%: about ₹19,500 — roughly ₹10,500 more, at the cost of one-day redemption and a NAV that can dip
      slightly.
    </p>
    <p class="guide-p">
      Is ₹10,500 worth the friction? For most households, yes — provided the fund is genuinely liquid and
      genuinely separate. For a household with irregular income and no other savings, the certainty of the
      savings account is worth more than the extra interest.
    </p>

    <h2 class="guide-h2">The three-month test</h2>
    <p class="guide-p">
      If you lost your income tomorrow, how many months could you cover essentials without borrowing or
      selling anything? Count only money available within 48 hours, in cash or a bank account. That number is
      your real emergency cover, whatever your total savings say.
    </p>
    <p class="guide-p">
      Most people discover the number is smaller than they assumed — often because the "savings" is in a
      fifteen-year PPF and the current account is spent by the 25th.
    </p>

    <h2 class="guide-h2">When to use it</h2>
    <p class="guide-p">
      Use it without guilt when the three-part test is met. Then rebuild on the same automated schedule. The
      failure mode is not using the fund — it is using it for something that fails the test and then having
      nothing left when the real emergency arrives.
    </p>
"""

EXTRAS = {
    "health-policy": POLICY,
    "tax": TAX2,
    "dividend": DIVIDEND2,
    "scss": SCSS2,
    "parents": PARENTS2,
    "rates": RATES2,
    "emergency": EMERGENCY2,
}
