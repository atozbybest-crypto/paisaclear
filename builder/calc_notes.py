"""Guidance appended to the calculator pages.

Each calculator had ~150 words of copy around an interactive tool — thin for a
reviewer and thin for a reader. These add the explanation that belongs next to
a calculator: what the inputs mean and where people go wrong.
"""

SAVINGS = """
    <h2 class="guide-h2">What the boxes actually mean</h2>
    <p class="guide-p">
      <strong>Amount:</strong> what you put in each time. For a lump sum, the whole amount once. For a monthly
      deposit, the instalment. Mixing the two is the most common mistake — a ₹1.5 lakh yearly deposit is not the
      same as ₹12,500 a month, because the monthly payments start earning earlier in the year.
    </p>
    <p class="guide-p">
      <strong>Rate:</strong> the annual rate, not the monthly one. If a product quotes 7.1% a year, enter 7.1.
      Entering 0.59 (the monthly equivalent) will understate the result by a wide margin.
    </p>
    <p class="guide-p">
      <strong>Years:</strong> the full term the money stays invested, including any period after you stop
      depositing. For PPF that is 15 years of deposits and 15 years of interest — not 15 years of both.
    </p>

    <h2 class="guide-h2">Where the answer misleads people</h2>
    <p class="guide-p">
      The calculator compounds interest assuming the rate never changes. For PPF and Sukanya Samriddhi that is
      not true: the rate is notified every quarter and applies to the whole balance. A 20 basis point cut over
      fifteen years changes the maturity figure by lakhs.
    </p>
    <p class="guide-p">
      It also ignores tax on the way out. A fixed deposit at 7.1% in the 30% slab keeps about 4.9% after tax;
      the calculator will happily show you the 7.1% figure unless you lower the rate yourself. For a tax-free
      product, leaving the rate as it is happens to be correct.
    </p>

    <h2 class="guide-h2">How to use it honestly</h2>
    <p class="guide-p">
      Run it twice: once at the current rate, once at a rate one percentage point lower. If the second number
      would still meet your goal, the plan is robust. If it would not, the plan depends on a rate nobody has
      promised — which is worth knowing before you commit.
    </p>
"""

LOAN = """
    <h2 class="guide-h2">The three inputs, and the one that matters most</h2>
    <p class="guide-p">
      <strong>Principal:</strong> the amount borrowed, not the property price. If you are buying a ₹60 lakh flat
      with ₹12 lakh down, the principal is ₹48 lakh.
    </p>
    <p class="guide-p">
      <strong>Rate:</strong> the annual rate on the sanction letter. Floating-rate loans are usually quoted as a
      spread over a benchmark — the rate you enter should be the current effective rate, not the spread.
    </p>
    <p class="guide-p">
      <strong>Tenure:</strong> the total term. Tenure moves the EMI more than people expect: on ₹48 lakh at 8.5%,
      20 years costs about ₹41,600 a month and 30 years about ₹36,900 — but the longer loan costs roughly ₹18
      lakh more in interest. The lower EMI is not the cheaper loan.
    </p>

    <h2 class="guide-h2">What the EMI number leaves out</h2>
    <p class="guide-p">
      Processing fees, insurance bundled with the loan, stamp duty, and the cost of any prepayment penalty.
      It also assumes the rate never changes — which is wrong for every floating-rate loan in India. When the
      benchmark moves, your EMI or your tenure changes, and the total interest moves with it.
    </p>

    <h2 class="guide-h2">The prepayment question</h2>
    <p class="guide-p">
      A prepayment goes entirely to principal, so the saving is not the EMI it removes but all the interest that
      principal would have earned over the remaining term. On a 20-year loan, prepaying in year five saves far
      more than the same amount prepaid in year fifteen. Run the calculator with a shorter tenure to see what
      aggressive repayment would do.
    </p>

    <h2 class="guide-h2">A rule worth keeping</h2>
    <p class="guide-p">
      Keep the EMI under about 35% of take-home pay. Above that, a single emergency forces the loan to be
      restructured — usually at a worse rate.
    </p>
"""

PLANNING = """
    <h2 class="guide-h2">What this calculator is solving</h2>
    <p class="guide-p">
      Most people start with a product — an FD, a fund, a policy — and hope it is enough. This tool runs the
      question the other way round: given a goal amount, a horizon and a rate you are willing to assume, what
      must you set aside each month?
    </p>
    <p class="guide-p">
      <strong>Goal:</strong> the amount you need, in today's money. If the goal is ten years away and inflation
      runs at 6%, the target should be inflated — ₹10 lakh today is about ₹17.9 lakh in ten years.
    </p>
    <p class="guide-p">
      <strong>Horizon:</strong> the years until you need the money. This is the single most important input,
      because it decides what you can hold. Money needed in three years cannot be in equity; money needed in
      fifteen can.
    </p>
    <p class="guide-p">
      <strong>Expected return:</strong> what you assume the money earns. Being optimistic here is the most
      expensive mistake in planning — it lowers the required monthly saving and leaves you short at the end.
    </p>

    <h2 class="guide-h2">Why the assumed return should be conservative</h2>
    <p class="guide-p">
      A 12% assumption on a 15-year goal produces a comfortable monthly figure. A 9% assumption on the same goal
      raises it by roughly a quarter. Only one of those is a plan; the other is a hope with a spreadsheet around
      it. Run both and judge whether you could survive the higher number.
    </p>

    <h2 class="guide-h2">What it cannot tell you</h2>
    <p class="guide-p">
      It cannot tell you whether a product will actually deliver the return you assumed, and it does not adjust
      for tax, which can take a third of a taxable return. It also assumes you make every payment — the most
      common real-world failure is not the wrong rate, it is the missed month.
    </p>
"""

SPENDING = """
    <h2 class="guide-h2">Why tracking spending before investing makes sense</h2>
    <p class="guide-p">
      A savings rate is a decision, not an outcome. You cannot decide to save 20% until you know what the other
      80% is doing. This planner exists to show where the money actually goes before you commit to a product or
      a monthly deposit.
    </p>
    <p class="guide-p">
      The numbers are stored only in your browser — nothing is uploaded — which means you can be honest in them
      without any of it leaving the page.
    </p>

    <h2 class="guide-h2">How to enter it usefully</h2>
    <p class="guide-p">
      Use last month's actual bank statement rather than a remembered average. Most people underestimate
      discretionary spending by a third and overestimate how much they saved.
    </p>
    <p class="guide-p">
      Separate <strong>fixed</strong> commitments — rent, EMI, school fees, insurance premiums — from
      <strong>variable</strong> ones. The fixed block is what an emergency fund has to cover; the variable block
      is what you can actually change this month.
    </p>

    <h2 class="guide-h2">What to look for in the result</h2>
    <p class="guide-p">
      Three things. Whether your essentials exceed half your income — above that, saving is hard and one shock
      is dangerous. Whether any single category is above 30% — concentration is where budgets break. And whether
      the savings figure matches what actually left your account, because a plan that assumes savings you did not
      make is not a plan.
    </p>

    <h2 class="guide-h2">The next step</h2>
    <p class="guide-p">
      Once you know the monthly surplus, the emergency fund comes first, then the goal calculator can tell you
      what that surplus becomes over a decade. Doing it in the other order — picking a product before knowing the
      surplus — is how people end up with a policy they cannot fund.
    </p>
"""

SALARY = """
    <h2 class="guide-h2">Why take-home is much lower than CTC</h2>
    <p class="guide-p">
      Cost to company includes the employer's provident fund contribution, gratuity and often insurance — money
      that never reaches your bank account. Between CTC and take-home sit four deductions: employee PF, income
      tax, professional tax and any variable pay that has not vested.
    </p>
    <p class="guide-p">
      The gap is usually 20% to 35%. A ₹12 lakh CTC commonly lands between ₹8.5 lakh and ₹9.5 lakh a year in
      hand, depending on the structure and the tax regime chosen.
    </p>

    <h2 class="guide-h2">The inputs that change the answer most</h2>
    <p class="guide-p">
      <strong>Basic salary:</strong> PF is 12% of basic, so a structure with a low basic has a higher take-home
      but a smaller retirement corpus. That is a trade, not a trick.
    </p>
    <p class="guide-p">
      <strong>Tax regime:</strong> old versus new changes the answer materially at most income levels. The new
      regime has lower slabs and no 80C deductions; the old one rewards PPF, ELSS and home-loan interest.
    </p>
    <p class="guide-p">
      <strong>Declarations:</strong> HRA, 80C, 80D and home-loan interest reduce TDS through the year. Not
      declaring them means a large tax deduction in the final months, or a refund much later.
    </p>

    <h2 class="guide-h2">What this estimate does not include</h2>
    <p class="guide-p">
      Variable pay, RSUs, joining bonuses, gratuity and employer NPS contributions. It also assumes a full year
      of service. If you joined mid-year or switched jobs, two Form 16s and a possible double standard deduction
      can change the final number considerably.
    </p>
"""

INCOME_TAX = """
    <h2 class="guide-h2">How to use this calculator</h2>
    <p class="guide-p">
      Choose your category first — individual, HUF, firm or company — because the slabs and deductions are
      different for each. Then enter gross total income, which is income after subtracting the deductions you
      claim, not your CTC.
    </p>
    <p class="guide-p">
      Every field is blank on purpose. A pre-filled example creates a wrong impression of what you will owe, and
      the numbers are meaningless until they are yours.
    </p>

    <h2 class="guide-h2">Old regime versus new — the decision</h2>
    <p class="guide-p">
      The new regime has wider slabs but gives up most deductions. The old regime keeps 80C, 80D, HRA and
      home-loan interest, but taxes at higher slab rates. Which wins depends almost entirely on how much you
      claim: a salaried taxpayer with ₹2.5 lakh of deductions often does better in the old regime; one with almost
      none does better in the new.
    </p>
    <p class="guide-p">
      Run both and compare the final tax, not the slab rates. The regime with the lower headline rate is
      frequently the more expensive one.
    </p>

    <h2 class="guide-h2">What this does not cover</h2>
    <p class="guide-p">
      Capital gains, which are taxed at their own rates and reported separately. Surcharge on very high incomes
      is included where applicable, but marginal relief and special-rate incomes are not. It is an estimate to
      help you plan a budget — the return you file is prepared from your actual documents.
    </p>
    <p class="guide-p">
      Slabs and rebates change every Budget. The figures used here are dated on the page; check them against the
      current Finance Act before relying on any number for planning.
    </p>
"""

NOTES = {
    "calculators/savings.html": SAVINGS,
    "calculators/loan.html": LOAN,
    "calculators/planning.html": PLANNING,
    "calculators/spending.html": SPENDING,
    "calculators/salary.html": SALARY,
    "calculators/income-tax.html": INCOME_TAX,
}
