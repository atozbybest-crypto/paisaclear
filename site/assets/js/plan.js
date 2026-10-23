/* Emergency-fund and retirement planners. Pure arithmetic on user inputs. */

(function () {
  "use strict";

  var form = document.getElementById("plan-form");
  if (!form) return;

  var out = document.getElementById("plan-output");
  var tabs = Array.prototype.slice.call(document.querySelectorAll("[data-plan-tab]"));
  var mode = "emergency";
  var CATALOG = [];
  try {
    CATALOG = JSON.parse((document.getElementById("plan-catalog") || {}).textContent || "[]");
  } catch (error) { CATALOG = []; }

  function val(id) {
    var el = document.getElementById(id);
    var n = parseFloat(String((el && el.value) || "").replace(/[^0-9.]/g, ""));
    return isNaN(n) ? 0 : n;
  }

  function money(value) {
    var rounded = Math.round(value);
    var text = String(Math.abs(rounded));
    var last3 = text.slice(-3);
    var rest = text.slice(0, -3);
    if (rest) {
      rest = rest.replace(/\B(?=(\d{2})+(?!\d))/g, ",");
      text = rest + "," + last3;
    }
    return (rounded < 0 ? "−₹" : "₹") + text;
  }

  function short(value) {
    if (Math.abs(value) >= 10000000) return "₹" + (value / 10000000).toFixed(2) + " Cr";
    if (Math.abs(value) >= 100000) return "₹" + (value / 100000).toFixed(2) + " L";
    return money(value);
  }

  function row(label, value, note) {
    return '<div class="calc-total-row"><span>' + label + "</span><strong>" + value +
      (note ? ' <small class="calc-row-note">' + note + "</small>" : "") + "</strong></div>";
  }

  function suggestions(amount, noteText) {
    if (!CATALOG.length || amount <= 0) return "";
    var fits = CATALOG.filter(function (p) { return p.m <= amount; });
    if (!fits.length) return "";
    var seen = {}, picks = [];
    fits.forEach(function (p) {
      if (seen[p.c] || picks.length >= 4) return;
      seen[p.c] = true;
      picks.push(p);
    });
    return '<div class="planner-suggest">' +
      "<h3>Products your amount can already reach</h3>" +
      '<p class="planner-suggest-note">' + noteText + "</p>" +
      '<ul class="suggest-list">' +
      picks.map(function (p) {
        return '<li class="suggest-item"><a href="../products/' + p.s + '.html">' + p.n + "</a>" +
          "<span>" + p.p + " · min " + money(p.m) + "</span></li>";
      }).join("") +
      "</ul></div>";
  }

  function requiredMonthly(gap, annualRate, years, currentMonthly) {
    var i = annualRate / 12;
    var n = Math.max(1, Math.round(years * 12));
    var factor = i > 0 ? ((Math.pow(1 + i, n) - 1) / i) * (1 + i) : n;
    return currentMonthly + gap / factor;
  }

  function renderEmergency() {
    var expenses = val("e-expenses");
    var months = val("e-months") || 0;
    var saved = val("e-saved");
    var monthly = val("e-monthly");

    var target = expenses * months;
    var gap = Math.max(0, target - saved);
    var monthsToFill = monthly > 0 ? Math.ceil(gap / monthly) : null;
    var pct = target > 0 ? Math.min(100, (saved / target) * 100) : 0;

    return '<p class="calc-headline-label">Emergency fund target</p>' +
      '<p class="calc-headline-value">' + money(target) + "</p>" +
      '<p class="calc-headline-note">' + months + " months of " + money(expenses) + " a month.</p>" +
      '<div class="bar-track bar-track-lg"><div class="bar-fill" style="width:' + pct.toFixed(1) + '%"></div></div>' +
      '<p class="calc-fineprint">' + pct.toFixed(0) + "% funded.</p>" +
      '<div class="calc-totals">' +
        row("Target", money(target)) +
        row("Already set aside", money(saved)) +
        row("Still to build", money(gap)) +
        row("At " + money(monthly) + " a month", monthsToFill === null ? "—" : monthsToFill + " months", monthsToFill === null ? "set an amount" : "") +
      "</div>" +
      suggestions(saved, "Filtered only by the " + money(saved) + " you already have. This is not a recommendation.") +
      '<p class="calc-fineprint">Emergency money normally needs to be reachable quickly. Check each product\'s ' +
      "access terms on its page before relying on it.</p>";
  }

  function renderRetire() {
    var age = val("r-age");
    var retireAge = val("r-retire");
    var yearsToGo = Math.max(0, retireAge - age);
    var expenses = val("r-expenses");
    var inflation = val("r-inflation") / 100;
    var grow = val("r-grow") / 100;
    var post = val("r-post") / 100;
    var cover = val("r-years");
    var saved = val("r-saved");
    var monthly = val("r-monthly");

    var expensesThen = expenses * Math.pow(1 + inflation, yearsToGo);
    // Present value at retirement of a monthly income rising with inflation.
    var realPost = post - inflation;
    var monthsCovered = cover * 12;
    var corpusNeeded;
    if (Math.abs(realPost) < 0.0001) {
      corpusNeeded = expensesThen * monthsCovered;
    } else {
      var i = realPost / 12;
      corpusNeeded = expensesThen * (1 - Math.pow(1 + i, -monthsCovered)) / i;
    }

    var grown = saved * Math.pow(1 + grow, yearsToGo);
    var monthlyRate = grow / 12;
    var contributions = yearsToGo * 12;
    var sip = monthlyRate > 0
      ? monthly * ((Math.pow(1 + monthlyRate, contributions) - 1) / monthlyRate) * (1 + monthlyRate)
      : monthly * contributions;
    var projected = grown + sip;
    var gap = corpusNeeded - projected;

    var progress = corpusNeeded > 0 ? Math.min(100, (projected / corpusNeeded) * 100) : 0;

    return '<p class="calc-headline-label">Corpus you would need at ' + retireAge + "</p>" +
      '<p class="calc-headline-value">' + short(corpusNeeded) + "</p>" +
      '<p class="calc-headline-note">To cover ' + money(expensesThen) + " a month for " + cover + " years, after inflation.</p>" +
      '<div class="bar-track bar-track-lg"><div class="bar-fill" style="width:' + progress.toFixed(1) + '%"></div></div>' +
      '<p class="calc-fineprint">On your numbers you are projected to reach ' + progress.toFixed(0) + "% of it.</p>" +
      '<div class="calc-totals">' +
        row("Monthly expenses at " + retireAge, money(expensesThen)) +
        row("Corpus needed", money(corpusNeeded)) +
        row("Projected from savings", money(projected), "at " + (grow * 100).toFixed(1) + "%") +
        row(gap > 0 ? "Shortfall" : "Surplus", money(Math.abs(gap)), gap > 0 ? "" : "on these assumptions") +
      "</div>" +
      (gap > 0
        ? '<p class="calc-verdict">To close the gap on the same assumptions you would need about ' +
          money(requiredMonthly(gap, grow, yearsToGo, monthly)) + " a month, or work longer, or plan for less."
        : '<p class="calc-verdict">On these assumptions the corpus is covered. Change a figure to see how fragile that is.</p>') +
      suggestions(monthly, "Products whose minimum is within the " + money(monthly) + " a month you invest. Not a recommendation.") +
      '<p class="calc-fineprint">A constant return is assumed. Real markets do not deliver one.</p>';
  }

  function render() {
    if (mode === "emergency" && (val("e-expenses") <= 0 || val("e-months") <= 0)) {
      out.innerHTML = '<p class="calc-empty-text">Enter your monthly expenses and how many months of cover you want.</p>';
      return;
    }
    if (mode === "retire" && (val("r-age") <= 0 || val("r-retire") <= 0 || val("r-expenses") <= 0)) {
      out.innerHTML = '<p class="calc-empty-text">Enter your age, the age you want to stop, and your monthly expenses.</p>';
      return;
    }
    out.innerHTML = mode === "emergency" ? renderEmergency() : renderRetire();
  }

  function setMode(next) {
    mode = next;
    tabs.forEach(function (tab) {
      var on = tab.getAttribute("data-plan-tab") === next;
      tab.classList.toggle("is-on", on);
      tab.setAttribute("aria-pressed", String(on));
    });
    Array.prototype.forEach.call(document.querySelectorAll("[data-only]"), function (block) {
      block.hidden = block.getAttribute("data-only") !== next;
    });
    render();
  }

  tabs.forEach(function (tab) {
    tab.addEventListener("click", function () { setMode(tab.getAttribute("data-plan-tab")); });
  });
  form.addEventListener("submit", function (event) { event.preventDefault(); render(); });
  form.addEventListener("input", render);
  form.addEventListener("change", render);

  setMode("emergency");
})();
