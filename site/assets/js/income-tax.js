/* Income-tax calculator. Rules come from content/tax-rules.json. */

(function () {
  "use strict";

  var form = document.getElementById("it-form");
  if (!form) return;

  var RULES = {};
  try {
    RULES = JSON.parse(document.getElementById("it-rules").textContent || "{}");
  } catch (error) { RULES = {}; }

  var out = document.getElementById("it-output");

  function el(id) { return document.getElementById(id); }
  function val(id) { return el(id) ? el(id).value : ""; }
  function num(id) {
    var n = parseFloat(String(val(id)).replace(/[^0-9.]/g, ""));
    return isNaN(n) ? 0 : n;
  }

  function money(v) {
    var r = Math.round(v);
    var t = String(Math.abs(r)), last3 = t.slice(-3), rest = t.slice(0, -3);
    if (rest) { rest = rest.replace(/\B(?=(\d{2})+(?!\d))/g, ","); t = rest + "," + last3; }
    return (r < 0 ? "−₹" : "₹") + t;
  }

  function slabTax(slabs, income) {
    var tax = 0, previous = 0;
    slabs.forEach(function (s) {
      var ceiling = s.upTo === null ? Infinity : s.upTo;
      if (income > previous) {
        var slice = Math.min(income, ceiling) - previous;
        if (slice > 0) tax += slice * s.rate;
      }
      previous = ceiling;
    });
    return tax;
  }

  function surchargeFor(steps, income, tax) {
    var sur = 0;
    (steps || []).forEach(function (s) {
      if (income > s.above) sur = Math.max(sur, tax * s.rate);
    });
    return sur;
  }

  function compute() {
    var entity = val("it-entity");
    var income = num("it-income");
    var age = val("it-age");
    var status = val("it-status");
    var regimeKey = val("it-regime");
    var cess = RULES.cess || 0.04;

    var grossTax = 0, rebate = 0, surcharge = 0, note = "";

    if (entity === "individual" || entity === "huf") {
      var regime = RULES.regimes[regimeKey];
      var slabs = regime.slabs;
      if (regimeKey === "old" && entity === "individual") {
        var exempt = RULES.ageExemptionOld[age];
        // rebuild the old slabs around the age-based exemption
        slabs = [{ upTo: exempt, rate: 0 }];
        if (exempt < 500000) slabs.push({ upTo: 500000, rate: 0.05 });
        slabs.push({ upTo: 1000000, rate: 0.20 });
        slabs.push({ upTo: null, rate: 0.30 });
      }
      grossTax = slabTax(slabs, income);

      var resident = status === "resident";
      if (resident && income <= regime.rebate.taxableLimit) {
        rebate = Math.min(grossTax, regime.rebate.maxRebate);
      }
      surcharge = surchargeFor(regime.surcharge, income, Math.max(0, grossTax - rebate));
      note = regime.label;
    } else if (entity === "firm" || entity === "local") {
      var rule = RULES.entities[entity];
      grossTax = income * rule.rate;
      surcharge = surchargeFor(rule.surcharge, income, grossTax);
      note = rule.label + " — flat " + (rule.rate * 100).toFixed(0) + "%";
    } else {
      var rule2 = RULES.entities.company;
      var small = val("it-turnover") === "small";
      var rate = small ? rule2.rate_small : rule2.rate;
      grossTax = income * rate;
      surcharge = surchargeFor(rule2.surcharge, income, grossTax);
      note = "Domestic company — " + (rate * 100).toFixed(0) + "%" + (small ? " (turnover up to ₹400 cr)" : "");
    }

    var afterRebate = Math.max(0, grossTax - rebate);
    var cessAmount = (afterRebate + surcharge) * cess;
    var total = afterRebate + surcharge + cessAmount;

    return {
      grossTax: grossTax, rebate: rebate, afterRebate: afterRebate,
      surcharge: surcharge, cess: cessAmount, total: total,
      effective: income > 0 ? (total / income) * 100 : 0,
      income: income, note: note,
    };
  }

  function card(label, value) {
    return '<div class="it-card"><p class="it-card-label">' + label + '</p>' +
      '<p class="it-card-value">' + value + "</p></div>";
  }

  function render() {
    var r = compute();
    if (r.income <= 0) {
      out.innerHTML = '<p class="calc-empty-text">Enter a taxable income to calculate.</p>';
      return;
    }
    out.innerHTML =
      card("Income tax", money(r.grossTax)) +
      card("Rebate under section 156", money(r.rebate)) +
      card("Income tax after rebate", money(r.afterRebate)) +
      card("Surcharge", money(r.surcharge)) +
      card("Health and education cess (4%)", money(r.cess)) +
      card("Total tax liability", money(r.total)) +
      '<p class="it-verdict">' + r.note + " · effective rate " + r.effective.toFixed(2) +
      "% of ₹" + Math.round(r.income).toLocaleString("en-IN") + ".</p>" +
      '<p class="calc-fineprint">Marginal relief on surcharge is not applied. Verify at the Income Tax ' +
      "Department before relying on this figure.</p>";
  }

  function syncRows() {
    var entity = val("it-entity");
    var person = entity === "individual" || entity === "huf";
    el("row-age").hidden = entity !== "individual";
    el("row-status").hidden = !person;
    el("row-regime").hidden = !person;
    el("row-turnover").hidden = entity !== "company";
  }

  form.addEventListener("submit", function (e) { e.preventDefault(); render(); });
  form.addEventListener("input", function () { syncRows(); render(); });
  form.addEventListener("change", function () { syncRows(); render(); });
  var reset = document.getElementById("it-reset");
  if (reset) reset.addEventListener("click", function () { window.setTimeout(function () { syncRows(); render(); }, 0); });

  syncRows();
  render();
})();
