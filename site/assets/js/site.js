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

/* Left rail: mobile drawer */
(function () {
  "use strict";
  var toggle = document.querySelector(".nav-toggle");
  var sidebar = document.getElementById("sidebar");
  if (!toggle || !sidebar) return;

  function setOpen(open) {
    document.body.classList.toggle("nav-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    if (open) {
      var scrim = document.createElement("div");
      scrim.className = "nav-scrim";
      scrim.id = "nav-scrim";
      scrim.addEventListener("click", function () { setOpen(false); });
      document.body.appendChild(scrim);
    } else {
      var existing = document.getElementById("nav-scrim");
      if (existing) existing.remove();
    }
  }

  toggle.addEventListener("click", function () {
    setOpen(!document.body.classList.contains("nav-open"));
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") setOpen(false);
  });

  Array.prototype.forEach.call(sidebar.querySelectorAll("a"), function (link) {
    link.addEventListener("click", function () { setOpen(false); });
  });
})();

/* Peeking rail: open on approach, close on leaving. Desktop only. */
(function () {
  "use strict";
  var sidebar = document.getElementById("sidebar");
  var handle = document.querySelector(".rail-handle");
  if (!sidebar || !handle) return;

  var desktop = window.matchMedia("(min-width: 1024px)");
  var closeTimer = null;

  var zone = document.createElement("div");
  zone.className = "rail-hotzone";
  document.body.appendChild(zone);

  function open() {
    if (!desktop.matches) return;
    window.clearTimeout(closeTimer);
    document.body.classList.add("rail-open");
    handle.setAttribute("aria-expanded", "true");
  }

  function closeSoon() {
    if (!desktop.matches) return;
    window.clearTimeout(closeTimer);
    closeTimer = window.setTimeout(function () {
      if (sidebar.contains(document.activeElement)) return;
      document.body.classList.remove("rail-open");
      handle.setAttribute("aria-expanded", "false");
    }, 220);
  }

  zone.addEventListener("mouseenter", open);
  handle.addEventListener("mouseenter", open);
  handle.addEventListener("click", open);
  sidebar.addEventListener("mouseenter", open);
  sidebar.addEventListener("mouseleave", closeSoon);
  sidebar.addEventListener("focusin", open);
  sidebar.addEventListener("focusout", closeSoon);
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      document.body.classList.remove("rail-open");
      handle.setAttribute("aria-expanded", "false");
    }
  });
  desktop.addEventListener("change", function () {
    document.body.classList.remove("rail-open");
  });
})();
