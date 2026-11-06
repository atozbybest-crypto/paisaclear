"""Legal pages required for advertising review: terms and disclaimer."""

from __future__ import annotations

from .site import icon


def terms() -> str:
    return """
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="index.html">Home</a></li><li aria-current="page">Terms of use</li>
    </ol></nav>
    <h1>Terms of use</h1>
    <p class="page-lede">The rules for using PaisaClear. Short, because the site is simple.</p>
    <p class="page-meta">Last updated 6 November 2026</p>
  </div>
</section>

<section class="section">
  <div class="shell shell-narrow">
    <h2 class="guide-h2">What this site is</h2>
    <p class="guide-p">
      PaisaClear is a free reference site about financial products available in India. It explains how products
      work, what they cost and what to check. It is published for general information.
    </p>

    <h2 class="guide-h2">What you agree to</h2>
    <ul class="check-list">
      <li>""" + icon("check", "icon icon-sm") + """<span>Use the site lawfully, and do not attempt to disrupt it or scrape it at a volume that degrades service for others.</span></li>
      <li>""" + icon("check", "icon icon-sm") + """<span>Understand that figures shown are as of the date printed on the page, and may have changed since.</span></li>
      <li>""" + icon("check", "icon icon-sm") + """<span>Verify anything important with the provider before acting on it.</span></li>
    </ul>

    <h2 class="guide-h2">Accuracy</h2>
    <p class="guide-p">
      We take care to date and source every figure, and the site is checked daily for stale data. Even so, we
      cannot promise that every number is current or error-free. Rates are revised by the government, insurers
      and fund houses without notice to us. If you spot something wrong, tell us — corrections take priority
      over new content.
    </p>

    <h2 class="guide-h2">No advice, no intermediary</h2>
    <p class="guide-p">
      Nothing here is investment, tax, insurance or legal advice, and we are not registered with SEBI as an
      investment adviser. PaisaClear does not sell products, does not accept deposits, does not execute
      transactions and does not act as an agent for any provider.
    </p>

    <h2 class="guide-h2">Our content</h2>
    <p class="guide-p">
      The text, layout and calculators on this site are ours. You may link to any page and quote short
      excerpts with attribution. You may not republish substantial parts of the site, or present it as your
      own. Product names and provider names belong to their owners and are used only to identify the product.
    </p>

    <h2 class="guide-h2">Links to other sites</h2>
    <p class="guide-p">
      We link to official sources, providers, and news publishers. We do not control those sites and are not
      responsible for their content, their accuracy or their privacy practices.
    </p>

    <h2 class="guide-h2">Advertising</h2>
    <p class="guide-p">
      The site may display advertising, including through Google. Advertising is separate from editorial
      content: an advertiser cannot pay for a favourable write-up, and products are never ranked by who pays.
      See the <a href="privacy.html">privacy page</a> for how advertising cookies work.
    </p>

    <h2 class="guide-h2">Liability</h2>
    <p class="guide-p">
      The site is provided as it is. To the extent the law allows, we are not liable for any loss arising from
      use of the site or reliance on its content. That includes investment losses, missed deadlines and errors
      in third-party data.
    </p>

    <h2 class="guide-h2">Changes</h2>
    <p class="guide-p">
      These terms may change as the site grows. The date at the top of the page is always the current version.
      Continued use after a change means you accept it.
    </p>

    <p class="guide-src">
      Governed by the laws of India. Questions about these terms: use the
      <a href="feedback.html">contact form</a>.
    </p>
  </div>
</section>
"""


def disclaimer() -> str:
    return """
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="index.html">Home</a></li><li aria-current="page">Disclaimer</li>
    </ol></nav>
    <h1>Disclaimer</h1>
    <p class="page-lede">
      PaisaClear explains financial products. It does not recommend them, and it is not an adviser. Read this
      before you act on anything here.
    </p>
    <p class="page-meta">Last updated 6 November 2026</p>
  </div>
</section>

<section class="section">
  <div class="shell shell-narrow">
    <h2 class="guide-h2">Not investment advice</h2>
    <p class="guide-p">
      The content on this site is general information, not advice tailored to you. We do not know your income,
      your obligations, your tax position or your goals, so nothing here can tell you what to buy, hold or sell.
      PaisaClear is not a SEBI-registered investment adviser and does not provide portfolio management services.
    </p>

    <h2 class="guide-h2">Markets and returns</h2>
    <p class="guide-p">
      Returns shown for funds and ETFs are calculated from published NAV history and are past performance.
      Past performance does not predict future returns. The value of a market-linked investment falls as well
      as rises, and you can get back less than you put in.
    </p>

    <h2 class="guide-h2">Rates change</h2>
    <p class="guide-p">
      Every rate on this site carries the date it applied. Small-savings rates are notified quarterly, bond
      yields move daily, and insurers revise premiums without notice to us. Treat any figure older than the
      page's stated date as historical.
    </p>

    <h2 class="guide-h2">Calculators are estimates</h2>
    <p class="guide-p">
      The calculators use the inputs you provide and the assumptions printed beside each result. They do not
      account for every rule — tax slabs, surcharge, cess, penalties, revision of rates or changes in
      regulation. Use them to understand how a product behaves, not to plan an exact outcome.
    </p>

    <h2 class="guide-h2">Health insurance</h2>
    <p class="guide-p">
      Plan features on the health insurance pages are the insurer's own description of their product,
      reproduced without independent verification. We do not compare premiums, and a listing is not an
      endorsement. Waiting periods, sub-limits, room-rent caps and exclusions in the policy wording decide
      every claim.
    </p>

    <h2 class="guide-h2">Scam checker</h2>
    <p class="guide-p">
      The scam checker matches wording patterns commonly used in financial fraud. It cannot confirm that a
      message is genuine, and a low score is not a clean bill of health. It has no access to call databases,
      bank records or any fraud registry, and it does not store what you paste.
    </p>

    <h2 class="guide-h2">Dividend records</h2>
    <p class="guide-p">
      Payment dates and amounts are taken from public market data. A long record of paying dividends is history,
      not a promise: a company can reduce or stop a dividend at any time, and share prices fall as well as rise.
    </p>

    <h2 class="guide-h2">News and third-party links</h2>
    <p class="guide-p">
      Headlines on the news page are published by other organisations and linked back to them. We do not write
      or edit those stories, and a link is not an endorsement of the report.
    </p>

    <h2 class="guide-h2">Affiliate relationships</h2>
    <p class="guide-p">
      PaisaClear does not currently earn commission from any product on this site. If that changes, affected
      pages will say so in plain language at the top, and payment will never influence a rating or a ranking.
    </p>

    <p class="guide-src">
      If something here looks wrong, tell us through the <a href="feedback.html">contact form</a> — corrections
      take priority.
    </p>
  </div>
</section>
"""
