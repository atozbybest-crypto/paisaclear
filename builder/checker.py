"""Scam red-flag checker page — patterns, never a verdict."""

from __future__ import annotations

from .site import icon


def page() -> str:
    return """
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="index.html">Home</a></li><li aria-current="page">Scam checker</li>
    </ol></nav>
    <h1>Scam checker</h1>
    <p class="page-lede">
      Paste a message, a phone number or a link you are unsure about. We highlight the patterns that appear
      in known scams — then you verify through the official channel. This is a red-flag checker, not a verdict.
    </p>
    <p class="page-meta">Runs in your browser · nothing is sent anywhere</p>
  </div>
</section>

<section class="section">
  <div class="shell checker-layout">
    <form class="checker-form" id="scam-form">
      <label class="finder-label" for="scam-input">What did you receive?</label>
      <textarea id="scam-input" class="it-input checker-input" rows="7"
        placeholder="Paste the message, number or link here. Example: Dear customer, your SBI account will be blocked in 24 hours. Update KYC at sbi-kyc-verify.com"></textarea>
      <div class="it-actions">
        <button class="btn btn-primary" type="submit">Check for red flags</button>
        <button class="btn btn-ghost" type="reset" id="scam-reset">Clear</button>
      </div>
    </form>

    <div class="checker-results" id="scam-results" aria-live="polite">
      <p class="finder-placeholder">Nothing checked yet.</p>
    </div>
  </div>
</section>

<section class="section section-tint">
  <div class="shell shell-narrow">
    <div class="calc-notes">
      <h2>What this can and cannot do</h2>
      <ul class="check-list">
        <li>""" + icon("check", "icon icon-sm") + """<span>It recognises wording and link patterns that appear in real scams: urgency, OTP requests, lookalike domains, UPI collect requests.</span></li>
        <li>""" + icon("alert", "icon icon-sm") + """<span><strong>It cannot tell you something is genuine.</strong> A clean result only means the usual patterns are absent — not that the message is safe.</span></li>
        <li>""" + icon("alert", "icon icon-sm") + """<span>It has no access to call databases, bank records or the RBI fraud registry. Those are the only sources that can confirm a number or account.</span></li>
        <li>""" + icon("check", "icon icon-sm") + """<span>Always verify by calling the number printed on your bank card or on the bank's own website — never a number in the message.</span></li>
      </ul>
      <p class="muted">
        Reporting: <a href="https://cybercrime.gov.in" target="_blank" rel="noopener noreferrer">cybercrime.gov.in</a>
        or 1930 · <a href="feedback.html">tell us about a scam you received</a>
      </p>
    </div>
  </div>
</section>

<script>
/* Red-flag checker. Deterministic patterns; no network, no verdict. */
(function () {
  "use strict";
  var form = document.getElementById("scam-form");
  if (!form) return;
  var input = document.getElementById("scam-input");
  var out = document.getElementById("scam-results");

  var RULES = [
    { name: "Urgency or a deadline", why: "Scams create time pressure so you act before checking.",
      test: /(within \\d+\\s*(hour|hr|minute|min)|immediately|urgent|last (date|chance)|today itself|expire[sd]?)/i },
    { name: "Asks for OTP, PIN or CVV", why: "No bank, wallet or company ever asks for these.",
      test: /(otp|one[- ]time password|pin\\b|cvv|card number|aadhaar number|net ?banking password)/i },
    { name: "Link that does not match the brand", why: "Real banks use their own domain, not hyphens and extra words.",
      test: /(https?:\\/\\/)?(?:[a-z0-9-]+\\.)*(sbi|hdfc|icici|axis|kotak|paytm|phonepe|gpay|amazon|flipkart)[a-z0-9-]*\\.(?!co\\.in|com\\/?|in\\/?)[a-z]{2,}/i },
    { name: "Shortened or unfamiliar link", why: "Short links hide the real destination.",
      test: /(bit\\.ly|tinyurl|t\\.co|is\\.gd|rebrand\\.ly|linktr\\.ee|[a-z0-9-]+\\.(xyz|top|club|online|site|live)\\b)/i },
    { name: "UPI collect or QR request", why: "Receiving money never requires approving a collect request or scanning a QR.",
      test: /(upi|collect request|scan (this )?qr|google pay|phonepe|paytm).{0,40}(approve|accept|scan|request)/i },
    { name: "Prize, lottery or refund you did not ask for", why: "Unexpected winnings and refunds are bait.",
      test: /(lottery|lucky (draw|winner)|prize|you have won|cash ?back of|refund of|scratch card)/i },
    { name: "Threat of account block or legal action", why: "Fear is used to bypass your judgement.",
      test: /(account (will be )?(blocked|suspended|frozen)|legal action|fir\\b|police case|court notice|deactivated)/i },
    { name: "Asks you to install an app or share screen", why: "Remote-access apps let a scammer see your banking screen.",
      test: /(install (this|anydesk|teamviewer|quick ?support)|screen shar|remote access|apk)/i },
    { name: "Job, loan or investment with no paperwork", why: "Payments before paperwork are the signature of a scam.",
      test: /(work from home|earn \\d+|guaranteed (return|profit)|registration fee|processing fee|security deposit).{0,60}(pay|transfer|send)/i },
    { name: "Grammar and formatting oddities", why: "Mass-sent scams rarely read like official communication.",
      test: /(dear (customer|user|sir\\/madam)|kindly (do|update|verify)|your account has been)/i }
  ];

  function esc(text) {
    return String(text).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function render() {
    var text = (input.value || "").trim();
    if (!text) {
      out.innerHTML = '<p class="finder-placeholder">Paste a message to check.</p>';
      return;
    }
    var hits = RULES.filter(function (rule) { return rule.test.test(text); });

    var header;
    if (hits.length === 0) {
      header = '<div class="checker-verdict is-clear"><strong>None of the usual patterns matched.</strong>' +
        "<p>That does not make it genuine — it only means this message avoids the obvious wording. " +
        "If it asks for money or details, verify through the official app or the number on your card.</p></div>";
    } else {
      header = '<div class="checker-verdict is-flagged"><strong>' + hits.length +
        (hits.length === 1 ? " red flag found" : " red flags found") + ".</strong>" +
        "<p>Do not act on this message. Verify by calling the number on your bank card or the company's own " +
        "website — never a number or link inside the message.</p></div>";
    }

    var list = hits.map(function (rule) {
      return '<li><strong>' + esc(rule.name) + "</strong><span>" + esc(rule.why) + "</span></li>";
    }).join("");

    out.innerHTML = header + (list ? '<ul class="checker-list">' + list + "</ul>" : "") +
      '<p class="calc-fineprint">Checked in your browser. Nothing you typed was sent to us or stored.</p>';
  }

  form.addEventListener("submit", function (event) { event.preventDefault(); render(); });
  form.addEventListener("input", render);
  var reset = document.getElementById("scam-reset");
  if (reset) reset.addEventListener("click", function () {
    window.setTimeout(function () {
      out.innerHTML = '<p class="finder-placeholder">Nothing checked yet.</p>';
    }, 0);
  });
})();
</script>
"""
