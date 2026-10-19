/* Salary / take-home calculator.
   All tax constants come from content/tax-rules.json, embedded in the page. */

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
      ctc: ctc,
      basic: basic,
      hra: hra,
      employerPf: employerPf,
      gross: gross,
      employeePf: employeePf,
      pt: pt,
      hraExempt: hraExempt,
      regimes: regimes
    };
  }

  function row(label, value, note) {
    return '<div class="calc-row"><span>' + label + "</span><span>" + value +
      (note ? ' <small class="calc-row-note">' + note + "</small>" : "") + "</span></div>";
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
    var monthly = best.homeTake / 12;

    out.innerHTML =
      '<div class="calc-headline">' +
        '<p class="calc-headline-label">Monthly take-home · ' + best.label + "</p>" +
        '<p class="calc-headline-value">' + money(monthly) + "</p>" +
        '<p class="calc-headline-note">' + money(best.homeTake) + " a year, after tax, PF and professional tax</p>" +
      "</div>" +

      '<div class="calc-compare">' +
        '<div class="calc-compare-card' + (better === "new" ? " is-best" : "") + '">' +
          "<span>" + newer.label + "</span>" +
          '<strong>' + money(newer.homeTake) + "</strong>" +
          '<small>tax ' + moneyShort(newer.tax.total) + "</small>" +
        "</div>" +
        '<div class="calc-compare-card' + (better === "old" ? " is-best" : "") + '">' +
          "<span>" + older.label + "</span>" +
          '<strong>' + money(older.homeTake) + "</strong>" +
          '<small>tax ' + moneyShort(older.tax.total) + "</small>" +
        "</div>" +
      "</div>" +

      '<p class="calc-verdict">' +
        (difference < 1
          ? "Both regimes come out the same on this salary."
          : best.label + " leaves you " + money(difference) + " better off a year.") +
      "</p>" +

      '<div class="calc-breakdown">' +
        '<h3>How it adds up</h3>' +
        row("Annual CTC", money(result.ctc)) +
        row("Employer PF", money(result.employerPf), "not paid to you") +
        row("Gross salary", money(result.gross)) +
        row("Basic", money(result.basic)) +
        row("Your PF contribution", money(result.employeePf), "goes to your PF account") +
        row("Professional tax", money(result.pt)) +
        (result.hraExempt > 0 ? row("HRA exempt (old regime)", money(result.hraExempt)) : "") +
        row("Taxable income · new", money(newer.taxable)) +
        row("Tax · new", money(newer.tax.total), "incl. " + money(newer.tax.cess) + " cess") +
        row("Taxable income · old", money(older.taxable)) +
        row("Tax · old", money(older.tax.total), "incl. " + money(older.tax.cess) + " cess") +
      "</div>" +

      '<p class="calc-fineprint">Estimate for FY ' + RULES.financialYear +
      ". Ignores marginal relief, gratuity, LTA, employer NPS and non-salary income. Rules as of " +
      RULES.asOf + ".</p>";
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
