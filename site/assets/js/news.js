/* Money news: filter headlines by section. */
(function () {
  "use strict";
  var grid = document.getElementById("news-grid");
  if (!grid) return;
  var chips = Array.prototype.slice.call(document.querySelectorAll("[data-news-cat]"));
  var items = Array.prototype.slice.call(grid.querySelectorAll(".news-item"));

  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      var cat = chip.getAttribute("data-news-cat");
      chips.forEach(function (c) { c.classList.toggle("is-on", c === chip); });
      items.forEach(function (item) {
        item.hidden = cat !== "all" && item.getAttribute("data-cat") !== cat;
      });
    });
  });
})();
