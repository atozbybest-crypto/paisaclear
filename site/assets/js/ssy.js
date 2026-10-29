/* Sukanya Samriddhi calculator: annual deposits, annual compounding, 21-year term. */

(function () {
  "use strict";

  var form = document.getElementById("ssy-form");
  if (!form) return;

  var out = document.getElementById("ssy-output");
  var TERM = 21;

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

  function project(amount, depositYears, ratePct) {
    var rate = ratePct / 100;
    var balance = 0;
    var deposited = 0;
    var rows = [];
    for (var year = 1; year <= TERM; year += 1) {
      if (year <= depositYears) {
        balance += amount;
        deposited += amount;
      }
      var interest = balance * rate;
      balance += interest;
      rows.push({ year: year, deposit: year <= depositYears ? amount : 0, interest: interest, balance: balance });
    }
    return { rows: rows, maturity: balance, deposited: deposited };
  }

  function render() {
    var amount = num("ssy-amount");
    var years = Math.min(15, Math.max(1, num("ssy-years") || 15));
    var rate = num("ssy-rate") || 8.2;

    if (amount <= 0) {
      out.innerHTML = '<p class="calc-empty-text">Enter an amount to see the projection.</p>';
      return;
    }

    var r = project(amount, years, rate);
    var interest = r.maturity - r.deposited;

    var table = r.rows.map(function (row) {
      return "<tr><td>" + row.year + "</td><td>" + (row.deposit ? money(row.deposit) : "—") +
        "</td><td>" + money(row.interest) + "</td><td>" + money(row.balance) + "</td></tr>";
    }).join("");

    out.innerHTML =
      '<p class="calc-headline-label">Value when the account matures</p>' +
      '<p class="calc-headline-value">' + money(r.maturity) + "</p>" +
      '<p class="calc-headline-note">After 21 years, at ' + rate + "% a year.</p>" +
      '<div class="calc-totals">' +
      '<div class="calc-total-row"><span>You deposit</span><strong>' + money(r.deposited) + "</strong></div>" +
      '<div class="calc-total-row"><span>Interest earned</span><strong>' + money(interest) + "</strong></div>" +
      '<div class="calc-total-row is-grand"><span>Maturity value</span><strong>' + money(r.maturity) + "</strong></div>" +
      "</div>" +
      '<details class="calc-details"><summary>Year by year</summary>' +
      '<div class="amort-wrap"><table class="amort"><thead><tr><th scope="col">Year</th>' +
      '<th scope="col">Deposit</th><th scope="col">Interest</th><th scope="col">Balance</th></tr></thead>' +
      "<tbody>" + table + "</tbody></table></div></details>" +
      '<p class="calc-fineprint">Assumes the rate stays at ' + rate + "% for the whole term and that every " +
      "deposit is made. The notified rate is revised each quarter.</p>";
  }

  form.addEventListener("submit", function (e) { e.preventDefault(); render(); });
  form.addEventListener("input", render);
  form.addEventListener("change", render);
  var reset = document.getElementById("ssy-reset");
  if (reset) reset.addEventListener("click", function () { window.setTimeout(render, 0); });
  render();
})();
