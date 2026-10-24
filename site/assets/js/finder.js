/* Smart Scheme Finder. Filters the catalogue; never recommends. */

(function () {
  "use strict";

  var form = document.getElementById("finder-form");
  if (!form) return;

  var CATALOG = [];
  try {
    CATALOG = JSON.parse(document.getElementById("finder-catalog").textContent || "[]");
  } catch (e) { CATALOG = []; }

  var out = document.getElementById("finder-results");

  function val(id) { var el = document.getElementById(id); return el ? el.value : ""; }
  function num(id) {
    var n = parseFloat(String(val(id)).replace(/[^0-9.]/g, ""));
    return isNaN(n) ? 0 : n;
  }
  function money(v) {
    var t = String(Math.round(v)), last3 = t.slice(-3), rest = t.slice(0, -3);
    if (rest) { rest = rest.replace(/\B(?=(\d{2})+(?!\d))/g, ","); t = rest + "," + last3; }
    return "₹" + t;
  }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function yearsIn(tenure) {
    var m = String(tenure || "").match(/(\d+)\s*(year|month)/i);
    if (!m) return null;
    return m[2].toLowerCase() === "month" ? Number(m[1]) / 12 : Number(m[1]);
  }

  function evaluate(p, q) {
    var reasons = [];
    var ok = true;

    // amount
    if (q.amount > 0 && p.m !== null && p.m > q.amount) return null;
    if (p.m !== null) reasons.push("Minimum " + money(p.m));
    else reasons.push("Premium varies by age and term");

    // lock-in
    var yrs = yearsIn(p.t);
    if (q.lock === "none" && p.k) return null;
    if (q.lock === "short" && p.k && yrs !== null && yrs > 1) return null;
    if (q.lock === "mid" && p.k && yrs !== null && yrs > 5) return null;
    if (!p.k) reasons.push("No lock-in");
    else if (yrs !== null) reasons.push("Locked for about " + (yrs < 1 ? Math.round(yrs * 12) + " months" : Math.round(yrs) + " years"));

    // risk
    if (q.risk === "none") {
      if (p.r !== "guaranteed" || p.l !== "low") return null;
      reasons.push("Guaranteed, low risk");
    } else if (q.risk === "some") {
      if (p.r === "market-linked" && p.l !== "low" && p.l !== "moderate") return null;
      reasons.push(p.r === "market-linked" ? "Market-linked, moderate risk" : "Promised return");
    } else {
      if (p.r === "market-linked") reasons.push("Market-linked");
    }

    // goal
    if (q.goal === "income") {
      if (!(p.y === "monthly" || p.y === "quarterly" || p.y === "half-yearly" || p.o.indexOf("monthly-income") !== -1)) return null;
      reasons.push("Pays " + (p.y || "regularly"));
    } else if (q.goal === "grow") {
      if (!(p.c === "mutual-funds" || p.c === "etfs" || p.r === "market-linked")) return null;
      reasons.push("Built for growth");
    } else if (q.goal === "tax") {
      if (p.o.indexOf("tax-saving") === -1) return null;
      reasons.push("Tax benefit");
    } else if (q.goal === "safe") {
      if (!(p.r === "guaranteed" && p.l === "low")) return null;
      reasons.push("Safe and reachable");
    } else if (q.goal === "child") {
      var name = p.n.toLowerCase();
      if (!(name.indexOf("sukanya") !== -1 || name.indexOf("provident") !== -1 || p.o.indexOf("start-small") !== -1)) return null;
      reasons.push("Suits long-term goals");
    }

    // tax
    if (q.tax === "yes" && p.o.indexOf("tax-saving") === -1) return null;
    if (q.tax === "yes") reasons.push("Counts for 80C");

    var score = 0;
    if (p.r === "guaranteed") score += 2;
    if (q.goal === "income" && p.y) score += 3;
    if (q.goal === "income" && p.o.indexOf("monthly-income") !== -1) score += 4;
    if (q.goal === "grow" && (p.c === "mutual-funds" || p.c === "etfs")) score += 3;
    if (p.o.indexOf("tax-saving") !== -1) score += 1;
    if (!p.k) score += 1;

    return { product: p, reasons: reasons, score: score, ok: ok };
  }

  function card(r) {
    var p = r.product;
    return '<article class="finder-card">' +
      '<a class="finder-card-name" href="../products/' + p.s + '.html">' + esc(p.n) + "</a>" +
      '<p class="finder-card-provider">' + esc(p.p) + "</p>" +
      '<ul class="finder-reasons">' +
      r.reasons.slice(0, 4).map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") +
      "</ul>" +
      '<p class="finder-card-meta">' + esc(p.t || "Open-ended") + " · " + esc(p.y || "at maturity") + "</p>" +
      "</article>";
  }

  function render() {
    var q = {
      goal: val("f-goal"),
      amount: num("f-amount"),
      lock: val("f-lock"),
      risk: val("f-risk"),
      tax: val("f-tax"),
    };

    var matches = [];
    CATALOG.forEach(function (p) {
      var r = evaluate(p, q);
      if (r) matches.push(r);
    });

    matches.sort(function (a, b) {
      if (b.score !== a.score) return b.score - a.score;
      var am = a.product.m === null ? Infinity : a.product.m;
      var bm = b.product.m === null ? Infinity : b.product.m;
      return am - bm;
    });

    var top = matches.slice(0, 12);

    var summary = '<div class="finder-summary"><p><strong>' + matches.length +
      "</strong> products match those filters" +
      (matches.length > top.length ? ", showing the 12 closest" : "") + ".</p></div>";

    if (!matches.length) {
      out.innerHTML = summary +
        '<div class="finder-empty"><p>Nothing matches all five answers. Try loosening one — the lock-in or the risk question usually opens it up.</p>' +
        '<p class="muted">Or <a href="../browse.html">browse the full catalogue</a>.</p></div>';
      return;
    }

    out.innerHTML = summary + '<div class="finder-grid">' + top.map(card).join("") + "</div>" +
      '<p class="calc-fineprint">These are filters, not recommendations. A product appearing here only means its ' +
      "stated terms match your answers — not that it suits your circumstances.</p>";
  }

  form.addEventListener("submit", function (e) { e.preventDefault(); render(); });
  var reset = document.getElementById("finder-reset");
  if (reset) reset.addEventListener("click", function () {
    window.setTimeout(function () {
      out.innerHTML = '<p class="finder-placeholder">Answer the five questions and press the button.</p>';
    }, 0);
  });
})();
