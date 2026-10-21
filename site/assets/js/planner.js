/* Spending planner. State lives in localStorage; nothing leaves the browser. */

(function () {
  "use strict";

  var form = document.getElementById("expense-form");
  if (!form) return;

  var KEY = "paisaclear.planner.v1";
  var CATALOG = [];
  var dataEl = document.getElementById("pl-catalog");
  try {
    CATALOG = JSON.parse(dataEl.textContent || "[]");
  } catch (error) {
    CATALOG = [];
  }

  var els = {
    start: document.getElementById("pl-start"),
    income: document.getElementById("pl-income"),
    amount: document.getElementById("pl-amount"),
    category: document.getElementById("pl-category"),
    date: document.getElementById("pl-date"),
    note: document.getElementById("pl-note"),
    list: document.getElementById("pl-list"),
    empty: document.getElementById("pl-empty"),
    balance: document.getElementById("pl-balance"),
    noteLine: document.getElementById("pl-note-line"),
    startOut: document.getElementById("pl-start-out"),
    spent: document.getElementById("pl-spent"),
    daily: document.getElementById("pl-daily"),
    proj: document.getElementById("pl-proj"),
    bars: document.getElementById("pl-bars"),
    suggest: document.getElementById("pl-suggest"),
    suggestList: document.getElementById("pl-suggest-list"),
    suggestNote: document.getElementById("pl-suggest-note"),
  };

  var state = { start: 50000, income: 0, items: [] };

  function load() {
    try {
      var saved = JSON.parse(window.localStorage.getItem(KEY) || "null");
      if (saved && Array.isArray(saved.items)) {
        state = { start: Number(saved.start) || 0, income: Number(saved.income) || 0, items: saved.items };
      }
    } catch (error) { /* first run, or storage blocked */ }
  }

  function save() {
    try {
      window.localStorage.setItem(KEY, JSON.stringify(state));
    } catch (error) { /* private mode: keep working in memory */ }
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

  function todayISO() {
    return new Date().toISOString().slice(0, 10);
  }

  function totals() {
    var spent = state.items.reduce(function (sum, item) { return sum + item.a; }, 0);
    var days = 1;
    if (state.items.length) {
      var dates = state.items.map(function (i) { return i.d; }).sort();
      var first = new Date(dates[0]);
      var last = new Date(dates[dates.length - 1]);
      days = Math.max(1, Math.round((last - first) / 86400000) + 1);
    }
    return {
      spent: spent,
      left: state.start - spent,
      days: days,
      daily: spent / days,
      byCategory: state.items.reduce(function (map, item) {
        map[item.c] = (map[item.c] || 0) + item.a;
        return map;
      }, {}),
    };
  }

  function renderList() {
    var items = state.items.slice().sort(function (a, b) { return a.d < b.d ? 1 : -1; });
    els.list.innerHTML = items.map(function (item) {
      return '<li class="expense-item">' +
        '<span class="expense-cat">' + escapeHtml(item.c) + "</span>" +
        '<span class="expense-note">' + escapeHtml(item.n || "") + "</span>" +
        '<span class="expense-date">' + item.d + "</span>" +
        '<span class="expense-amount">' + money(item.a) + "</span>" +
        '<button type="button" class="expense-del" data-id="' + item.id + '" aria-label="Remove">×</button>' +
        "</li>";
    }).join("");
    els.empty.hidden = state.items.length > 0;
    Array.prototype.forEach.call(els.list.querySelectorAll("[data-id]"), function (button) {
      button.addEventListener("click", function () {
        var id = Number(button.getAttribute("data-id"));
        state.items = state.items.filter(function (i) { return i.id !== id; });
        save(); render();
      });
    });
  }

  function escapeHtml(text) {
    return String(text).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function renderBars(t) {
    var entries = Object.keys(t.byCategory).map(function (category) {
      return { category: category, amount: t.byCategory[category] };
    }).sort(function (a, b) { return b.amount - a.amount; });

    if (!entries.length) {
      els.bars.innerHTML = '<p class="planner-empty">No spends yet.</p>';
      return;
    }

    els.bars.innerHTML = entries.map(function (entry) {
      var share = t.spent ? (entry.amount / t.spent) * 100 : 0;
      return '<div class="bar-row">' +
        '<div class="bar-head"><span>' + escapeHtml(entry.category) + "</span>" +
        "<strong>" + money(entry.amount) + " · " + share.toFixed(0) + "%</strong></div>" +
        '<div class="bar-track"><div class="bar-fill" style="width:' + share.toFixed(1) + '%"></div></div>' +
        "</div>";
    }).join("");
  }

  function renderSuggest(t) {
    if (!CATALOG.length) { els.suggest.hidden = true; return; }
    var budget = Math.max(state.start, t.left, 0);
    if (budget <= 0) { els.suggest.hidden = true; return; }

    var fits = CATALOG.filter(function (p) { return p.m <= budget; });
    if (!fits.length) { els.suggest.hidden = true; return; }

    // one per category, cheapest first, up to four
    var seen = {};
    var picks = [];
    fits.forEach(function (p) {
      if (seen[p.c] || picks.length >= 4) return;
      seen[p.c] = true;
      picks.push(p);
    });

    els.suggest.hidden = false;
    els.suggestNote.textContent =
      "With " + money(budget) + " available, these products have a minimum you already meet. " +
      "Nothing here is a recommendation — it ignores your goals, tax and risk.";
    els.suggestList.innerHTML = picks.map(function (p) {
      return '<li class="suggest-item">' +
        '<a href="../products/' + p.s + '.html">' + escapeHtml(p.n) + "</a>" +
        "<span>" + escapeHtml(p.p) + " · min " + money(p.m) + "</span>" +
        "</li>";
    }).join("");
  }

  function render() {
    var t = totals();
    els.startOut.textContent = money(state.start);
    els.spent.textContent = money(t.spent);
    els.balance.textContent = money(t.left);
    els.daily.textContent = money(t.daily);
    els.proj.textContent = money(t.daily * 30);

    if (t.spent === 0) {
      els.noteLine.textContent = "Enter what you have to begin.";
    } else if (t.left < 0) {
      els.noteLine.textContent = "You have spent " + money(-t.left) + " more than your starting amount.";
    } else {
      els.noteLine.textContent =
        "You have spent " + money(t.spent) + " over " + t.days + " day" + (t.days === 1 ? "" : "s") + ".";
    }

    var top = Object.keys(t.byCategory).sort(function (a, b) { return t.byCategory[b] - t.byCategory[a]; })[0];
    if (top) {
      var share = Math.round((t.byCategory[top] / t.spent) * 100);
      els.noteLine.textContent += " " + top + " is the largest share, at " + share + "%.";
    }

    renderList();
    renderBars(t);
    renderSuggest(t);
    save();
  }

  els.start.value = state.start;
  els.date.value = todayISO();
  load();
  els.start.value = state.start;
  els.income.value = state.income || "";

  els.start.addEventListener("input", function () {
    state.start = Number(els.start.value) || 0;
    render();
  });
  els.income.addEventListener("input", function () {
    state.income = Number(els.income.value) || 0;
    save();
  });

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var amount = Number(els.amount.value);
    if (!amount || amount <= 0) { els.amount.focus(); return; }
    state.items.push({
      id: Date.now(),
      a: amount,
      c: els.category.value,
      d: els.date.value || todayISO(),
      n: (els.note.value || "").trim(),
    });
    els.amount.value = "";
    els.note.value = "";
    render();
    els.amount.focus();
  });

  document.getElementById("pl-clear").addEventListener("click", function () {
    if (!state.items.length) return;
    if (!window.confirm("Delete every logged spend on this device?")) return;
    state.items = [];
    render();
  });

  render();
})();
