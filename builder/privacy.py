"""Privacy page — written around what the site actually does, not boilerplate."""

from __future__ import annotations


def privacy(ctx: dict) -> str:
    return """
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="index.html">Home</a></li><li aria-current="page">Privacy</li>
    </ol></nav>
    <h1>Privacy</h1>
    <p class="page-lede">
      This site has no accounts, no payments and no advertising trackers. It collects very little, and this
      page says exactly what that is.
    </p>
    <p class="page-meta">Last updated 21 October 2026</p>
  </div>
</section>

<section class="section">
  <div class="shell shell-narrow">
    <div class="privacy-body">

      <h2>The short version</h2>
      <ul class="check-list">
        <li><span>No account, no sign-in, no newsletter signup.</span></li>
        <li><span>No cookies are set by this site.</span></li>
        <li><span>No advertising or cross-site tracking scripts.</span></li>
        <li><span>What you type into the planners stays in your browser.</span></li>
        <li><span>If you send feedback, we get your message and — only if you type it — your email.</span></li>
      </ul>

      <h2>What is collected, and why</h2>

      <h3>Feedback you send us</h3>
      <p>
        The feedback form asks for your name, your email, what the message is about, which page it concerns and
        the message itself. Name, email and the page field are optional. The message is required.
      </p>
      <p>
        That submission is stored by our hosting provider, Netlify, and sent to the site owner by email. We use
        it for one purpose: to check the report and, where you asked for a reply, to answer you. We do not use
        it for marketing and we do not sell it. Submissions are kept until the report is resolved, and for up to
        twelve months afterwards.
      </p>

      <h3>Visit statistics</h3>
      <p>
        We use <strong>Netlify Analytics</strong>, which is built from the hosting provider's own server logs
        rather than from a script in the page. It records the pages requested, the time, an approximate
        location derived from the network address, the referring site and the browser type.
      </p>
      <p>
        It sets no cookies and does not track you across other websites. The figures are aggregated: we see that
        a page had visitors, not who they were. There is no third-party analytics script on any page — if you
        view the source, you will not find Google Analytics, Meta Pixel or similar.
      </p>

      <h3>The planners and calculators</h3>
      <p>
        The salary, savings, loan, emergency-fund and retirement calculators do their arithmetic in your
        browser. Nothing you type is sent to us, and nothing is stored once you close the page.
      </p>
      <p>
        The spending planner is the one exception, and it is deliberate: what you log is saved in your
        browser's local storage <em>on your device</em> so the list survives a reload. It is never transmitted.
        Clearing your browser data deletes it, and we cannot recover it because we never had it.
      </p>

      <h3>Search and hosting</h3>
      <p>
        The site is served by Netlify, which necessarily processes the request when you load a page. Search
        Console is used to see which queries bring people here from Google — that data is aggregate search
        performance, not a record of individual visitors.
      </p>

      <h2>Cookies</h2>
      <p>
        This site sets no cookies of its own, which is why you will not see a cookie banner. If that changes,
        this page changes first.
      </p>

      <h2>Your choices</h2>
      <ul class="check-list">
        <li><span><strong>Ask what we hold.</strong> Send a feedback message and we will tell you what was received from you.</span></li>
        <li><span><strong>Ask us to delete it.</strong> We will remove any feedback submission and anything derived from it.</span></li>
        <li><span><strong>Correct it.</strong> Tell us which field is wrong and we will fix or delete the record.</span></li>
        <li><span><strong>Withdraw.</strong> Any reply you asked for stops when you ask us to stop.</span></li>
      </ul>
      <p>
        Use the <a href="feedback.html">feedback form</a> for any of these, and mention that your message is a
        privacy request so it is handled separately from corrections.
      </p>

      <h2>What this site does not do</h2>
      <ul class="check-list">
        <li><span>No selling or renting of personal data.</span></li>
        <li><span>No behavioural profiling or advertising audiences.</span></li>
        <li><span>No tracking pixels embedded by third parties.</span></li>
        <li><span>No payments, so no card or bank details are ever collected.</span></li>
        <li><span>No accounts, so there are no passwords for us to hold.</span></li>
      </ul>

      <h2>Children</h2>
      <p>
        The site explains financial products for adults considering them. It is not directed at children, and we
        do not knowingly collect information from anyone under 18.
      </p>

      <h2>Changes to this page</h2>
      <p>
        If what the site collects changes — for example, if a newsletter is ever added — this page is updated
        before the change goes live, and the date at the top changes with it.
      </p>

      <p class="privacy-foot">
        Questions about any of this can go through the <a href="feedback.html">feedback form</a>.
        That is the only contact route, and it is deliberately the only one.
      </p>
    </div>
  </div>
</section>
"""
