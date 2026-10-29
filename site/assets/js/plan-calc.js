/* Calculator shared by the scheme guides.
   config.type: "recurring" (yearly deposits) | "lumpsum" | "payout". */

(function () {
  "use strict";

  var form = document.getElementById("plan-form");
  if (!form) return;

  var cfg = { type: "lumpsum", periods: 12, term: 5 };
  try {
    cfg = JSON.parse(document.getElementById("plan-config").textContent || "{}");
  } catch (e) { /* defaults */ }

  var out = document.getElementById("plan-output");

  function num(id) {
    var el = document.getElementById(id);
    var n = parseFloat(String((el && el.value) || "").replace(/[^0-9.]/g, ""));
    return isNaN(n) ? 0 : n;
  }

  function money(v) {
    var t = String(Math.round(v)), last3 = t.slice(-3), rest = t.slice(0, -3);
    if (rest) { rest = rest.replace(/\B(?=(\d{2})+(?!\d))/g, ","); t = rest + "," + last3; }
    return "₹" + t;
  }

  function row(label, value, cls) {
    return '<div class="calc-total-row' + (cls ? " " + cls : "") + '"><span>' + label +
      "</span><strong>" + value + "</strong></div>";
  }

  function render() {
    var amount = num("plan-amount");
    var rate = num("plan-rate");
    var years = Math.max(1, num("plan-years"));

    if (amount <= 0 || rate <= 0) {
      out.innerHTML = '<p class="calc-empty-text">Enter an amount to see the projection.</p>';
      return;
    }

    if (cfg.type === "recurring") {
      var balance = 0, deposited = 0;
      for (var y = 1; y <= years; y += 1) {
        balance = (balance + amount) * (1 + rate / 100);
        deposited += amount;
      }
      out.innerHTML =
        '<p class="calc-headline-label">At maturity, after ' + years + " years</p>" +
        '<p class="calc-headline-value">' + money(balance) + "</p>" +
        '<p class="calc-headline-note">' + money(deposited) + " deposited at " + rate + "% a year.</p>" +
        '<div class="calc-totals">' +
        row("You deposit", money(deposited)) +
        row("Interest earned", money(balance - deposited)) +
        row("Maturity value", money(balance), "is-grand") +
        "</div>" +
        '<p class="calc-fineprint">Assumes the rate stays constant and every deposit is made.</p>';
      return;
    }

    if (cfg.type === "payout") {
      var periods = cfg.periods || 12;
      var perPeriod = (amount * (rate / 100)) / periods;
      var totalPaid = perPeriod * periods * years;
      var label = periods === 12 ? "each month" : "each quarter";
      var every = periods === 12 ? "monthly" : "quarterly";
      out.innerHTML =
        '<p class="calc-headline-label">You receive ' + every + "</p>" +
        '<p class="calc-headline-value">' + money(perPeriod) + "</p>" +
        '<p class="calc-headline-note">' + label + ", on " + money(amount) + " at " + rate + "%.</p>" +
        '<div class="calc-totals">' +
        row("Interest over " + years + " years", money(totalPaid)) +
        row("Capital returned", money(amount)) +
        row("Total back", money(totalPaid + amount), "is-grand") +
        "</div>" +
        '<p class="calc-fineprint">The interest is taxable at your slab, so the after-tax figure is lower. ' +
        "The rate is revised quarterly for new deposits.</p>";
      return;
    }

    // lumpsum
    var maturity = amount * Math.pow(1 + rate / 100, years);
    out.innerHTML =
      '<p class="calc-headline-label">At maturity, after ' + years + " years</p>" +
      '<p class="calc-headline-value">' + money(maturity) + "</p>" +
      '<p class="calc-headline-note">On ' + money(amount) + " at " + rate + "% a year, compounded annually.</p>" +
      '<div class="calc-totals">' +
      row("You deposit", money(amount)) +
      row("Interest earned", money(maturity - amount)) +
      row("Maturity value", money(maturity), "is-grand") +
      "</div>" +
      '<p class="calc-fineprint">Interest is taxable at your slab unless the scheme says otherwise, so the ' +
      "after-tax return is lower than this figure.</p>";
  }

  form.addEventListener("submit", function (e) { e.preventDefault(); render(); });
  form.addEventListener("input", render);
  form.addEventListener("change", render);
  var reset = document.getElementById("plan-reset");
  if (reset) reset.addEventListener("click", function () { window.setTimeout(render, 0); });
  render();
})();
