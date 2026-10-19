/* Salary / take-home calculator.
   Tax constants come from content/tax-rules.json, embedded in the page. */

(function () {
  "use strict";

  var dataEl = document.getElementById("tax-rules");
  var form = document.getElementById("salary-form");
  if (!dataEl || !form) return;

  var RULES;
  try {
    RULES = JSON.parse(dataEl.textContent);
  } catch (error) {
    return;
  }

  var out = document.getElementById("calc-output");
  var empty = document.getElementById("calc-empty");
  var mode = "year"; // "year" | "month"

  var COLOURS = {
    basic: "var(--green)",
    hra: "var(--amber)",
    other: "var(--violet)",
    employerPf: "var(--blue)",
    deductions: "var(--rose)",
  };

  function num(id) {
    var el = document.getElementById("calc-" + id);
    if (!el) return 0;
    var value = parseFloat(String(el.value).replace(/[^0-9.]/g, ""));
    return isNaN(value) ? 0 : value;
  }

  function checked(id) {
    var el = document.getElementById("calc-" + id);
    return Boolean(el && el.checked);
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
    return (rounded < 0 ? "-₹" : "₹") + text;
  }

  function moneyShort(value) {
    if (Math.abs(value) >= 10000000) return "₹" + (value / 10000000).toFixed(2) + " Cr";
    if (Math.abs(value) >= 100000) return "₹" + (value / 100000).toFixed(2) + " L";
    return money(value);
  }

  function shown(value) {
    return mode === "month" ? value / 12 : value;
  }

  function taxFor(regime, taxable) {
    var tax = 0;
    var previous = 0;

    regime.slabs.forEach(function (slab) {
      var ceiling = slab.upTo === null ? Infinity : slab.upTo;
      if (taxable > previous) {
        var slice = Math.min(taxable, ceiling) - previous;
        if (slice > 0) tax += slice * slab.rate;
      }
      previous = ceiling;
    });

    var rebate = 0;
    if (taxable <= regime.rebate.taxableLimit) {
      rebate = Math.min(tax, regime.rebate.maxRebate);
      tax -= rebate;
    }

    var surcharge = 0;
    regime.surcharge.forEach(function (step) {
      if (taxable > step.above) surcharge = Math.max(surcharge, tax * step.rate);
    });

    var cess = (tax + surcharge) * RULES.cess;
    return { base: tax, rebate: rebate, surcharge: surcharge, cess: cess, total: tax + surcharge + cess };
  }

  function compute() {
    var ctc = num("ctc");
    if (ctc <= 0) return null;

    var basic = ctc * (num("basic") / 100);
    var hra = basic * (num("hra") / 100);
    var employerPf = checked("pf-in-ctc") ? basic * RULES.epfRate : 0;
    var gross = Math.max(0, ctc - employerPf);
    var employeePf = basic * RULES.epfRate;
    var pt = num("pt");
    var otherAllowances = Math.max(0, gross - basic - hra);
    var metro = checked("metro");

    var hraExempt = 0;
    var rent = num("rent") * 12;
    if (rent > 0) {
      hraExempt = Math.max(0, Math.min(
        hra,
        rent - RULES.limits.hraBasicShare * basic,
        (metro ? RULES.limits.hraMetro : RULES.limits.hraNonMetro) * basic
      ));
    }

    var c80c = Math.min(RULES.limits.sec80c, num("sec80c") + employeePf);
    var c80d = Math.min(RULES.limits.sec80d, num("sec80d"));
    var home = Math.min(RULES.limits.homeLoanInterest, num("home"));

    var regimes = {};
    Object.keys(RULES.regimes).forEach(function (key) {
      var regime = RULES.regimes[key];
      var deductions = regime.standardDeduction;
      if (regime.professionalTaxAllowed) deductions += pt;
      if (key === "old") deductions += hraExempt + c80c + c80d + home;

      var taxable = Math.max(0, gross - deductions);
      var tax = taxFor(regime, taxable);
      regimes[key] = {
        label: regime.label,
        deductions: deductions,
        taxable: taxable,
        tax: tax,
        homeTake: gross - employeePf - pt - tax.total
      };
    });

    return {
      ctc: ctc, basic: basic, hra: hra, otherAllowances: otherAllowances,
      employerPf: employerPf, gross: gross, employeePf: employeePf, pt: pt,
      deductions: employeePf + pt, hraExempt: hraExempt, regimes: regimes
    };
  }

  function donut(segments, total) {
    var stops = [];
    var cursor = 0;
    segments.forEach(function (segment) {
      var share = total > 0 ? (segment.value / total) * 100 : 0;
      if (share <= 0) return;
      var end = Math.min(100, cursor + share);
      stops.push(segment.colour + " " + cursor.toFixed(2) + "% " + end.toFixed(2) + "%");
      cursor = end;
    });
    if (!stops.length) stops = ["var(--line) 0% 100%"];
    return '<div class="donut" style="background: conic-gradient(' + stops.join(", ") + ')">' +
      '<div class="donut-hole"><span>' + moneyShort(total) + "</span><small>CTC</small></div></div>";
  }

  function line(label, value, colour, note) {
    return '<li class="calc-line">' +
      (colour ? '<span class="calc-dot" style="background:' + colour + '"></span>' : '<span class="calc-dot is-blank"></span>') +
      '<span class="calc-line-label">' + label + "</span>" +
      '<span class="calc-line-value">' + money(shown(value)) +
      (note ? ' <small>' + note + "</small>" : "") + "</span></li>";
  }

  function render(result) {
    if (!result) {
      out.hidden = true;
      empty.hidden = false;
      return;
    }
    empty.hidden = true;
    out.hidden = false;

    var newer = result.regimes.new;
    var older = result.regimes.old;
    var better = newer.homeTake >= older.homeTake ? "new" : "old";
    var best = result.regimes[better];
    var difference = Math.abs(newer.homeTake - older.homeTake);

    var segments = [
      { label: "Basic salary", value: result.basic, colour: COLOURS.basic },
      { label: "HRA", value: result.hra, colour: COLOURS.hra },
      { label: "Other allowances", value: result.otherAllowances, colour: COLOURS.other },
      { label: "Employer PF", value: result.employerPf, colour: COLOURS.employerPf },
    ];

    out.innerHTML =
      '<div class="calc-toolbar">' +
        '<span class="calc-toolbar-label">Show</span>' +
        '<div class="seg-toggle" role="group" aria-label="Yearly or monthly">' +
          '<button type="button" data-mode="year" class="' + (mode === "year" ? "is-on" : "") + '">Yearly</button>' +
          '<button type="button" data-mode="month" class="' + (mode === "month" ? "is-on" : "") + '">Monthly</button>' +
        "</div>" +
      "</div>" +

      '<div class="calc-visual">' +
        donut(segments, result.ctc) +
        '<ul class="calc-lines">' +
          line("Basic salary", result.basic, COLOURS.basic) +
          line("HRA", result.hra, COLOURS.hra) +
          line("Other allowances", result.otherAllowances, COLOURS.other) +
          (result.employerPf > 0 ? line("Employer PF", result.employerPf, COLOURS.employerPf, "in CTC") : "") +
        "</ul>" +
      "</div>" +

      '<div class="calc-totals">' +
        '<div class="calc-total-row"><span>Gross salary</span><strong>' + money(shown(result.gross)) + "</strong></div>" +
        '<div class="calc-total-row"><span>Your PF and professional tax</span><strong>− ' + money(shown(result.deductions)) + "</strong></div>" +
        '<div class="calc-total-row is-sub"><span>Net salary</span><strong>' + money(shown(result.gross - result.deductions)) + "</strong></div>" +
        '<div class="calc-total-row"><span>Income tax · ' + best.label + " " + (mode === "month" ? "/ month" : "/ year") + "</span><strong>− " +
          money(shown(best.tax.total)) + "</strong></div>" +
        '<div class="calc-total-row is-grand"><span>Take-home</span><strong>' + money(shown(best.homeTake)) + "</strong></div>" +
      "</div>" +

      '<div class="calc-compare">' +
        '<div class="calc-compare-card' + (better === "new" ? " is-best" : "") + '">' +
          "<span>" + newer.label + "</span>" +
          "<strong>" + money(shown(newer.homeTake)) + "</strong>" +
          "<small>tax " + money(shown(newer.tax.total)) + "</small>" +
        "</div>" +
        '<div class="calc-compare-card' + (better === "old" ? " is-best" : "") + '">' +
          "<span>" + older.label + "</span>" +
          "<strong>" + money(shown(older.homeTake)) + "</strong>" +
          "<small>tax " + money(shown(older.tax.total)) + "</small>" +
        "</div>" +
      "</div>" +

      '<p class="calc-verdict">' +
        (difference < 1
          ? "Both regimes come out the same on this salary."
          : best.label + " leaves you " + money(difference) + " better off a year.") +
      "</p>" +

      '<details class="calc-details">' +
        "<summary>Full breakdown</summary>" +
        '<div class="calc-breakdown">' +
          '<div class="calc-row"><span>Annual CTC</span><span>' + money(result.ctc) + "</span></div>" +
          '<div class="calc-row"><span>Employer PF</span><span>' + money(result.employerPf) + " <small class=\"calc-row-note\">not paid to you</small></span></div>" +
          '<div class="calc-row"><span>Gross salary</span><span>' + money(result.gross) + "</span></div>" +
          '<div class="calc-row"><span>Your PF contribution</span><span>' + money(result.employeePf) + "</span></div>" +
          '<div class="calc-row"><span>Professional tax</span><span>' + money(result.pt) + "</span></div>" +
          (result.hraExempt > 0 ? '<div class="calc-row"><span>HRA exempt (old regime)</span><span>' + money(result.hraExempt) + "</span></div>" : "") +
          '<div class="calc-row"><span>Taxable income · new</span><span>' + money(newer.taxable) + "</span></div>" +
          '<div class="calc-row"><span>Tax · new</span><span>' + money(newer.tax.total) + '</span></div>' +
          '<div class="calc-row"><span>Taxable income · old</span><span>' + money(older.taxable) + "</span></div>" +
          '<div class="calc-row"><span>Tax · old</span><span>' + money(older.tax.total) + "</span></div>" +
        "</div>" +
      "</details>" +

      '<p class="calc-fineprint">Estimate for FY ' + RULES.financialYear +
      ". Ignores marginal relief, gratuity, LTA, employer NPS and non-salary income. Rules as of " +
      RULES.asOf + ".</p>";

    Array.prototype.forEach.call(out.querySelectorAll("[data-mode]"), function (button) {
      button.addEventListener("click", function () {
        mode = button.getAttribute("data-mode");
        render(compute());
      });
    });
  }

  function run(event) {
    if (event) event.preventDefault();
    render(compute());
  }

  form.addEventListener("submit", run);
  form.addEventListener("input", run);
  form.addEventListener("change", run);

  var reset = document.getElementById("calc-reset");
  if (reset) {
    reset.addEventListener("click", function () {
      window.setTimeout(run, 0);
    });
  }

  run();
})();
