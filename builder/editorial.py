"""About the editor — the human accountable for the site.

AdSense reviewers look for ownership. This page exists so the site has a name,
a method and a way to be held to it.
"""

from __future__ import annotations

from .site import esc


def page(editor: dict, today: str) -> str:
    name = editor.get("name") or "the editor"
    location = editor.get("location") or "India"
    started = editor.get("since") or "2026"
    why = editor.get("why") or (
        "India has more ways to save than almost anywhere else, and very little plain information "
        "about where to start. PaisaClear exists to close that gap."
    )
    email_page = "feedback.html"

    return f"""
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="index.html">Home</a></li><li aria-current="page">About the editor</li>
    </ol></nav>
    <h1>About the editor</h1>
    <p class="page-lede">
      PaisaClear is written and maintained by one person, {esc(name)}, based in {esc(location)}.
      There is no content team, no syndicated feed and no automated text generation on this site.
    </p>
    <p class="page-meta">Last reviewed {esc(today)}</p>
  </div>
</section>

<section class="section">
  <div class="shell shell-narrow">
    <h2 class="guide-h2">Why this site exists</h2>
    <p class="guide-p">{esc(why)}</p>
    <p class="guide-p">
      A rate printed without a date is not information. It is a guess wearing a suit. PaisaClear exists to
      publish the figure, the date it was true, and the link to where it came from — for every product on the
      site, on every page.
    </p>

    <h2 class="guide-h2">How the site is produced</h2>
    <ul class="check-list">
      <li><span><strong>Rates are fetched, not typed.</strong> Small-savings rates, bond yields and fund NAVs come from official sources on a schedule, and every figure carries its own date.</span></li>
      <li><span><strong>Product records are reviewed by hand.</strong> Each record states who it suits, what it costs, what the lock-in is and what to check before buying — written, not scraped.</span></li>
      <li><span><strong>The site is checked daily.</strong> An automated audit fails loudly if any published rate has gone stale, if a link breaks, or if a page loses its metadata.</span></li>
      <li><span><strong>Corrections come first.</strong> If a figure is wrong, fixing it takes priority over publishing anything new.</span></li>
    </ul>

    <h2 class="guide-h2">What this site will not do</h2>
    <p class="guide-p">
      It will not recommend a product, take a payment, sell your data, or publish a number without saying when
      it was true. The site is not registered with SEBI as an investment adviser, and nothing on it is advice.
      The <a href="disclaimer.html">disclaimer</a> sets out the limits in full.
    </p>

    <h2 class="guide-h2">How to hold me to it</h2>
    <p class="guide-p">
      If you find a figure that is wrong, a rate that has moved, or a claim you think is unsupported, tell me
      through the <a href="{email_page}">contact form</a>. Corrections are published on the page itself, and
      the date at the top changes when a page is reviewed — so you can see whether what you are reading has
      been checked recently.
    </p>

    <h2 class="guide-h2">Editorial independence</h2>
    <p class="guide-p">
      The site does not currently earn commission from any product it describes. If that changes, the affected
      pages will say so at the top, and payment will never decide how a product is described or whether it is
      listed at all.
    </p>

    <p class="guide-src">
      Contact: <a href="{email_page}">the contact form</a> · Method: <a href="how-we-work.html">how we work</a> ·
      Terms: <a href="terms.html">terms of use</a>
    </p>
  </div>
</section>
"""
