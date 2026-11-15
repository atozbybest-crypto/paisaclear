"""Long-form articles, batch one — ~2,000 words each."""

from __future__ import annotations

from .articles import _shell

HEALTH_POLICY = _shell(
    "How to read a health insurance policy: the five clauses that decide your claim",
    "The premium is what you pay. These five clauses decide what you get back — and none of them are on the brochure.",
    "Reviewed 15 November 2026",
    """
    <p class="guide-p">
      Two health policies can quote the same sum insured, the same premium and the same hospital network, and
      behave completely differently when you claim. The difference lives in five clauses buried in the policy
      wording. Read them before you pay, in this order.
    </p>
    <p class="guide-p">
      This is not a comparison of insurers. It is a method for reading any policy, in about forty minutes, so
      that you know what you have bought before the hospital asks you to sign an admission form.
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
      maternity usually have their own clocks — often longer than the general pre-existing period. A policy
      with a two-year pre-existing wait can still have a four-year wait on knee replacement.
    </p>
    <p class="guide-p">
      <strong>What to do:</strong> search the wording for "waiting period" and read every mention, not just the
      first. There are usually three: the initial waiting period (30 days for everything except accidents), the
      specific-disease waiting period, and the pre-existing waiting period. They run in parallel and the longest
      one applies.
    </p>

    <h2 class="guide-h2">2. Room rent limits — the clause that costs the most</h2>
    <p class="guide-p">
      A policy capping room rent at 1% of sum insured per day does more damage than people expect. When your
      room exceeds the cap, most insurers apply a <em>proportionate deduction</em> to the entire bill, not just
      the room charge.
    </p>
    <p class="guide-p">
      On a ₹5 lakh cover, a 1% cap is ₹5,000 a day. Admit yourself to an ₹8,000 room and the insurer may reduce
      the whole claim by the same ratio — paying 62% of the surgeon's fee, the ICU charge, the medicines, the
      lot. The clause with the smallest print has the largest effect on what you receive.
    </p>
    <p class="guide-p">
      Single private room without a cap is worth paying for. If the choice is ₹4 lakh with no room cap or
      ₹6 lakh with a 1% cap, the smaller policy with no cap often settles more.
    </p>
    <p class="guide-p">
      <strong>The arithmetic, worked:</strong> a ₹3 lakh bill, of which ₹40,000 is the room. With no cap, the
      insurer pays close to the lot. With a 1% cap on ₹5 lakh (₹5,000 a day) and an eight-day stay at ₹8,000,
      the allowed room rent is ₹40,000 against ₹64,000 billed — a ratio of 62%. Applied proportionately across
      the bill, the insurer pays roughly ₹1.87 lakh and you pay ₹1.13 lakh. The room cost you ₹1.13 lakh of
      your own money, not ₹24,000.
    </p>

    <h2 class="guide-h2">3. Sub-limits on specific treatments</h2>
    <p class="guide-p">
      A ₹10 lakh policy does not mean ₹10 lakh for everything. Cataract surgery may be capped at ₹40,000 per
      eye; maternity at ₹50,000; cardiac procedures at a percentage of sum insured. These are separate ceilings
      inside the main one.
    </p>
    <p class="guide-p">
      Ask for the sub-limit table in writing. If an insurer will not give it before you buy, that is your
      answer. The table usually sits in the policy schedule, not the wording, and it is the single document
      most people never read.
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
    <p class="guide-p">
      A useful rule: never accept a co-payment above 10% unless the alternative is no cover at all. Co-payment
      is permanent; a premium saving is not.
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

    <h2 class="guide-h2">Beyond the five: four more things worth finding</h2>
    <ul class="check-list">
      <li><span><strong>Day-care procedures.</strong> Cataract, dialysis, chemotherapy and many others no longer need a night's stay. Confirm they are covered without hospitalisation.</span></li>
      <li><span><strong>Ambulance and consumables.</strong> Consumables — gloves, syringes, implants — are often excluded or capped. On a large surgery this is a real bill.</span></li>
      <li><span><strong>Pre and post hospitalisation.</strong> 30 and 60 days is standard; 90 and 180 is better, and it covers the diagnostics before and after admission.</span></li>
      <li><span><strong>Network hospitals.</strong> Check the insurer's list yourself, for your city and your preferred hospital, rather than asking the agent.</span></li>
    </ul>

    <h2 class="guide-h2">A forty-minute reading routine</h2>
    <p class="guide-p">
      Search the PDF for these words in order: <em>waiting</em>, <em>room</em>, <em>sub-limit</em>,
      <em>co-pay</em>, <em>restoration</em>, <em>exclusion</em>. Read the paragraph before and after each hit.
      That gives you a working understanding of the policy in under an hour, and it is more than most buyers
      ever do.
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
      That number is misleading for two of the three, because they are taxed differently. Here is the
      arithmetic, with the assumptions stated.
    </p>

    <h2 class="guide-h2">The numbers used here</h2>
    <ul class="check-list">
      <li><span><strong>PPF:</strong> 7.10%, notified for the quarter beginning 1 October 2026 — exempt, exempt, exempt.</span></li>
      <li><span><strong>Bank FD:</strong> 7.10% assumed, for comparison. Interest taxed at your slab.</span></li>
      <li><span><strong>NSC:</strong> 7.70%, notified for the same quarter. Interest taxed at your slab.</span></li>
    </ul>
    <p class="guide-p">
      The 4% health and education cess is added to your slab rate, so 30% becomes 31.2%, 20% becomes 20.8% and
      5% becomes 5.2%. Surcharge above ₹50 lakh income is ignored here for clarity.
    </p>

    <h2 class="guide-h2">The only number that matters: after-tax yield</h2>
    <p class="guide-p">
      After-tax yield = headline rate × (1 − your effective slab). At the 30% slab:
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
    <ul class="check-list">
      <li><span><strong>5% slab:</strong> FD at 7.10% keeps 6.73%; NSC at 7.70% keeps 7.30%. PPF at 7.10% still wins against the FD, loses narrowly to NSC.</span></li>
      <li><span><strong>20% slab:</strong> FD at 7.10% keeps 5.62%; NSC at 7.70% keeps 6.10%. PPF wins clearly.</span></li>
      <li><span><strong>Below the taxable threshold:</strong> no tax is due on FD interest at all. A higher-rate taxable product genuinely pays more, and this is the one case where the conventional advice reverses.</span></li>
    </ul>

    <h2 class="guide-h2">A worked example over fifteen years</h2>
    <p class="guide-p">
      ₹1,50,000 a year for fifteen years, at the rates above, 30% slab:
    </p>
    <p class="guide-p">
      PPF at 7.10% tax-free: about <strong>₹40.7 lakh</strong> at maturity, tax already settled.<br>
      FD at 7.10%, compounded and taxed annually: about <strong>₹33.1 lakh</strong> in hand after tax.<br>
      NSC at 7.70% in five-year certificates rolled over, taxed annually: about <strong>₹35.4 lakh</strong>.
    </p>
    <p class="guide-p">
      The differences are not rounding. They come from one clause in the tax code, not from the interest rate.
      Over fifteen years the gap between PPF and the FD is roughly ₹7.6 lakh on ₹22.5 lakh deposited.
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
    <p class="guide-p">
      <strong>Reinvestment risk on NSC.</strong> Each five-year certificate must be reinvested at whatever rate
      is then on offer. The 7.70% is not a fifteen-year rate; it is a five-year rate repeated three times with
      unknown future rates.
    </p>

    <h2 class="guide-h2">Three arithmetic errors people make</h2>
    <ul class="check-list">
      <li><span><strong>Comparing compounded FD interest with paid-out interest.</strong> An FD that pays interest out and an NSC that compounds are not comparable at the same rate. Reinvest the FD payout to compare fairly.</span></li>
      <li><span><strong>Forgetting TDS.</strong> TDS is not a final tax. If your slab is below the TDS rate, claim the refund — many savers never do.</span></li>
      <li><span><strong>Ignoring the 80C limit.</strong> The deduction is capped at ₹1.5 lakh across all instruments. Depositing ₹3 lakh into PPF does not give ₹3 lakh of deduction.</span></li>
    </ul>

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

DIVIDEND = _shell(
    "What a 25-year dividend streak actually predicts",
    "A long record is evidence of a habit. It is not a forecast — and the difference costs people money.",
    "Reviewed 15 November 2026",
    """
    <p class="guide-p">
      A company that has paid a dividend every year for twenty-five years is making a statement about how it
      runs itself. It is not making a promise about next year. Investors routinely confuse the two, and the
      confusion is expensive because the shares that carry the longest records are usually the ones trading at
      a premium for exactly that reason.
    </p>

    <h2 class="guide-h2">What the streak actually tells you</h2>
    <p class="guide-p">
      Three things, and all three are useful.
    </p>
    <ul class="check-list">
      <li><span><strong>The board treats the dividend as a commitment.</strong> Companies cut dividends reluctantly, because the market punishes the cut harder than it rewards the increase. A twenty-five-year record means several boards, across several downturns, chose to protect the payout.</span></li>
      <li><span><strong>Cash has been real, not accounting.</strong> A dividend is paid in rupees. A company cannot pay one for twenty-five years out of paper profits alone.</span></li>
      <li><span><strong>Capital allocation has been disciplined.</strong> Paying out cash means not spending it on everything else — a signal about management's restraint.</span></li>
    </ul>

    <h2 class="guide-h2">What it does not tell you</h2>
    <p class="guide-p">
      It does not tell you the dividend will be maintained. It does not tell you the payout is affordable
      today. And it does not tell you the share price is a good price.
    </p>
    <p class="guide-p">
      Two numbers matter more than the length of the record: the <strong>payout ratio</strong> — the share of
      earnings paid out — and <strong>free cash flow</strong>, the money actually available after the company
      has paid for its own upkeep. A company paying 90% of earnings as dividend has no room to absorb a bad
      year without cutting. A company paying 30% of strong free cash flow could double the dividend and still
      be comfortable.
    </p>
    <p class="guide-p">
      A twenty-five-year streak funded by borrowing is not a record of strength. It is a record of a balance
      sheet being spent.
    </p>

    <h2 class="guide-h2">The yield illusion</h2>
    <p class="guide-p">
      Yield is dividend divided by price. A high yield is either a generous company or a falling share price,
      and the market is usually telling you something when it prices a stock at 8%. Run the total return —
      dividend plus price movement over five years — before you call a stock an income stock.
    </p>
    <p class="guide-p">
      A 2% yield on a share that has compounded at 12% a year beats a 7% yield on a share that has traded flat
      for a decade. The second one is not income; it is a slow return of your own capital.
    </p>

    <h2 class="guide-h2">The cyclical trap</h2>
    <p class="guide-p">
      Long dividend records cluster in sectors with steady, contract-like cash flows: utilities, mining,
      fertilisers, consumer staples. They are rarer in sectors that swing hard. That is not an accident — it is
      arithmetic. A commodity producer with a long record has usually survived by paying small, sustainable
      dividends rather than large, impressive ones.
    </p>

    <h2 class="guide-h2">The traps specific to Indian dividend investing</h2>
    <p class="guide-p">
      <strong>Dividends are taxed at your slab.</strong> Since 2020 the dividend is taxed in your hands, with
      TDS above the threshold. A 4% dividend in the 30% slab is 2.7% after tax. Compare that with what the same
      money would earn in a tax-free small-savings scheme before you call it income.
    </p>
    <p class="guide-p">
      <strong>The share price moves independently.</strong> A 4% dividend on a stock that fell 20% is not
      income; it is a smaller loss. This is the single most common error in dividend investing.
    </p>
    <p class="guide-p">
      <strong>A streak is history, not a covenant.</strong> Companies are under no obligation to keep paying.
      Several long records on the Indian market have been broken in bad years, and each time the share price
      fell further than the dividend was worth.
    </p>

    <h2 class="guide-h2">Four questions to ask before buying a dividend payer</h2>
    <ol class="guide-list">
      <li><strong>Is the dividend covered by free cash flow?</strong> If the payout exceeds free cash flow for two years running, it is being funded by the balance sheet.</li>
      <li><strong>What is the payout ratio against earnings?</strong> Under 50% is comfortable in most sectors; above 80% needs a reason.</li>
      <li><strong>Is the business cyclical?</strong> A commodity producer's dividend follows the commodity, whatever the record says.</li>
      <li><strong>What does the debt look like?</strong> Rising debt with a steady dividend is a warning, not a comfort.</li>
    </ol>

    <h2 class="guide-h2">How to use a streak properly</h2>
    <p class="guide-p">
      Treat it as a filter, not a signal. Start with companies that have paid for a long time, then read three
      things yourself: the payout ratio against earnings, free cash flow against the dividend, and the debt on
      the balance sheet. If all three hold, the record is meaningful. If any one fails, the record is a
      coincidence that has not yet ended.
    </p>
    <p class="guide-p">
      The <a href="categories/dividend-champions.html">Dividend Champions records</a> on this site list the
      last ten payments for each company, with the date of each. Use the dates to see whether the dividend has
      been rising, flat or slipping — the pattern matters more than the count.
    </p>
    """,
)

SCSS = _shell(
    "Senior Citizens' Savings Scheme: when it beats a fixed deposit",
    "The highest rate available to most retirees is not automatically the best place for the money. Here is where it wins and where it ties your hands.",
    "Reviewed 15 November 2026",
    """
    <p class="guide-p">
      SCSS pays 8.20%, notified for the quarter beginning 1 October 2026. A senior-citizen fixed deposit at a
      large bank typically pays 0.25% to 0.50% above its normal rate. On paper SCSS usually wins. After tax and
      after the practical restrictions, the answer depends on how much you need the money to stay put.
    </p>

    <h2 class="guide-h2">The arithmetic</h2>
    <p class="guide-p">
      SCSS pays interest quarterly and returns the capital at maturity after five years. The interest is
      taxable at your slab, and TDS applies above the threshold. At the 20% slab with cess, an 8.20% SCSS
      deposit keeps about <strong>6.49%</strong>; at the 30% slab about <strong>5.64%</strong>.
    </p>
    <p class="guide-p">
      A senior FD at 7.75% keeps about <strong>6.14%</strong> at 20% and <strong>5.33%</strong> at 30%. On
      ₹20 lakh, the difference is roughly ₹7,000 to ₹12,000 a year — worth knowing, and worth checking against
      what your bank actually offers before you decide.
    </p>

    <h2 class="guide-h2">What SCSS gives you that a deposit does not</h2>
    <ul class="check-list">
      <li><span><strong>A government guarantee</strong>, not a bank one. Above ₹5 lakh, a bank deposit depends on the bank; SCSS depends on the sovereign.</span></li>
      <li><span><strong>A rate fixed for five years</strong>, notified when you invest. If rates fall, yours does not.</span></li>
      <li><span><strong>80C eligibility</strong> on the deposit, in the old regime.</span></li>
      <li><span><strong>Extension</strong> by three years at maturity, with the rate then in force.</span></li>
    </ul>

    <h2 class="guide-h2">What it takes away</h2>
    <p class="guide-p">
      <strong>The money is locked.</strong> Premature closure is allowed after one year, with a penalty on the
      rate already paid. Close it in the first year and you may get back less than you put in after adjustment.
    </p>
    <p class="guide-p">
      <strong>Interest is paid out, not compounded.</strong> That is deliberate — this is an income product —
      but it means the ₹20 lakh does not grow. If you do not need the quarterly income, you will need to
      reinvest it yourself, and the rate on that reinvestment is unknown today.
    </p>
    <p class="guide-p">
      <strong>There is a ceiling.</strong> ₹30 lakh per depositor, including extensions. Above that, SCSS
      cannot hold your whole corpus.
    </p>

    <h2 class="guide-h2">The comparison nobody runs</h2>
    <p class="guide-p">
      Against PPF, SCSS pays more and is available only to those over 60. Against a bank FD, SCSS pays more
      and is safer above ₹5 lakh. Against a debt mutual fund, SCSS has no interest-rate risk on the capital and
      no expense ratio — but also no liquidity.
    </p>
    <p class="guide-p">
      The honest way to compare is on the money you actually need. Split the corpus: five years of expenses
      that must never move, and the rest that can. SCSS is well suited to the part that must never move. It is
      a poor fit for money you may need for a medical bill or a family obligation next year.
    </p>

    <h2 class="guide-h2">The reinvestment problem, worked out</h2>
    <p class="guide-p">
      ₹30 lakh at 8.20% pays ₹2.46 lakh a year, or about ₹20,500 a quarter. If you spend the interest, the
      capital stays at ₹30 lakh for five years while prices rise around it — an inflation problem, not a
      default risk.
    </p>
    <p class="guide-p">
      If instead you reinvest each quarter into a recurring deposit at 6.5%, you end with roughly ₹2 lakh more
      than the untouched interest — a meaningful difference over five years, and the arithmetic most people
      never run. The catch is that you have to actually do it, every quarter, for five years.
    </p>

    <h2 class="guide-h2">Small practical points that catch people out</h2>
    <p class="guide-p">
      Open it at a post office or an authorised bank — the rate is the same. Bring proof of age, because the
      60-year threshold is checked. If you are between 55 and 60 and retired on superannuation or under a VRS,
      you can open one within a month of receiving your retirement benefits, subject to conditions; that window
      is narrow and worth diarising.
    </p>
    <p class="guide-p">
      The quarterly interest lands in your savings account. If TDS is deducted, file for a refund when you
      submit your return — many retirees overpay tax simply by not claiming it. Submit Form 15H if your total
      income is below the taxable limit and you want TDS stopped at source.
    </p>
    <p class="guide-p">
      Current rate and the quarter it applied: see the <a href="plans/senior-citizens-savings-scheme.html">SCSS
      page</a>, and run your own numbers in the <a href="calculators/savings.html">savings calculator</a>.
    </p>
    """,
)
