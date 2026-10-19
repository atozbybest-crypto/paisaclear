/* Product filtering on browse.html.
   Everything is pre-rendered in the HTML, so with JS off the full list is still
   readable — this only narrows it down. */

(function () {
  "use strict";

  var results = document.getElementById("results");
  if (!results) return;

  var cards = Array.prototype.slice.call(results.querySelectorAll(".pcard"));
  var input = document.getElementById("q");
  var categorySelect = document.getElementById("filter-category");
  var sortSelect = document.getElementById("sort");
  var returnChips = Array.prototype.slice.call(document.querySelectorAll(".filter-chip[data-return]"));
  var count = document.getElementById("result-count");
  var empty = document.getElementById("no-results");
  var reset = document.getElementById("reset-filters");
  var resetEmpty = document.getElementById("reset-empty");

  var state = { q: "", category: "all", returnType: "all", sort: "default" };

  function apply() {
    var query = state.q.trim().toLowerCase();
    var shown = 0;

    cards.forEach(function (card) {
      var matchText = !query || card.dataset.text.indexOf(query) !== -1;
      var matchCategory = state.category === "all" || card.dataset.category === state.category;
      var matchReturn = state.returnType === "all" || card.dataset.return === state.returnType;
      var visible = matchText && matchCategory && matchReturn;
      card.hidden = !visible;
      if (visible) shown += 1;
    });

    if (state.sort === "risk-asc") {
      cards.sort(function (a, b) {
        var ra = Number(a.dataset.riskband || 99);
        var rb = Number(b.dataset.riskband || 99);
        return ra - rb;
      });
    } else if (state.sort === "name") {
      cards.sort(function (a, b) { return a.dataset.name.localeCompare(b.dataset.name); });
    } else if (state.sort === "min-asc") {
      cards.sort(function (a, b) { return Number(a.dataset.min) - Number(b.dataset.min); });
    }
    cards.forEach(function (card) { results.appendChild(card); });

    count.textContent = shown + (shown === 1 ? " product" : " products");
    empty.hidden = shown !== 0;
    results.hidden = shown === 0;

    var dirty = state.q !== "" || state.category !== "all" || state.returnType !== "all" || state.sort !== "default";
    reset.hidden = !dirty;
  }

  function setReturn(value) {
    state.returnType = value;
    returnChips.forEach(function (chip) {
      var active = chip.dataset.return === value;
      chip.classList.toggle("is-active", active);
      chip.setAttribute("aria-pressed", String(active));
    });
  }

  function syncUrl() {
    if (!window.history || !window.history.replaceState) return;
    var params = new URLSearchParams();
    if (state.q) params.set("q", state.q);
    if (state.category !== "all") params.set("category", state.category);
    if (state.returnType !== "all") params.set("return", state.returnType);
    var qs = params.toString();
    window.history.replaceState(null, "", qs ? "?" + qs : window.location.pathname);
  }

  function resetAll() {
    state.q = "";
    state.category = "all";
    state.sort = "default";
    input.value = "";
    categorySelect.value = "all";
    sortSelect.value = "default";
    setReturn("all");
    apply();
    syncUrl();
    input.focus();
  }

  input.addEventListener("input", function () {
    state.q = input.value;
    apply();
  });

  input.addEventListener("change", syncUrl);

  categorySelect.addEventListener("change", function () {
    state.category = categorySelect.value;
    apply();
    syncUrl();
  });

  sortSelect.addEventListener("change", function () {
    state.sort = sortSelect.value;
    apply();
  });

  returnChips.forEach(function (chip) {
    chip.setAttribute("aria-pressed", String(chip.dataset.return === "all"));
    chip.addEventListener("click", function () {
      setReturn(chip.dataset.return);
      apply();
      syncUrl();
    });
  });

  reset.addEventListener("click", resetAll);
  if (resetEmpty) resetEmpty.addEventListener("click", resetAll);

  // Deep links: ?q=…, ?category=…, ?return=…
  var params = new URLSearchParams(window.location.search);
  if (params.get("q")) {
    state.q = params.get("q");
    input.value = state.q;
  }
  if (params.get("category") && categorySelect.querySelector('option[value="' + params.get("category") + '"]')) {
    state.category = params.get("category");
    categorySelect.value = state.category;
  }
  if (params.get("return")) {
    setReturn(params.get("return"));
  }

  apply();
})();
