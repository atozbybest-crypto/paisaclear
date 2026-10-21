/* Investment and deposit calculators. Pure client-side arithmetic. */

(function () {
  "use strict";

  var form = document.getElementById("money-form");
  if (!form) return;

  var out = document.getElementById("money-output");
  var tabs = Array.prototype.slice.call(document.querySelectorAll("[data-money-tab]"));
  var mode = "sip";

  function num(id, fallback) {
    var el = document.getElementById("m-" + id);
    if (!el) return fallback || 0;
    var value = parseFloat(String(el.value).replace(/[^0-9.]/g, ""));
    return isNaN(value) ? 0 : value;
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

  function short(value) {
    if (Math.abs(value) >= 10000000) return "₹" + (value / 10000000).toFixed(2) + " Cr";
    if (Math.abs(value) >= 100000) return "₹" + (value / 100000).toFixed(2) + " L";
    return money(value);
  }

  function sipValue(monthly, annualRate, years, stepUp) {
    var r = annualRate / 100 / 12;
    var balance = 0;
    var invested = 0;
    var contribution = monthly;
    for (var year = 0; year < years; year += 1) {
      for (var month = 0; month < 12; month += 1) {
        balance = (balance + contribution) * (1 + r);
        invested += contribution;
      }
      contribution = contribution * (1 + stepUp / 100);
    }
    return { value: balance, invested: invested };
  }

  function lumpSum(value, annualRate, years) {
    return value * Math.pow(1 + annualRate / 100, years);
  }

  function deposit(principal, annualRate, years, compounding) {
    if (compounding === "simple") {
      return principal * (1 + (annualRate / 100) * years);
    }
    var perYear = { annual: 1, "half-yearly": 2, quarterly: 4, monthly: 12 }[compounding] || 4;
    var rate = annualRate / 100 / perYear;
    return principal * Math.pow(1 + rate, perYear * years);
  }

  function rdValue(monthly, annualRate, years, compounding) {
    var perYear = { annual: 1, "half-yearly": 2, quarterly: 4, monthly: 12 }[compounding] || 4;
    var rate = annualRate / 100 / perYear;
    var periods = years * perYear;
    var perPeriod = (monthly * 12) / perYear;
    var value = 0;
    for (var i = 0; i < periods; i += 1) {
      value = (value + perPeriod) * (1 + rate);
    }
    return { value: value, invested: monthly * 12 * years };
  }

  function row(label, value, note) {
    return '<div class="calc-total-row"><span>' + label + '</span><strong>' + value +
      (note ? ' <small class="calc-row-note">' + note + "</small>" : "") + "</strong></div>";
  }

  function render() {
    var years = num("years", 10);
    var rate = num("rate", 8);
    var inflation = num("inflation", 5);
    var result;
    var heading;

    if (mode === "sip") {
      var monthly = num("monthly", 5000);
      result = sipValue(monthly, rate, years, num("stepup", 0));
      heading = "Monthly investing";
    } else if (mode === "lump") {
      var amount = num("amount", 100000);
      result = { value: lumpSum(amount, rate, years), invested: amount };
      heading = "One-time investment";
    } else {
      var principal = num("principal", 100000);
      var monthlyAdd = num("addmonthly", 0);
      var compounding = (document.getElementById("m-compounding") || {}).value || "quarterly";
      if (monthlyAdd > 0) {
        result = rdValue(monthlyAdd, rate, years, compounding);
      } else {
        result = { value: deposit(principal, rate, years, compounding), invested: principal };
      }
      heading = "Deposit maturity";
    }

    if (!result || !isFinite(result.value) || result.value <= 0) {
      out.innerHTML = '<p class="calc-empty-text">Put in an amount and a term to see the result.</p>';
      return;
    }

    var gain = result.value - result.invested;
    var real = result.value / Math.pow(1 + inflation / 100, years);

    out.innerHTML =
      '<p class="calc-headline-label">' + heading + " · after " + years + " years</p>" +
      '<p class="calc-headline-value">' + money(result.value) + "</p>" +
      '<p class="calc-headline-note">Illustrative only — not a forecast and not a guaranteed return.</p>' +
      '<div class="calc-totals">' +
        row("You put in", money(result.invested)) +
        row("Gain", money(gain), "at " + rate + "% a year") +
        row("Value in today's money", money(real), "after " + inflation + "% inflation") +
      "</div>" +
      '<p class="calc-fineprint">Assumes the rate stays constant and ignores tax, exit loads and charges. ' +
      "Real funds do neither.</p>";
  }

  function setMode(next) {
    mode = next;
    tabs.forEach(function (tab) {
      var on = tab.getAttribute("data-money-tab") === next;
      tab.classList.toggle("is-on", on);
      tab.setAttribute("aria-pressed", String(on));
    });
    Array.prototype.forEach.call(document.querySelectorAll("[data-only]"), function (block) {
      if (block.getAttribute("data-only") === "shared") return;
      block.hidden = block.getAttribute("data-only") !== next;
    });
    render();
  }

  tabs.forEach(function (tab) {
    tab.addEventListener("click", function () { setMode(tab.getAttribute("data-money-tab")); });
  });

  form.addEventListener("submit", function (event) { event.preventDefault(); render(); });
  form.addEventListener("input", render);
  form.addEventListener("change", render);

  setMode("sip");
})();
