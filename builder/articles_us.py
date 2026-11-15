"""US investing from India — the cross-border article."""

from __future__ import annotations

from .articles import _shell

ARTICLE = _shell(
    "Buying US stocks from India: the rules, the taxes and the trap nobody mentions",
    "Remittance limits, TCS, dividend withholding, and a US estate-tax exposure that most Indian investors do not know exists.",
    "Reviewed 15 November 2026",
    """
    <p class="guide-p">
      Buying a US-listed share from India takes about ten minutes on a brokerage app. Understanding what you have
      bought — and what it exposes you to — takes a little longer. This is the part the apps do not put on the
      sign-up screen.
    </p>

    <h2 class="guide-h2">1. Getting money out: the remittance route</h2>
    <p class="guide-p">
      Money sent abroad by a resident Indian goes under the RBI's Liberalised Remittance Scheme, which has an
      annual ceiling per person — currently USD 250,000. Investments in foreign securities fall inside that
      ceiling, alongside travel, education and gifts, so the limit is shared across everything you remit in a
      year.
    </p>
    <p class="guide-p">
      Your bank handles the remittance and asks for a purpose code. Investing abroad has its own code, and using
      the wrong one creates a paperwork problem later, usually when money comes back.
    </p>

    <h2 class="guide-p">
      <strong>The TCS point.</strong> Remittances above a threshold attract tax collected at source. TCS is not a
      tax on your income — it is a prepayment that you credit against your final liability when you file. But it
      is cash out of your pocket for months, and for a large remittance it is a real amount to plan for. The
      threshold and rate have changed more than once; check the current rule before you remit.
    </p>

    <h2 class="guide-h2">2. Tax on the way in: dividends</h2>
    <p class="guide-p">
      US dividends are subject to US withholding tax at source — 25% for Indian residents under the treaty, and
      often 30% if the correct form has not been filed with the broker. Filing the form that claims treaty
      benefits is worth 5 percentage points on every dividend, every year.
    </p>
    <p class="guide-p">
      India then taxes the same dividend in your hands, and gives you a foreign tax credit for what was withheld.
      To claim it you need the US tax statement from your broker and the right schedule in your return. Without
      the paperwork, you pay twice.
    </p>

    <h2 class="guide-h2">3. Tax on the way out: capital gains</h2>
    <p class="guide-p">
      Gains on US shares held for more than 24 months are long-term for an Indian resident, taxed at the
      long-term rate with indexation unavailable for foreign assets. Held for less, they are short-term and taxed
      at your slab. The US itself generally does not tax capital gains of a non-resident, so the liability sits
      with India.
    </p>
    <p class="guide-p">
      The awkward part is reporting: foreign holdings must be disclosed in the return, and the rupee value
      changes with the exchange rate on the day of each transaction. A share that went nowhere in dollars can
      produce a rupee gain, or a loss, purely from the currency.
    </p>

    <h2 class="guide-h2">4. The trap: US estate tax</h2>
    <p class="guide-p">
      This is the one almost nobody mentions. US-situated assets — including shares of US companies — held by a
      non-resident are potentially subject to US estate tax on death, above a threshold far lower than the one
      that applies to US citizens. For an Indian investor holding a meaningful sum in US shares, that exposure is
      real, and it is not covered by the India–US tax treaty in the way people assume.
    </p>
    <p class="guide-p">
      The practical workarounds are known: keep exposure through an India-domiciled fund that invests abroad
      rather than holding US shares directly, or hold through an Irish-domiciled ETF, which is not a US-situated
      asset. Each has its own cost and tax profile, and each is a decision worth taking advice on rather than
      inferring from a blog.
    </p>
    <p class="guide-p">
      The point of raising it here is not to give a solution. It is that the risk exists, it scales with the
      size of the holding, and it is invisible on a brokerage app.
    </p>

    <h2 class="guide-h2">5. Direct shares, an Indian fund, or a US ETF</h2>
    <p class="guide-p">
      <strong>Direct US shares</strong> give control and transparency, and bring estate-tax exposure, per-trade
      costs and a tax return that is harder to file.
    </p>
    <p class="guide-p">
      <strong>An Indian fund that invests abroad</strong> keeps everything domestic: no remittance, no TCS, no
      US estate exposure, taxed like any other Indian mutual fund. The cost is a higher expense ratio and the
      fund manager's choices.
    </p>
    <p class="guide-p">
      <strong>A US-domiciled ETF</strong> is cheap and liquid, with the same estate-tax profile as direct shares.
      An Irish-domiciled equivalent usually avoids that exposure and can be more tax-efficient on dividends.
    </p>

    <h2 class="guide-h2">What the ten-minute signup does not tell you</h2>
    <ul class="check-list">
      <li><span><strong>Currency is a position.</strong> A 12% dollar return with a 6% rupee appreciation is roughly a 6% return in rupees.</span></li>
      <li><span><strong>Reporting is mandatory, not optional.</strong> Foreign assets belong in your return even in years you did not sell.</span></li>
      <li><span><strong>Small amounts are not worth the compliance.</strong> Below a few lakh, an Indian fund investing abroad is usually simpler and no more expensive after accounting for fees and paperwork.</span></li>
      <li><span><strong>Rules change.</strong> The remittance ceiling, the TCS threshold and the treaty rates have all moved in the last few years. Verify before you act.</span></li>
    </ul>

    <h2 class="guide-h2">Where to look at the US side here</h2>
    <p class="guide-p">
      The <a href="us-market.html">US market page</a> carries indices, Treasury yields and the largest ETFs with
      the date each figure was observed. The <a href="us-companies.html">US companies page</a> shows revenue and
      filings straight from SEC EDGAR, so the numbers come from the company rather than a summary of it.
    </p>
    <p class="guide-p">
      Neither page recommends anything. What they do is let you look at a US business with the same discipline
      this site applies to Indian products: the figure, the date, and the source.
    </p>
    """,
)
