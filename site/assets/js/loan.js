/* Loan EMI and amortisation. Standard reducing-balance schedule. */

(function () {
  "use strict";

  var form = document.getElementById("loan-form");
  if (!form) return;

  var out = document.getElementById("loan-output");

  function num(id) {
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

  function emiFor(principal, annualRate, months) {
    var r = annualRate / 100 / 12;
    if (months <= 0) return 0;
    if (r === 0) return principal / months;
    var factor = Math.pow(1 + r, months);
    return (principal * r * factor) / (factor - 1);
  }

  function schedule(principal, annualRate, months, payment) {
    var r = annualRate / 100 / 12;
    var balance = principal;
    var rows = [];
    var totalInterest = 0;
    var totalPaid = 0;

    for (var month = 1; month <= months && balance > 0.5; month += 1) {
      var interest = balance * r;
      var principalPart = Math.min(payment - interest, balance);
      if (principalPart <= 0) break;
      balance = balance - principalPart;
      totalInterest += interest;
      totalPaid += principalPart + interest;
      rows.push({ month: month, interest: interest, principal: principalPart, balance: balance });
    }
    return { rows: rows, totalInterest: totalInterest, totalPaid: totalPaid, months: rows.length };
  }

  function donut(principal, interest) {
    var total = principal + interest;
    var share = total > 0 ? (principal / total) * 100 : 0;
    var stops = "var(--green) 0% " + share.toFixed(2) + "%, var(--amber) " + share.toFixed(2) + "% 100%";
    return '<div class="donut" style="background: conic-gradient(' + stops + ')">' +
      '<div class="donut-hole"><span>' + short(total) + "</span><small>total paid</small></div></div>";
  }

  function yearlyTable(rows) {
    var years = {};
    rows.forEach(function (row) {
      var year = Math.ceil(row.month / 12);
      if (!years[year]) years[year] = { principal: 0, interest: 0, balance: row.balance };
      years[year].principal += row.principal;
      years[year].interest += row.interest;
      years[year].balance = row.balance;
    });

    var body = Object.keys(years).map(function (year) {
      var y = years[year];
      return "<tr><td>" + year + "</td><td>" + money(y.principal) + "</td><td>" +
        money(y.interest) + "</td><td>" + money(y.balance) + "</td></tr>";
    }).join("");

    return '<table class="amort"><thead><tr><th scope="col">Year</th><th scope="col">Principal</th>' +
      '<th scope="col">Interest</th><th scope="col">Balance</th></tr></thead><tbody>' + body + "</tbody></table>";
  }

  function render() {
    var principal = num("l-amount");
    var rate = num("l-rate");
    var years = num("l-years");
    var extra = num("l-extra");

    if (principal <= 0 || years <= 0) {
      out.innerHTML = '<p class="calc-empty-text">Enter an amount and a term.</p>';
      return;
    }

    var months = Math.round(years * 12);
    var emi = emiFor(principal, rate, months);
    var base = schedule(principal, rate, months, emi);
    var withExtra = extra > 0 ? schedule(principal, rate, months, emi + extra) : null;

    var saved = withExtra ? base.totalInterest - withExtra.totalInterest : 0;

    out.innerHTML =
      '<p class="calc-headline-label">Monthly payment (EMI)</p>' +
      '<p class="calc-headline-value">' + money(emi) + "</p>" +
      '<p class="calc-headline-note">' + months + " instalments on " + short(principal) +
      " at " + rate + "% a year.</p>" +
      '<div class="calc-visual">' + donut(principal, base.totalInterest) +
      '<ul class="calc-lines">' +
      '<li class="calc-line"><span class="calc-dot" style="background:var(--green)"></span>' +
      '<span class="calc-line-label">Principal</span><span class="calc-line-value">' + short(principal) + "</span></li>" +
      '<li class="calc-line"><span class="calc-dot" style="background:var(--amber)"></span>' +
      '<span class="calc-line-label">Interest</span><span class="calc-line-value">' + short(base.totalInterest) + "</span></li>" +
      "</ul></div>" +
      '<div class="calc-totals">' +
      '<div class="calc-total-row"><span>Total you pay</span><strong>' + money(base.totalPaid) + "</strong></div>" +
      '<div class="calc-total-row"><span>Interest as a share</span><strong>' +
      ((base.totalInterest / principal) * 100).toFixed(0) + "%</strong></div>" +
      (withExtra
        ? '<div class="calc-total-row"><span>With ' + money(extra) + " extra</span><strong>" +
          withExtra.months + " months</strong></div>" +
          '<div class="calc-total-row is-grand"><span>Interest saved</span><strong>' + money(saved) + "</strong></div>"
        : '<div class="calc-total-row is-grand"><span>Interest paid</span><strong>' + money(base.totalInterest) + "</strong></div>") +
      "</div>" +
      '<details class="calc-details" open>' +
      "<summary>Year-by-year schedule</summary>" +
      '<div class="amort-wrap">' + yearlyTable((withExtra || base).rows) + "</div>" +
      "</details>" +
      '<p class="calc-fineprint">Reducing-balance arithmetic. Rates on floating loans change, which changes ' +
      "the EMI or the term.</p>";
  }

  form.addEventListener("submit", function (event) { event.preventDefault(); render(); });
  form.addEventListener("input", render);
  form.addEventListener("change", render);
  render();
})();
