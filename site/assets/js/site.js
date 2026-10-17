/* Small site-wide behaviour: keyboard access to search. */
(function () {
  "use strict";

  var search = document.getElementById("head-q");

  document.addEventListener("keydown", function (event) {
    var tag = document.activeElement ? document.activeElement.tagName : "";
    var typing = /^(INPUT|TEXTAREA|SELECT)$/.test(tag);

    if (event.key === "/" && !typing && search) {
      event.preventDefault();
      search.focus();
      search.select();
    }
  });
})();
