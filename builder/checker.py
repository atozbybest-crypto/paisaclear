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
      Paste a message, a link or a number you are unsure about. We highlight everything that appears in known
      financial scams — then you verify through the official channel. This is a red-flag checker, not a verdict.
    </p>
    <p class="page-meta">Runs in your browser · nothing is sent anywhere</p>
  </div>
</section>

<section class="section">
  <div class="shell checker-layout">
    <form class="checker-form" id="scam-form">
      <label class="finder-label" for="scam-input">What did you receive?</label>
      <textarea id="scam-input" class="it-input checker-input" rows="8"
        placeholder="Paste the whole message, including any link or number. Example: Dear customer, your SBI account will be blocked in 24 hours. Complete KYC at http://sbi-kyc-verify.com and pay Rs 499"></textarea>
      <div class="it-actions">
        <button class="btn btn-primary" type="submit">Check for red flags</button>
        <button class="btn btn-ghost" type="reset" id="scam-reset">Clear</button>
      </div>
      <p class="field-hint">Paste the message as it arrived. The more of it you include, the more patterns we can match.</p>
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
        <li>""" + icon("check", "icon icon-sm") + """<span>It recognises the wording, links and payment requests that appear in real scams — twenty-four patterns, weighted by how dangerous each one is.</span></li>
        <li>""" + icon("alert", "icon icon-sm") + """<span><strong>It cannot tell you something is genuine.</strong> A low score means the usual patterns are absent, not that the message is safe.</span></li>
        <li>""" + icon("alert", "icon icon-sm") + """<span>It cannot check a phone number against a call database. There is no public list of scam numbers in India — only your bank and the cybercrime portal can act on one.</span></li>
        <li>""" + icon("check", "icon icon-sm") + """<span>Always verify by calling the number printed on your card or the one on the company's own website — never a number inside the message.</span></li>
      </ul>
      <p class="muted">
        Report it: <a href="https://cybercrime.gov.in" target="_blank" rel="noopener noreferrer">cybercrime.gov.in</a>
        or call 1930 · <a href="feedback.html">tell us about a scam you received</a>
      </p>
    </div>
  </div>
</section>

<script>
/* Red-flag checker.
   Twenty-four weighted patterns. It reports what matched; it never certifies
   a message as genuine, because it has no way to know that. */
(function () {
  "use strict";

  var form = document.getElementById("scam-form");
  if (!form) return;
  var input = document.getElementById("scam-input");
  var out = document.getElementById("scam-results");

  var RULES = [
    /* ---- critical: asking for a secret, or for you to move money ---- */
    { s: 3, name: "Asks for an OTP, PIN or CVV", why: "No bank, wallet, company or government office ever asks for these. Anyone who does is stealing from you.", re: /(otp|one[- ]?time password|verification code|pin\\b|cvv|card number|net ?banking password|mpin|grid card)/i },
    { s: 3, name: "Asks you to approve a UPI collect request", why: "Receiving money never needs you to approve a request. Approving one sends money out of your account.", re: /(collect request|approve (the )?request|upi request|scan (this |the )?qr|request money|paytm request)/i },
    { s: 3, name: "Asks you to install a remote-access app", why: "AnyDesk, TeamViewer and screen sharing let a scammer watch you type your banking password.", re: /(anydesk|team ?viewer|quick ?support|screen shar|remote access|install (this )?(app|apk)|apk file)/i },
    { s: 3, name: "Asks you to pay to receive something", why: "Fees before delivery, before a refund, before a prize, or before a loan is disbursed — that is the scam.", re: /(pay|transfer|send|deposit).{0,40}(fee|charges|tax|gst|processing|registration|security deposit|advance)/i },

    /* ---- high: impersonation and pressure ---- */
    { s: 2, name: "Link that imitates a brand's domain", why: "Real banks use their own domain. Extra words and hyphens — sbi-kyc-verify.com — are the giveaway.", re: /(?:https?:\\/\\/)?(?:[a-z0-9-]+\\.)*(sbi|hdfc|icici|axis|kotak|pnb|bob|canara|paytm|phonepe|gpay|amazon|flipkart|irctc|epfo|incometax|lic)[a-z0-9-]*\\.(?!co\\.in|com\\/?$|in\\/?$|org\\/?$)[a-z]{2,}/i },
    { s: 2, name: "Threat that the account will be blocked", why: "Fear is used to stop you checking. Banks do not switch off accounts by SMS.", re: /(account|card|sim|service).{0,25}(blocked|suspended|frozen|deactivated|disconnected|closed)/i },
    { s: 2, name: "Deadline measured in hours", why: "A real deadline survives a phone call to the official number. A fake one does not.", re: /(within \\d+ ?(hour|hr|minute|min)|in the next \\d+ ?(hour|minute)|before midnight|today itself|expires? (today|tonight))/i },
    { s: 2, name: "KYC, PAN or Aadhaar update demanded", why: "KYC is updated in the bank's app or branch, never through a link in a message.", re: /(kyc|e-?kyc|re-?kyc|pan (update|link|card)|aadha[ae]r (update|link|verify)|video kyc)/i },
    { s: 2, name: "Prize, lottery, refund or cashback you did not ask for", why: "Unexpected winnings are bait. You will be asked for a fee or your details to 'release' them.", re: /(lottery|lucky (draw|winner)|you have won|prize money|cash ?back of|scratch card|gift (worth|card)|refund of (rs|₹)?\\s?\\d)/i },
    { s: 2, name: "Impersonates a government office", why: "Income tax, GST, EPFO and police never demand payment over a link or a phone call.", re: /(income tax department|gst department|epfo|epf|trai|uidai|cbi|police|cyber cell|court notice|legal notice|fir\\b)/i },
    { s: 2, name: "Parcel, courier or customs story", why: "A common pretext for a small 'clearance' payment that turns into card theft.", re: /(parcel|courier|customs|shipment|delivery (failed|pending)|india post).{0,60}(fee|pay|clearance|held|customs duty)/i },
    { s: 2, name: "Electricity, gas or water disconnection", why: "Utility disconnections are arranged with the utility, not by a link in a message.", re: /(electricity|power|gas|water).{0,40}(disconnect|disconnection|bill overdue)/i },

    { s: 2, name: "Delivery failure that wants your details", why: "Couriers do not collect address or card details through a link. Check the tracking number on the carrier's own site.", re: /(package|parcel|delivery|courier|shipment).{0,70}(could not be delivered|failed|incomplete address|reschedul|update your (info|details|address)|redelivery)/i },
    { s: 2, name: "Unpaid toll, fine or penalty with a payment link", why: "Toll and traffic penalties are paid on the authority's portal, not through a link that arrives by SMS.", re: /(toll|fine|penalty|unpaid (balance|amount)|late fee|outstanding (balance|amount)|parking (ticket|violation))/i },
    { s: 2, name: "Fake fraud alert asking you to 'verify'", why: "This is the most common card phishing script. A real bank never asks you to verify through a link.", re: /(security alert|suspicious (charge|transaction|activity|login)|unauthori[sz]ed (charge|transaction)|unusual (activity|login)|if this wasn.t you|wasn.t you|reply stop|verify your (account|identity|card))/i },
    { s: 2, name: "Asks you to reply STOP or similar to a link", why: "'Reply STOP' is borrowed from real marketing to make a fake alert look routine.", re: /(reply (stop|yes|no|1)\b|text (stop|yes))\b/i },
    { s: 2, name: "Job offer that arrives unasked", why: "Recruiters do not find you through a random message promising pay per day and a chat app to 'start'.", re: /(found your (resume|cv|profile)|hiring (remote|flexible)|remote workers?|flexible hours|message (us|me) on (whatsapp|telegram)|apply on (whatsapp|telegram)|start (today|immediately))/i },
    { s: 1, name: "Conversation opener from an unknown sender", why: "Wrong-number and 'are you there?' openers are the first step of a longer scam, usually ending in an investment pitch.", re: /(are we still (meeting|on)|can i ask you a (question|something)|is this (a )?(good|right) time|you (up|there)\?|sorry, wrong number)/i },
    { s: 1, name: "Asks you to update your info through a link", why: "Account details are updated inside an app you already have, not on a page sent to you.", re: /(update your (info|information|details|account|records)|confirm your (details|account|payment)|complete your (profile|verification))/i },
    { s: 3, name: "Family emergency from a new number", why: "This is the 'hi mum, new number' scam. The person asking for money is not your relative — call them on the number you already have.", re: /(hi (papa|mummy|mom|dad|amma|appa)|this is my new (number|phone)|new number,? (save|please save)|lost my (phone|wallet)|phone got (stolen|lost)|in an emergency).{0,90}(transfer|send|pay|upi|money|urgent)/i },
    { s: 2, name: "Asks you to return money 'sent by mistake'", why: "The transfer never happened, or came from a stolen account. Returning it makes you the one who lost the money.", re: /(mistakenly|by mistake|wrongly) (sent|transferred)|(sent|transferred).{0,30}(by mistake|instead of my|wrong (number|account|upi))|return the (amount|money)|send (it|the money) back/i },
    { s: 2, name: "Tells you to transfer to a given UPI or account", why: "A message that supplies the account to pay into is directing your money, not receiving it.", re: /(transfer|send|pay|deposit).{0,45}(to this|to the|into this) (upi|account|number|id)|upi id\s*[:\-]|pay to\s*(upi|this)/i },
    { s: 2, name: "Threatens police or legal action over a message", why: "No agency demands payment or threatens arrest by SMS. This is intimidation to stop you thinking.", re: /(face (police|legal) action|police (complaint|case) will be|arrest warrant|legal proceedings will|non[- ]?bailable)/i },
    { s: 2, name: "Asks you to contact an 'officer' or 'agent' directly", why: "Utility and bank staff never give you a personal mobile number to settle a bill.", re: /(contact (our|the) (officer|agent|executive|representative)|call (our|the) (officer|agent))\b/i },
    /* ---- medium: the shape of a mass-sent scam ---- */
    { s: 1, name: "Investment or trading 'guarantee'", why: "No legitimate product guarantees a return. SEBI-registered advisers cannot promise profits either.", re: /(guaranteed (return|profit|income)|assured returns?|double your money|\\d+ ?% (daily|weekly|monthly) return|risk[- ]free (profit|investment)|sure shot)/i },
    { s: 1, name: "Trading tips group or 'mentor'", why: "Groups promising calls, tips or a 'fund manager' on WhatsApp or Telegram are almost always pump-and-dump.", re: /(telegram|whatsapp) (group|channel)|trading (tips|signals)|fund manager|portfolio manager|join (our )?(group|channel)/i },
    { s: 1, name: "Pre-approved loan or instant credit", why: "Real lenders run checks. 'Pre-approved' offers that want a fee first are the scam.", re: /(pre[- ]?approved loan|instant loan|loan approved|credit limit (of|up to)|no (credit )?check|without cibil)/i },
    { s: 2, name: "Unasked job offer with pay per day", why: "Recruiters do not find you through a random message that quotes a daily wage and moves you to a chat app.", re: /(part[- ]?time job|work from home|remote (workers?|job)|found your (resume|cv|profile)|(rs\.?|₹|\$)\s?\d[\d,]*\s?(per|a|\/)\s?(day|week|month)|daily (payout|payment)|simple tasks|like and earn|flexible hours)/i },
    { s: 1, name: "Shortened or unfamiliar link", why: "Short links hide the destination, so you cannot see where you are being sent.", re: /(bit\\.ly|tinyurl|t\\.co|is\\.gd|rebrand\\.ly|cutt\\.ly|shorturl|[a-z0-9-]+\\.(xyz|top|club|online|site|live|click|shop)\\b)/i },
    { s: 1, name: "Asks you to contact an unknown number", why: "The number in the message is the scammer's, however official it looks.", re: /(call (us )?(on|at)|contact (us )?(on|at)|whatsapp (us|me) (on|at)|reply (with )?\\+?91[\\s-]?\\d{5})/i },
    { s: 1, name: "Mass-mail opening", why: "Official letters carry your name and account reference, not 'Dear customer'.", re: /(dear (customer|user|sir\\/madam|valued customer)|kindly (do|update|verify|note)|this is to inform you)/i },
    { s: 1, name: "Asks you to send documents on WhatsApp", why: "KYC documents sent on chat can be used to open accounts in your name.", re: /(send|share|upload).{0,30}(aadha[ae]r|pan|photo|selfie|document).{0,30}(whatsapp|chat|reply)/i },

    /* ---- weak signals, still worth surfacing in combination ---- */
    { s: 1, name: "Sense of secrecy or a 'special' offer", why: "Legitimate offers do not ask you to keep quiet or act before others.", re: /(do not (tell|share)|keep (this )?(confidential|secret)|only for (you|selected)|special (offer|price) for you)/i },
    { s: 1, name: "Unusual capitalisation", why: "Copied templates and evasion tricks produce text that reads oddly.", re: /(URGENT!|FINAL NOTICE|IMPORTANT!!|\\b[A-Z]{6,}\\b)/ },
    { s: 1, name: "Rupee amounts attached to a link", why: "A figure plus a link is the classic 'pay here' structure.", re: /(rs\\.?\\s?\\d+|₹\\s?\\d+).{0,40}(https?:\\/\\/|www\\.|click|link)/i },
    { s: 1, name: "Your details already 'confirmed'", why: "Scams state your details as settled so you stop checking and just click.", re: /(your (details|information|account) (has|have) been (verified|updated|confirmed)|we have (received|noted) your)/i }
  ];

  function esc(text) {
    return String(text).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function verdict(score, hits) {
    if (!hits.length) {
      return '<div class="checker-verdict is-clear"><strong>Nothing on our list matched.</strong>' +
        "<p>That is not a clean bill of health — it only means this message avoids the patterns we can " +
        "recognise. If it asks for money, documents or a click, verify through the official app or the " +
        "number on your card before doing anything.</p></div>";
    }
    if (score >= 6) {
      return '<div class="checker-verdict is-danger"><strong>High risk — do not act on this.</strong>' +
        "<p>" + hits.length + " patterns matched, weighted " + score +
        " out of the highest severity. Break contact and verify through the official channel.</p></div>";
    }
    if (score >= 3) {
      return '<div class="checker-verdict is-flagged"><strong>Suspicious — treat it as a scam until proven otherwise.</strong>' +
        "<p>" + hits.length + " patterns matched. Nothing legitimate needs you to act this way.</p></div>";
    }
    if (score === 2) {
      return '<div class="checker-verdict is-flagged"><strong>A red flag matched.</strong>' +
        "<p>This pattern on its own is enough to stop. Nothing legitimate asks you to act this way, " +
        "and the next step is always to verify through the official channel.</p></div>";
    }
    return '<div class="checker-verdict is-flagged"><strong>One weak signal matched.</strong>' +
      "<p>On its own this is not proof, but the message is shaped like a mass-sent scam. Verify before acting.</p></div>";
  }

  var TODO = '<div class="checker-todo"><p class="checker-todo-title">What to do</p><ol>' +
    "<li>Do not reply, do not call the number in the message, do not click the link.</li>" +
    "<li>Open your bank's own app, or call the number printed on your card.</li>" +
    "<li>If money has already moved, call 1930 and file at cybercrime.gov.in the same day.</li></ol></div>";

  function render() {
    var text = (input.value || "").trim();
    if (!text) {
      out.innerHTML = '<p class="finder-placeholder">Paste a message to check.</p>';
      return;
    }

    // A bare phone number cannot be checked: there is no public scam-number
    // database in India. Say so instead of implying the number is clean.
    var digits = (text.match(/\d/g) || []).length;
    if (digits >= 8 && digits <= 14 && /^[+\d\s\-()]+$/.test(text)) {
      out.innerHTML = '<div class="checker-verdict is-nonum"><strong>A number cannot be checked here.</strong>' +
        "<p>India has no public register of scam numbers, so no website can tell you whether this one is " +
        "genuine. What you can do:</p></div>" +
        '<div class="checker-todo"><p class="checker-todo-title">What to do</p><ol>' +
        "<li>Do not share OTPs, and never approve a UPI collect request from it.</li>" +
        "<li>Look the number up in your bank's official app or on the company's own website.</li>" +
        "<li>Report it as spam in Truecaller or your phone's dialler, and file it at cybercrime.gov.in if it asked for money.</li></ol></div>" +
        '<p class="calc-fineprint">Nothing you typed was sent to us or stored.</p>';
      return;
    }

    var hits = RULES.filter(function (rule) { return rule.re.test(text); });
    hits.sort(function (a, b) { return b.s - a.s; });
    var score = hits.reduce(function (sum, r) { return sum + r.s; }, 0);

    var list = hits.map(function (rule) {
      var level = rule.s >= 3 ? "critical" : rule.s === 2 ? "high" : "medium";
      return '<li class="is-' + level + '"><strong>' + esc(rule.name) + "</strong><span>" +
        esc(rule.why) + "</span></li>";
    }).join("");

    out.innerHTML = verdict(score, hits) +
      (list ? '<ul class="checker-list">' + list + "</ul>" : "") +
      (hits.length ? TODO : "") +
      '<p class="calc-fineprint">Checked in your browser. Nothing you typed was sent to us or stored. ' +
      "This screen matches patterns; it cannot confirm or deny that a specific sender is genuine.</p>";
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
