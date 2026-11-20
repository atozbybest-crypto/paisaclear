/* AskPaisa — retrieval assistant over the site's own index.
   No model, no network: it scores the query against content/askpaisa.json. */

(function () {
  "use strict";

  var root = document.getElementById("askpaisa");
  if (!root) return;

  var base = root.getAttribute("data-base") || "";
  var open = false;
  var loaded = false;
  var index = [];
  var el = {};
  var usHint = null;

  var SUGGESTIONS = [
    "Sukanya Samriddhi rules",
    "PPF vs FD",
    "senior citizen scheme",
    "best tax saving fund",
    "is this message a scam",
    "US index funds"
  ];

  var STOP = ["open", "show", "me", "about", "the", "a", "an", "of", "for", "what", "is",
              "tell", "please", "can", "you", "give", "details", "info", "information",
              "page", "link", "go", "to", "and", "how", "does", "work", "works", "in", "on"];

  function esc(t) {
    return String(t).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  var SHORT = ["us", "usa", "fd", "sip", "elss", "nsc", "kvp", "scss", "sbi"];

  function tokens(q) {
    return q.toLowerCase().replace(/[^a-z0-9\s]/g, " ").split(/\s+/)
      .filter(function (t) {
        if (STOP.indexOf(t) !== -1) return false;
        return t.length > 2 || SHORT.indexOf(t) !== -1;
      });
  }

  function wantsUS(q) {
    return /\b(us|usa|america|american|s&p|sp500|nasdaq|dow|wall street)\b/i.test(q);
  }

  function score(entry, q, toks) {
    var title = entry.t.toLowerCase();
    var words = (entry.w || "").toLowerCase();
    var summary = (entry.s || "").toLowerCase();
    var s = 0;
    if (title.indexOf(q) !== -1) s += 40;
    toks.forEach(function (t) {
      if (title.indexOf(t) !== -1) s += 8;
      if (words.indexOf(t) !== -1) s += 4;
      if (summary.indexOf(t) !== -1) s += 1;
    });
    // every token should appear somewhere for a confident answer
    var hit = toks.filter(function (t) {
      return title.indexOf(t) !== -1 || words.indexOf(t) !== -1 || summary.indexOf(t) !== -1;
    }).length;
    if (toks.length && hit === toks.length) s += 6;
    if (q && usHint !== null) {
      var isUS = entry.u.indexOf("us-") === 0;
      s += usHint ? (isUS ? 30 : -10) : (isUS ? -6 : 0);
    }
    return s;
  }

  function search(q) {
    var toks = tokens(q);
    if (!toks.length) return [];
    var ql = q.toLowerCase().trim();
    usHint = wantsUS(q);
    return index
      .map(function (e) { return { e: e, s: score(e, ql, toks) }; })
      .filter(function (r) { return r.s > 0; })
      .sort(function (a, b) { return b.s - a.s || a.e.t.length - b.e.t.length; })
      .slice(0, 4)
      .map(function (r) { return r.e; });
  }

  function bubble(text, who) {
    var div = document.createElement("div");
    div.className = "ap-msg is-" + who;
    div.innerHTML = text;
    el.log.appendChild(div);
    el.log.scrollTop = el.log.scrollHeight;
  }

  function answer(q) {
    bubble(esc(q), "you");
    var results = search(q);
    if (!results.length) {
      bubble("That is not covered on PaisaClear yet — and I only answer from what is on this site. " +
        "Try <a href='" + base + "browse.html'>all products</a>, the " +
        "<a href='" + base + "rates.html'>rates page</a>, or " +
        "<a href='" + base + "rates.html'>" + "ask a different way</a>.", "bot");
      return;
    }
    var top = results[0];
    var html = "<strong>" + esc(top.t) + "</strong><span class='ap-kind'>" + esc(top.k) + "</span>";
    if (top.s) html += "<p>" + esc(top.s) + "</p>";
    html += "<a class='ap-open' href='" + base + esc(top.u) + "'>Open " + esc(top.t) + " →</a>";
    if (results.length > 1) {
      html += "<div class='ap-more'><span>Also on the site</span>";
      results.slice(1).forEach(function (r) {
        html += "<a href='" + base + esc(r.u) + "'>" + esc(r.t) + "</a>";
      });
      html += "</div>";
    }
    bubble(html, "bot");
  }

  function load(cb) {
    if (loaded) return cb();
    fetch(base + "assets/data/askpaisa.json")
      .then(function (r) { return r.json(); })
      .then(function (data) { index = data; loaded = true; cb(); })
      .catch(function () {
        bubble("The index could not load. Try <a href='" + base + "browse.html'>all products</a>.", "bot");
      });
  }

  function toggle(force) {
    open = force === undefined ? !open : force;
    root.classList.toggle("is-open", open);
    el.panel.setAttribute("aria-hidden", open ? "false" : "true");
    if (open) {
      load(function () {
        if (!el.log.dataset.greeted) {
          el.log.dataset.greeted = "1";
          bubble("Ask me about any product, scheme or page on PaisaClear. I answer only from this site.", "bot");
          var chips = document.createElement("div");
          chips.className = "ap-chips";
          SUGGESTIONS.forEach(function (s) {
            var b = document.createElement("button");
            b.type = "button";
            b.className = "ap-chip";
            b.textContent = s;
            b.addEventListener("click", function () { el.input.value = s; answer(s); el.input.value = ""; });
            chips.appendChild(b);
          });
          el.log.appendChild(chips);
        }
        el.input.focus();
      });
    }
  }

  function init() {
    el.panel = document.getElementById("ap-panel");
    el.log = document.getElementById("ap-log");
    el.input = document.getElementById("ap-input");
    el.form = document.getElementById("ap-form");
    el.button = document.getElementById("ap-launch");
    el.close = document.getElementById("ap-close");
    if (!el.panel) return;

    el.button.addEventListener("click", function () { toggle(); });
    el.close.addEventListener("click", function () { toggle(false); });
    el.form.addEventListener("submit", function (e) {
      e.preventDefault();
      var q = el.input.value.trim();
      if (!q) return;
      load(function () { answer(q); el.input.value = ""; });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && open) toggle(false);
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
