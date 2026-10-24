/* Answers page: filter by text and category. */

(function () {
  "use strict";

  var list = document.getElementById("faq-list");
  if (!list) return;

  var search = document.getElementById("faq-search");
  var chips = Array.prototype.slice.call(document.querySelectorAll(".faq-chip"));
  var items = Array.prototype.slice.call(list.querySelectorAll(".faq-item"));
  var groups = Array.prototype.slice.call(list.querySelectorAll(".faq-group"));
  var count = document.getElementById("faq-count");
  var empty = document.getElementById("faq-empty");
  var category = "all";

  function apply() {
    var q = (search.value || "").trim().toLowerCase();
    var shown = 0;

    items.forEach(function (item) {
      var text = item.textContent.toLowerCase();
      var matchText = !q || text.indexOf(q) !== -1;
      var matchCat = category === "all" || item.dataset.cat === category;
      var visible = matchText && matchCat;
      item.hidden = !visible;
      if (visible) shown += 1;
    });

    groups.forEach(function (group) {
      var any = Array.prototype.some.call(group.querySelectorAll(".faq-item"), function (i) { return !i.hidden; });
      group.hidden = !any;
    });

    count.textContent = shown + (shown === 1 ? " answer" : " answers");
    empty.hidden = shown !== 0;
  }

  search.addEventListener("input", apply);
  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      category = chip.dataset.faqCat;
      chips.forEach(function (c) { c.classList.toggle("is-on", c === chip); });
      apply();
    });
  });
})();
