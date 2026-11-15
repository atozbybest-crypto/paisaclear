"""Extra sections that take batch-one articles to around 2,000 words each."""

HEALTH_POLICY_EXTRA = """
    <h2 class="guide-h2">Six claims, and which clause decides each one</h2>
    <p class="guide-p">
      The clauses only matter in combination, and the combination is easier to see in examples. These six are
      ordinary Indian hospital situations.
    </p>
    <p class="guide-p">
      <strong>A cataract operation, day care, ₹55,000 billed.</strong> The policy has a ₹40,000 sub-limit per
      eye. The insurer pays ₹40,000; you pay ₹15,000 plus any consumables excluded. No waiting period applies if
      the policy is older than the specified-disease wait.
    </p>
    <p class="guide-p">
      <strong>A knee replacement, ₹4.2 lakh, in a ₹6,000 room.</strong> The cap is 1% of ₹5 lakh, which is
      ₹5,000 a day. On a six-day stay the room is over by ₹6,000, and because the room exceeded the cap, the
      insurer applies proportionate deduction to the whole bill: it pays roughly 83%, or ₹3.5 lakh. You pay
      ₹70,000, of which only ₹6,000 was the actual room overrun.
    </p>
    <p class="guide-p">
      <strong>A cardiac stent at 14 months, with a policy bought at 62.</strong> The pre-existing wait is three
      years and the insured had hypertension declared at proposal. The claim is examined for whether the
      condition existed before the policy. If the insurer links it, the claim is rejected in full — with the
      premium refunded. This is why the definition of pre-existing is the single most important sentence in the
      document.
    </p>
    <p class="guide-p">
      <strong>A second hospitalisation in the same year, same family floater.</strong> The sum insured is
      exhausted by the first. Restoration decides whether the second claim is paid at all, and most policies
      restore only for a different illness, once a year.
    </p>
    <p class="guide-p">
      <strong>Maternity, planned, in year two.</strong> A two-year waiting period applies. The claim falls
      inside the wait and is excluded, even though the policy is "two years old" by calendar. Waiting periods
      run from the policy start date, not from the date of the last renewal.
    </p>
    <p class="guide-p">
      <strong>Dengue, five days, ₹90,000, first month of a new policy.</strong> The initial waiting period of
      30 days excludes everything except accidents. The claim is rejected — a fact that surprises people
      annually during monsoon.
    </p>

    <h2 class="guide-h2">Questions people ask after reading the wording</h2>
    <p class="guide-p">
      <strong>Does a higher sum insured fix a room-rent cap?</strong> Sometimes. If the cap is expressed as a
      percentage of sum insured, doubling the cover doubles the allowed room rent. If it is a fixed rupee
      amount, it does not move.
    </p>
    <p class="guide-p">
      <strong>Is a 30-day initial waiting period negotiable?</strong> Not usually, but accidents are covered
      from day one in most policies. Read whether the policy separates accident cover from illness cover.
    </p>
    <p class="guide-p">
      <strong>What happens if I switch insurers?</strong> Waiting periods are not always carried forward.
      Some insurers credit the previous policy's continuity if you switch without a gap, some do not. Ask
      specifically, and get it in writing before you move.
    </p>
    <p class="guide-p">
      <strong>Do I need a separate critical illness policy?</strong> Different product. Health indemnity pays
      hospital bills; critical illness pays a lump sum on diagnosis. The second covers income loss and
      non-medical costs, and it does not replace the first.
    </p>
    <p class="guide-p">
      <strong>Is a top-up worth it?</strong> A top-up begins paying after a deductible, which is usually
      satisfied by the base policy's cover. It is a cheap way to raise total protection, provided the deductible
      matches what the base policy actually pays.
    </p>
"""

TAX_EXTRA = """
    <h2 class="guide-h2">The same comparison at four rate combinations</h2>
    <p class="guide-p">
      Rates change, so the conclusion should not depend on one number. Here is the after-tax yield at four
      combinations a saver might actually face, at the 30% slab:
    </p>
    <p class="guide-p">
      7.10% tax-free (PPF) → <strong>7.10%</strong><br>
      7.10% taxable (FD) → <strong>4.88%</strong><br>
      7.70% taxable (NSC) → <strong>5.30%</strong><br>
      8.20% taxable (SCSS, if eligible) → <strong>5.64%</strong>
    </p>
    <p class="guide-p">
      The ordering holds across every plausible rate in the current cycle. Only when the taxable rate approaches
      10.3% does it overtake a 7.10% tax-free return — and no small-savings or bank product is within two
      percentage points of that today.
    </p>

    <h2 class="guide-h2">What happens if the PPF rate is cut</h2>
    <p class="guide-p">
      PPF's rate is notified quarterly and applies to the whole balance. A cut from 7.10% to 6.90% reduces the
      return on everything you have already saved, not just on new deposits. That is the opposite of an FD,
      which fixes its rate when booked, and the opposite of NSC, which fixes its rate for its five-year term.
    </p>
    <p class="guide-p">
      Over a fifteen-year holding period, a 20 basis point cut compounded is not trivial: on a ₹22.5 lakh
      deposit schedule it is roughly ₹1.1 lakh at maturity. Which is why the "floating versus fixed" choice
      inside these products is a real decision, not a rounding error.
    </p>

    <h2 class="guide-h2">The liquidity ladder</h2>
    <p class="guide-p">
      A reasonable structure for someone in the 30% slab with a long horizon:
    </p>
    <ol class="guide-list">
      <li><strong>Three to six months of expenses</strong> in a savings account or liquid fund. Not PPF. This is the emergency fund and it exists to protect the rest.</li>
      <li><strong>PPF to the ₹1.5 lakh 80C limit</strong>, for the tax-free compounding and the 80C deduction together.</li>
      <li><strong>NSC or a fixed deposit</strong> for money needed in three to five years, where a fixed rate matters more than the last 40 basis points.</li>
      <li><strong>SCSS</strong>, if eligible, for the part of the corpus that must produce income and must not fall in value.</li>
    </ol>
    <p class="guide-p">
      The order is deliberate: liquidity first, tax-free growth second, fixed rates for dated goals third.
      Reversing it is how people end up breaking a PPF in year four for a medical bill.
    </p>

    <h2 class="guide-h2">Questions people ask</h2>
    <p class="guide-p">
      <strong>Can I have both PPF and NSC?</strong> Yes, and many savers do. The ₹1.5 lakh 80C limit applies
      across both, so the deduction does not double.
    </p>
    <p class="guide-p">
      <strong>Is the PPF interest really tax-free above ₹2.5 lakh a year?</strong> Contributions above ₹2.5 lakh
      in a financial year do not earn tax-free interest. For most savers the ₹1.5 lakh cap makes this
      irrelevant, but for a family pooling contributions into one account it matters.
    </p>
    <p class="guide-p">
      <strong>Does a joint PPF account exist?</strong> No. One account per person. A guardian may open one for
      a minor.
    </p>
    <p class="guide-p">
      <strong>What if I miss a year of PPF deposits?</strong> The account does not close and does not lapse, but
      a year without the ₹500 minimum earns no interest for that year. It can be revived with a small penalty.
    </p>
    <p class="guide-p">
      <strong>Are NSC and KVP the same thing?</strong> No. NSC pays interest that accumulates to maturity over
      five years; KVP doubles your money over roughly 115 months with no periodic interest at all. KVP also has
      no 80C benefit.
    </p>
"""

DIVIDEND_EXTRA = """
    <h2 class="guide-h2">How to read a ten-payment history</h2>
    <p class="guide-p">
      A list of the last ten dividends, with dates, tells you more than a streak count ever will. Read it in
      three passes.
    </p>
    <p class="guide-p">
      <strong>First, the direction.</strong> Are the amounts rising, flat or falling? A company paying ₹2, ₹2,
      ₹2.5, ₹3 over a decade is growing the payout; one paying ₹5, ₹5, ₹4, ₹3 is shrinking it while the streak
      stays intact. The record survives a cut as long as something is paid.
    </p>
    <p class="guide-p">
      <strong>Second, the frequency.</strong> Annual, interim plus final, or quarterly. Indian companies usually
      pay once or twice a year. If the ten payments span two years, the company pays often; if they span ten
      years, it pays annually.
    </p>
    <p class="guide-p">
      <strong>Third, the gaps.</strong> An unusually large payment followed by a small one often signals a
      special dividend — a one-off return of cash, usually from an asset sale. Do not build income expectations
      on a special dividend.
    </p>

    <h2 class="guide-h2">Three patterns worth recognising</h2>
    <p class="guide-p">
      <strong>The steady compounder.</strong> Small, rising payouts, low payout ratio, strong free cash flow.
      Boring, and the most reliable of the three.
    </p>
    <p class="guide-p">
      <strong>The cash cow.</strong> High payout ratio, flat revenue, no growth. The dividend is real but the
      share price goes nowhere, and the total return is roughly the dividend minus inflation.
    </p>
    <p class="guide-p">
      <strong>The stretched payer.</strong> High yield, rising debt, payout above free cash flow. The market is
      pricing in a cut before the company announces one. This is where most dividend investors lose money.
    </p>

    <h2 class="guide-h2">Why the streak survives a bad year</h2>
    <p class="guide-p">
      Because the streak measures whether <em>something</em> was paid, not whether the amount held. A company can
      cut its dividend by 70% and keep a twenty-five-year record intact. When you read "25 years of dividends",
      ask what the dividend was in the worst of those years.
    </p>

    <h2 class="guide-h2">Questions people ask</h2>
    <p class="guide-p">
      <strong>Is a dividend stock safer than a growth stock?</strong> No. It has a different return profile.
      A dividend payer can still fall 40%. The dividend is a component of return, not a form of protection.
    </p>
    <p class="guide-p">
      <strong>Should I reinvest dividends?</strong> For a long horizon, usually yes — but remember the dividend
      arrives after tax, so reinvestment compounds a smaller amount than the headline yield suggests.
    </p>
    <p class="guide-p">
      <strong>What is a good yield?</strong> There is no universal number. Compare the yield with the
      government bond yield: if a stock yields less than a five-year G-sec, you are being paid nothing for
      taking equity risk.
    </p>
    <p class="guide-p">
      <strong>Do dividends signal a healthy company?</strong> They signal a company with cash. Whether it is
      healthy depends on debt, growth and the industry — the dividend cannot tell you that on its own.
    </p>
"""

SCSS_EXTRA = """
    <h2 class="guide-h2">Who SCSS suits, and who it does not</h2>
    <p class="guide-p">
      <strong>It suits</strong> a retiree over 60 with a lump sum that must produce regular income and must not
      fall in value. Someone with no pension, or a pension that covers only part of monthly expenses. Someone
      who wants the money to be government-backed rather than bank-backed above ₹5 lakh.
    </p>
    <p class="guide-p">
      <strong>It does not suit</strong> someone who may need the capital within five years — a house purchase,
      a family obligation, a medical contingency. It does not suit someone whose entire savings is under ₹10
      lakh, because locking it all for five years removes the cushion that matters most. And it does not suit
      anyone still working and in the 30% slab, who cannot open one anyway.
    </p>

    <h2 class="guide-h2">SCSS against the three alternatives, side by side</h2>
    <p class="guide-p">
      <strong>Against a bank FD:</strong> higher rate, sovereign guarantee, but no premature access without
      penalty. The FD wins on flexibility, SCSS wins on rate and safety above ₹5 lakh.
    </p>
    <p class="guide-p">
      <strong>Against PPF:</strong> SCSS pays more and pays it out; PPF compounds tax-free and stays liquid
      from year six. A couple can hold both — PPF for the spouse under 60, SCSS for the one over 60.
    </p>
    <p class="guide-p">
      <strong>Against a debt mutual fund:</strong> SCSS fixes the rate for five years and returns the capital;
      a debt fund's NAV moves with rates and its return is not guaranteed. SCSS wins on certainty, the fund wins
      on liquidity and indexation after three years.
    </p>

    <h2 class="guide-h2">A worked plan for ₹40 lakh</h2>
    <p class="guide-p">
      Suppose a retiree of 63 has ₹40 lakh and monthly expenses of ₹35,000.
    </p>
    <p class="guide-p">
      ₹30 lakh into SCSS at 8.20% pays ₹20,500 a quarter — roughly ₹6,800 a month. Not enough alone, but it is
      the guaranteed floor.
    </p>
    <p class="guide-p">
      ₹6 lakh stays in a savings account and a sweep FD as the medical and emergency cushion — about eight
      months of expenses. This is the money that prevents an SCSS premature closure.
    </p>
    <p class="guide-p">
      ₹4 lakh goes into a short-duration debt fund or a ladder of FDs maturing each year, to cover the gap
      between ₹6,800 and ₹35,000 a month, topped up by any pension.
    </p>
    <p class="guide-p">
      The point of the structure is not the returns. It is that no single event forces the locked money open.
    </p>

    <h2 class="guide-h2">Questions people ask</h2>
    <p class="guide-p">
      <strong>Can a husband and wife each open one?</strong> Yes. The ₹30 lakh cap is per depositor, so a couple
      can hold ₹60 lakh between them.
    </p>
    <p class="guide-p">
      <strong>What happens on the depositor's death?</strong> The nominee receives the deposit and interest up
      to the date of death. No penalty applies.
    </p>
    <p class="guide-p">
      <strong>Can I add money later?</strong> No. SCSS is a single deposit, unlike PPF. Additional money needs a
      second account within the cap.
    </p>
    <p class="guide-p">
      <strong>Is the interest credited automatically?</strong> Yes, quarterly, to the linked savings account.
      If it is not being reinvested, it is being spent — plan for that deliberately.
    </p>
    <p class="guide-p">
      <strong>What if rates rise after I open it?</strong> Your rate is fixed for the term. That is the trade
      for certainty, and it cuts both ways.
    </p>
"""

EXTRAS = {
    "health-policy": HEALTH_POLICY_EXTRA,
    "tax": TAX_EXTRA,
    "dividend": DIVIDEND_EXTRA,
    "scss": SCSS_EXTRA,
}
