/* Comparison table on compare.html.
   The catalogue is fetched once from assets/data/catalog.json (cached by the
   browser), which keeps the page itself small. */

(function () {
  "use strict";

  var catalog = [];
  var bySlug = {};
  var byLabel = {};

  function label(p) { return p.name + " — " + p.providerShort; }

  function resolve(value) {
    return bySlug[value] || byLabel[value] || null;
  }

  function applyPreset() {
    var params = new URLSearchParams(window.location.search);
    var preset = (params.get("p") || "").split(",").filter(Boolean);
    preset.slice(0, selects.length).forEach(function (slug, index) {
      var product = bySlug[slug];
      if (product) selects[index].value = label(product);
    });
  }

  function boot(data) {
    catalog = data || [];
    catalog.forEach(function (product) {
      bySlug[product.slug] = product;
      byLabel[label(product)] = product;
    });
    applyPreset();
    render();
  }

  var selects = Array.prototype.slice.call(document.querySelectorAll(".slot-select"));
  var slots = Array.prototype.slice.call(document.querySelectorAll(".slot"));
  var wrap = document.getElementById("compare-wrap");
  var head = document.getElementById("compare-head");
  var bodyEl = document.getElementById("compare-body");
  var hint = document.getElementById("compare-hint");

  var RETURN_TYPES = {
    guaranteed: { label: "Guaranteed", tone: "green" },
    conditional: { label: "Conditional", tone: "amber" },
    "market-linked": { label: "Market-linked", tone: "violet" }
  };
  var RISK = {
    low: { label: "Low risk", tone: "blue" },
    moderate: { label: "Moderate risk", tone: "amber" },
    high: { label: "High risk", tone: "rose" }
  };

  function esc(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function money(amount) {
    if (typeof amount !== "number") return esc(amount || "—");
    var text = String(amount);
    if (text.length <= 3) return "₹" + text;
    var head3 = text.slice(0, -3);
    var tail = text.slice(-3);
    var groups = [];
    while (head3.length > 2) {
      groups.unshift(head3.slice(-2));
      head3 = head3.slice(0, -2);
    }
    if (head3) groups.unshift(head3);
    return "₹" + groups.join(",") + "," + tail;
  }

  function chip(text, tone) {
    return '<span class="chip chip-' + tone + '">' + esc(text) + "</span>";
  }

  var ROWS = [
    {
      label: "Return type",
      render: function (p) {
        var rt = RETURN_TYPES[p.returnType] || { label: p.returnType, tone: "neutral" };
        return chip(rt.label, rt.tone);
      }
    },
    {
      label: "Risk level",
      render: function (p) {
        var risk = RISK[p.riskLevel] || { label: p.riskLevel, tone: "neutral" };
        return chip(risk.label, risk.tone);
      }
    },
    { label: "Minimum investment", render: function (p) { return money(p.minInvestment); } },
    {
      label: "Rate",
      render: function (p) {
        if (p.rate) {
          return esc(p.rate.value) + ' <span class="fact-note">as of ' + esc(String(p.rate.asOf || "")) + "</span>";
        }
        if (p.rateRef) {
          return '<a class="compare-link" href="' + esc(p.rateRef.url) +
            '" target="_blank" rel="noopener noreferrer">Check at source →</a>';
        }
        return "—";
      }
    },
    { label: "Tenure", key: "tenure" },
    { label: "Payout", key: "payout" },
    { label: "Lock-in", key: "lockIn" },
    { label: "Access to your money", key: "liquidity" },
    { label: "Eligibility", key: "eligibility" },
    { label: "Tax", key: "tax" },
    { label: "Protection", key: "protection" },
    { label: "Last verified", key: "lastVerified" }
  ];

  function selected() {
    return selects.map(function (input) { return input.value; }).filter(Boolean);
  }

  function updateAvailability() {
    // The slots are text inputs backed by a shared <datalist>, so there are no
    // per-slot options to disable. Kept for the old <select> markup.
    var chosen = selected();
    selects.forEach(function (field) {
      if (!field.options) return;
      Array.prototype.forEach.call(field.options, function (option) {
        if (!option.value) return;
        option.disabled = option.value !== field.value && chosen.indexOf(option.value) !== -1;
      });
    });
  }

  function render() {
    var slugs = selected();
    updateAvailability();

    slots.forEach(function (slot, index) {
      var filled = Boolean(resolve(selects[index].value));
      slot.classList.toggle("is-filled", filled);
      var clear = slot.querySelector(".slot-clear");
      if (clear) clear.hidden = !filled;
    });

    if (!slugs.length) {
      if (wrap) wrap.hidden = true;
      if (hint) {
        hint.hidden = false;
        hint.textContent = "Pick a product in any slot. You can also add a product straight from its page.";
      }
      return;
    }

    var products = slugs.map(resolve).filter(Boolean);

    if (wrap) wrap.hidden = false;
    if (hint) hint.hidden = false;
    if (hint) hint.textContent =
      products.length === 1
        ? "Add a second product to see them side by side."
        : "Comparing " + products.length + " products. Rates are omitted by design — this compares structure, not price.";

    head.innerHTML =
      "<tr><th scope=\"col\">Product</th>" +
      products
        .map(function (p) {
          return (
            '<th scope="col">' +
            '<span class="compare-name">' + esc(p.name) + "</span>" +
            '<span class="compare-provider">' + esc(p.provider) + "</span>" +
            '<a class="compare-link" href="products/' + esc(p.slug) + '.html">Read the detail →</a>' +
            "</th>"
          );
        })
        .join("") +
      "</tr>";

    bodyEl.innerHTML = ROWS.map(function (row) {
      var cells = products
        .map(function (p) {
          var value = row.render ? row.render(p) : esc(p[row.key] || "—");
          return "<td>" + (value || "—") + "</td>";
        })
        .join("");
      return '<tr><th scope="row">' + esc(row.label) + "</th>" + cells + "</tr>";
    }).join("");

    if (window.history && window.history.replaceState) {
      var params = new URLSearchParams();
      params.set("p", slugs.join(","));
      window.history.replaceState(null, "", "?" + params.toString());
    }
  }

  selects.forEach(function (select) {
    select.addEventListener("change", render);
  });

  slots.forEach(function (slot, index) {
    var clear = slot.querySelector(".slot-clear");
    if (clear) {
      clear.addEventListener("click", function () {
        selects[index].value = "";
        render();
      });
    }
  });

  fetch("assets/data/catalog.json")
    .then(function (r) {
      if (!r.ok) throw new Error("catalogue " + r.status);
      return r.json();
    })
    .then(boot)
    .catch(function (error) {
      if (window.console && window.console.error) window.console.error("compare:", error);
      var host = document.getElementById("compare-wrap");
      if (host) {
        host.innerHTML = '<p class="compare-error">The product list could not be loaded. ' +
          "This page needs to run from a web server — open it at paisaclear.co.in, or start the local " +
          "server with <code>python serve.py</code>.</p>";
      }
      document.querySelectorAll(".slot-select").forEach(function (el) { el.disabled = true; });
    });
})();
