/* PaisaClear — self-contained build.
   Renders the whole site from window.PAISA_DATA with hash routing, so the
   bundled page works from file:// with no server and no network. */

(function () {
  "use strict";

  var ICONS = {
    shield: '<path d="M12 3 5 6v5.5c0 4.2 2.9 7.6 7 9.5 4.1-1.9 7-5.3 7-9.5V6l-7-3Z"/><path d="m9.2 12 2 2 3.6-3.8"/>',
    bank: '<path d="M3.5 9.5 12 4l8.5 5.5"/><path d="M5.5 10.5v7M9.8 10.5v7M14.2 10.5v7M18.5 10.5v7"/><path d="M3.5 20.5h17M3 17.8h18"/>',
    layers: '<path d="m12 3.5 8 4.2-8 4.2-8-4.2 8-4.2Z"/><path d="m4 12.2 8 4.2 8-4.2"/><path d="m4 16.4 8 4.2 8-4.2"/>',
    certificate: '<rect x="3.5" y="4.5" width="17" height="12" rx="1.6"/><path d="M7 8.5h6M7 12h4"/><circle cx="17" cy="17.5" r="2.6"/><path d="m15.8 19.6-.6 2 1.8-1 1.8 1-.6-2"/>',
    chart: '<path d="M4 19.5V4.5M4 19.5h16"/><path d="m7.5 15 3.4-4.4 3 2.4 3.4-5"/>',
    calendar: '<rect x="3.8" y="5.4" width="16.4" height="14.6" rx="1.8"/><path d="M8 3.5v3.4M16 3.5v3.4M3.8 10h16.4"/><path d="M8.5 14h2M13.5 14h2M8.5 17h2M13.5 17h2"/>',
    compass: '<circle cx="12" cy="12" r="8.4"/><path d="m15.2 8.8-2 4.4-4.4 2 2-4.4 4.4-2Z"/>',
    seedling: '<path d="M12 20.5v-7.4"/><path d="M12 13.1C12 9.4 9.4 6.6 5.5 6.6c0 3.9 2.8 6.5 6.5 6.5Z"/><path d="M12 13.1c0-3 2.2-5.4 5.6-5.4 0 3.3-2.4 5.4-5.6 5.4Z"/><path d="M8.5 20.5h7"/>',
    clock: '<circle cx="12" cy="12" r="8.4"/><path d="M12 7.4V12l3 1.9"/>',
    receipt: '<path d="M6 3.6h12v16.8l-2.4-1.6-2.4 1.6-2.4-1.6-2.4 1.6L6 20.4Z"/><path d="M9 8.4h6M9 12.2h6"/>',
    arrow: '<path d="M4.5 12h14M13 6.5l5.5 5.5-5.5 5.5"/>',
    check: '<path d="m5 12.5 4.4 4.4L19 6.8"/>',
    alert: '<path d="M12 4.2 21 19.8H3L12 4.2Z"/><path d="M12 10v4.2M12 17h.01"/>',
    umbrella: '<path d="M3.6 12a8.4 8.4 0 0 1 16.8 0Z"/><path d="M12 12v6.2a2.2 2.2 0 0 0 4.4 0"/><path d="M12 3.6V5"/>',
    info: '<circle cx="12" cy="12" r="8.4"/><path d="M12 11v5.2M12 8h.01"/>',
    scale: '<path d="M12 4v16M7 20h10"/><path d="M4 8h16"/><path d="m7.5 8-2.8 5.4h5.6L7.5 8ZM16.5 8l-2.8 5.4h5.6L16.5 8Z"/>'
  };

  var TONES = { guaranteed: "green", conditional: "amber", "market-linked": "violet" };
  var RISK_TONE = { low: "blue", moderate: "amber", high: "rose" };
  var ACCENT = {
    "government-schemes": "green", "bank-deposits": "blue",
    "mutual-funds": "violet", bonds: "amber", etfs: "rose", "lic-life-insurance": "violet"
  };

  function esc(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  function icon(name, cls) {
    return '<svg class="' + (cls || "icon") + '" viewBox="0 0 24 24" aria-hidden="true" focusable="false" ' +
      'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">' +
      (ICONS[name] || ICONS.info) + "</svg>";
  }

  function money(amount) {
    if (typeof amount !== "number") return esc(amount || "—");
    var text = String(amount);
    if (text.length <= 3) return "₹" + text;
    var head = text.slice(0, -3), tail = text.slice(-3), groups = [];
    while (head.length > 2) { groups.unshift(head.slice(-2)); head = head.slice(0, -2); }
    if (head) groups.unshift(head);
    return "₹" + groups.join(",") + "," + tail;
  }

  var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

  function prettyDate(iso) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(iso || ""));
    if (!m) return iso || "—";
    return Number(m[3]) + " " + MONTHS[Number(m[2]) - 1] + " " + m[1];
  }

  function rateLine(p) {
    if (p.rate) {
      return '<p class="pcard-rate"><span class="rate-value">' + esc(p.rate.value) + "</span>" +
        '<span class="rate-note">' + esc(p.rate.label) + " · as of " + esc(prettyDate(p.rate.asOf)) + "</span></p>";
    }
    if (p.rateRef) {
      return '<p class="pcard-rate pcard-rate-ref"><span class="rate-note">' + esc(p.rateRef.label) + "</span>" +
        '<a class="rate-link" href="' + esc(p.rateRef.url) + '" target="_blank" rel="noopener noreferrer">' +
        "Check at source " + icon("arrow", "icon icon-sm") + "</a></p>";
    }
    return "";
  }

  function sourceBlock(p) {
    if (!p.source || !p.source.url) return "";
    var display = String(p.source.url).split("://").pop().replace(/\/$/, "");
    return '<div class="source-strip"><div class="source-strip-head">' +
      '<span class="source-strip-label">Source</span>' +
      '<a class="source-strip-link" href="' + esc(p.source.url) + '" target="_blank" rel="noopener noreferrer">' +
      esc(p.source.label) + ' <span aria-hidden="true">↗</span></a></div>' +
      '<p class="source-strip-url">' + esc(display) + "</p>" +
      '<p class="source-strip-note">' + esc(p.source.note || "") + "</p></div>";
  }

  function ratePanel(p) {
    if (!p.rate) {
      if (!p.rateRef) return "";
      return '<div class="rate-panel rate-panel-ref"><div class="rate-main">' +
        '<span class="rate-label-lg">' + esc(p.rateRef.label) + "</span>" +
        '<span class="rate-label">Not published as a number here — it varies by provider, tenure or plan.</span></div>' +
        '<div class="rate-meta"><p>' + esc(p.rateRef.note || "") + "</p>" +
        '<p><a class="btn btn-ghost" href="' + esc(p.rateRef.url) + '" target="_blank" rel="noopener noreferrer">' +
        "Check the official page " + icon("arrow", "icon icon-sm") + "</a></p></div></div>";
    }
    var via = p.rate.confirmedVia
      ? ' · confirmed via <a href="' + esc(p.rate.confirmedViaUrl || p.rate.sourceUrl) +
        '" target="_blank" rel="noopener noreferrer">' + esc(p.rate.confirmedVia) + "</a>"
      : "";
    return '<div class="rate-panel"><div class="rate-main">' +
      '<span class="rate-value">' + esc(p.rate.value) + "</span>" +
      '<span class="rate-label">' + esc(p.rate.label) + " · " + esc(p.rate.cadence) + "</span></div>" +
      '<div class="rate-meta">' +
      "<p>As of <strong>" + esc(prettyDate(p.rate.asOf)) + "</strong>. Rates change — check the source before acting.</p>" +
      '<p>Source: <a href="' + esc(p.rate.sourceUrl) + '" target="_blank" rel="noopener noreferrer">' +
      esc(p.rate.sourceLabel) + "</a>" + via + "</p></div></div>";
  }

  function data() { return window.PAISA_DATA; }
  function cats() { return data().categories; }
  function products() { return data().products; }
  function bySlug(slug) {
    var list = products();
    for (var i = 0; i < list.length; i++) if (list[i].slug === slug) return list[i];
    return null;
  }
  function catById(id) {
    var list = cats();
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i];
    return null;
  }
  function rtById(id) {
    var list = data().returnTypes;
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i];
    return null;
  }

  function chip(text, tone, extra) {
    return '<span class="chip chip-' + tone + (extra ? " " + extra : "") + '">' + esc(text) + "</span>";
  }
  function returnChip(p) {
    var rt = rtById(p.returnType);
    return chip(rt.label, TONES[p.returnType] || "green", "chip-return");
  }
  function riskChip(p) {
    return chip((p.riskLevel || "moderate").charAt(0).toUpperCase() + (p.riskLevel || "moderate").slice(1) + " risk",
      RISK_TONE[p.riskLevel] || "amber", "chip-risk");
  }

  function productCard(p) {
    var cat = catById(p.category);
    return '<article class="pcard" data-category="' + esc(p.category) + '" data-return="' + esc(p.returnType) +
      '" data-min="' + esc(typeof p.minInvestment === "number" ? p.minInvestment : 0) +
      '" data-name="' + esc(p.name.toLowerCase()) +
      '" data-text="' + esc((p.name + " " + p.provider + " " + (p.oneLiner || "")).toLowerCase()) + '">' +
      '<a class="pcard-link" href="#/product/' + esc(p.slug) + '">' +
        '<div class="pcard-badges">' + returnChip(p) + riskChip(p) +
          '<span class="pcard-cat">' + esc(cat.short) + "</span></div>" +
        '<h3 class="pcard-name">' + esc(p.name) + "</h3>" +
        '<p class="pcard-provider">' + esc(p.provider) + "</p>" +
        '<p class="pcard-line">' + esc(p.oneLiner) + "</p>" +
        rateLine(p) +
        '<dl class="pcard-facts">' +
          "<div><dt>Minimum</dt><dd>" + money(p.minInvestment) + "</dd></div>" +
          "<div><dt>Tenure</dt><dd>" + esc(p.tenure || "—") + "</dd></div>" +
          "<div><dt>Payout</dt><dd>" + esc(p.payout || "—") + "</dd></div>" +
        "</dl>" +
        '<span class="pcard-cta">Read the detail ' + icon("arrow", "icon icon-sm") + "</span>" +
      "</a></article>";
  }

  function categoryCard(c) {
    var count = products().filter(function (p) { return p.category === c.id; }).length;
    var foot = c.status === "guide"
      ? '<span class="cat-count cat-guide">Verify at source</span>'
      : '<span class="cat-count">' + count + " product" + (count === 1 ? "" : "s") + "</span>";
    return '<a class="cat-card cat-' + (ACCENT[c.id] || "green") + '" href="#/category/' + esc(c.id) + '">' +
      '<span class="cat-icon">' + icon(c.icon) + "</span>" +
      '<span class="cat-name">' + esc(c.name) + "</span>" +
      '<span class="cat-tagline">' + esc(c.tagline) + "</span>" +
      '<span class="cat-foot">' + foot + icon("arrow", "icon icon-sm") + "</span></a>";
  }

  function crumb(items) {
    return '<nav class="crumbs" aria-label="Breadcrumb"><ol>' + items.map(function (item) {
      return item[1] ? '<li><a href="' + item[1] + '">' + esc(item[0]) + "</a></li>"
        : '<li aria-current="page">' + esc(item[0]) + "</li>";
    }).join("") + "</ol></nav>";
  }

  function checkList(items) {
    return '<ul class="check-list">' + items.map(function (item) {
      return "<li>" + icon("check", "icon icon-sm") + "<span>" + esc(item) + "</span></li>";
    }).join("") + "</ul>";
  }

  function riskList(items) {
    return '<ul class="risk-list">' + items.map(function (item) {
      return "<li>" + icon("alert", "icon icon-sm") + "<span>" + esc(item) + "</span></li>";
    }).join("") + "</ul>";
  }

  function factRow(label, valueHtml) {
    return '<div class="fact"><dt>' + esc(label) + "</dt><dd>" + valueHtml + "</dd></div>";
  }

  // ------------------------------------------------------------------ home

  function viewHome() {
    var featured = ["monthly-income", "government-backed", "tax-saving"];
    var blocks = featured.map(function (id) {
      var collection = data().collections.filter(function (c) { return c.id === id; })[0];
      var members = products().filter(function (p) { return (p.collections || []).indexOf(id) !== -1; }).slice(0, 4);
      if (!collection || !members.length) return "";
      return '<div class="collection"><div class="collection-head">' +
        '<span class="collection-icon">' + icon(collection.icon) + "</span><div>" +
        "<h3>" + esc(collection.title) + "</h3><p>" + esc(collection.blurb) + "</p></div></div>" +
        '<div class="pcard-row">' + members.map(productCard).join("") + "</div></div>";
    }).join("");

    var rtCards = data().returnTypes.map(function (rt) {
      return '<article class="rt-card rt-' + esc(rt.tone) + '">' +
        '<p class="rt-label">' + esc(rt.label) + "</p>" +
        '<p class="rt-short">' + esc(rt.short) + "</p>" +
        '<p class="rt-def">' + esc(rt.definition) + "</p>" +
        '<div class="rt-ask"><p class="rt-ask-title">Ask yourself</p><ul>' +
        rt.askYourself.map(function (a) { return "<li>" + esc(a) + "</li>"; }).join("") + "</ul></div>" +
        '<a class="text-link" href="#/method">Read the full explanation ' + icon("arrow", "icon icon-sm") + "</a>" +
        "</article>";
    }).join("");

    return '<section class="hero"><div class="shell">' +
      '<p class="eyebrow">Indian financial products, explained without the sales pitch</p>' +
      "<h1>Understand the <em>product</em><br>before you put money in it.</h1>" +
      '<p class="hero-lede">Plain-language detail on how each option works, what it pays, when you can get ' +
      "your money back, and what can go wrong — with the official sources to check.</p>" +
      '<form class="search-panel" data-search role="search">' +
      '<span class="search-panel-icon">' + icon("compass") + "</span>" +
      '<label class="sr-only" for="hero-q">Search financial products</label>' +
      '<input id="hero-q" type="search" autocomplete="off" placeholder="Try “monthly income”, “tax saving”, “government”">' +
      '<button class="btn btn-primary" type="submit">Search products</button></form></div></section>' +

      '<section class="section"><div class="shell">' +
      '<div class="section-head"><div><h2>Start with a category</h2>' +
      '<p class="section-lede">Different kinds of product, each with its own rules about what you are promised ' +
      "and what you can do with your money.</p></div>" +
      '<a class="section-link" href="#/browse">See all products ' + icon("arrow", "icon icon-sm") + "</a></div>" +
      '<div class="cat-grid">' + cats().map(categoryCard).join("") + "</div></div></section>" +

      '<section class="section section-tint"><div class="shell">' +
      '<div class="section-head"><div><h2>Ways in</h2>' +
      '<p class="section-lede">Collections that cut across categories — organised by what you might actually be trying to do.</p>' +
      "</div></div>" + blocks +
      '<a class="more-link" href="#/browse">Browse all ' + products().length + " products " +
      icon("arrow", "icon icon-sm") + "</a></div></section>" +

      '<section class="section"><div class="shell">' +
      '<div class="section-head"><div><h2>Guaranteed, conditional, market-linked</h2>' +
      '<p class="section-lede">Almost every product falls into one of these three buckets. Knowing which one ' +
      'you are looking at answers most of the important questions.</p></div>' +
      '<a class="section-link" href="#/method">Full explanation ' + icon("arrow", "icon icon-sm") + "</a></div>" +
      '<div class="rt-grid">' + rtCards + "</div></div></section>" +

      '<section class="cta-band"><div class="shell cta-inner"><div><h2>Comparing two or three options?</h2>' +
      "<p>Put them side by side — minimum investment, tenure, payout, access to your money, risk and tax.</p></div>" +
      '<a class="btn btn-primary" href="#/compare">Open the comparison table ' + icon("arrow", "icon icon-sm") + "</a>" +
      "</div></section>";
  }

  // ---------------------------------------------------------------- browse

  function viewBrowse(params) {
    var q = params.get("q") || "";
    var rtChips = data().returnTypes.map(function (rt) {
      return '<button class="filter-chip" type="button" data-return="' + esc(rt.id) + '">' + esc(rt.label) + "</button>";
    }).join("");

    return '<section class="page-head"><div class="shell">' +
      crumb([["Home", "#/"], ["All products", ""]]) +
      "<h1>All products</h1>" +
      '<p class="page-lede">' + products().length + " products across all five categories. Each record names " +
      "its provider and terms, and every figure is either dated and sourced or replaced with a link to the " +
      "provider's own page where it genuinely varies.</p>" +
      "</div></section>" +

      '<section class="shell"><div class="filter-bar" role="search">' +
      '<div class="filter-search"><label class="sr-only" for="q">Search products</label>' +
      '<input id="q" type="search" placeholder="Search by name, provider or feature" autocomplete="off" value="' +
      esc(q) + '"></div>' +
      '<div class="filter-row">' +
      '<label class="select-wrap"><span class="select-label">Category</span><select id="filter-category">' +
      '<option value="all">All categories</option>' +
      cats().map(function (c) { return '<option value="' + esc(c.id) + '">' + esc(c.name) + "</option>"; }).join("") +
      "</select></label>" +
      '<label class="select-wrap"><span class="select-label">Sort</span><select id="sort">' +
      '<option value="default">Featured order</option>' +
      '<option value="min-asc">Minimum investment: low to high</option>' +
      '<option value="name">Name A–Z</option></select></label></div>' +
      '<div class="filter-returns" role="group" aria-label="Filter by return type">' +
      '<span class="filter-label">What you are promised</span>' +
      '<button class="filter-chip is-active" type="button" data-return="all">Any</button>' + rtChips + "</div>" +
      '<div class="filter-status"><p id="result-count" role="status" aria-live="polite">' +
      products().length + ' products</p><button class="text-link" type="button" id="reset-filters" hidden>Reset filters</button></div>' +
      "</div>" +
      '<div class="pcard-grid" id="results">' + products().map(productCard).join("") + "</div>" +
      '<div class="empty-state" id="no-results" hidden><p class="empty-title">Nothing matches those filters.</p>' +
      '<p>Try a broader search, or <button class="text-link" type="button" id="reset-empty">clear the filters</button>.</p></div>' +
      "</section>";
  }

  // -------------------------------------------------------------- category

  function viewCategory(id) {
    var category = catById(id);
    if (!category) return viewNotFound();

    if (category.status === "guide") {
      var guide = category.guide || {};
      var guideLinks = (guide.links || []).map(function (link) {
        return '<li><a href="' + esc(link.url) + '" target="_blank" rel="noopener noreferrer">' +
          esc(link.label) + '<span class="ext" aria-hidden="true">↗</span></a></li>';
      }).join("");
      var guideChecks = category.whatToCheck.map(function (item) {
        return "<li>" + icon("check", "icon icon-sm") + "<span>" + esc(item) + "</span></li>";
      }).join("");
      var verifyItems = (guide.verify || []).map(function (item) {
        return '<li><a href="' + esc(item.url) + '" target="_blank" rel="noopener noreferrer">' + esc(item.label) +
          '<span class="ext" aria-hidden="true">↗</span></a><span class="verify-note">' + esc(item.note) + "</span></li>";
      }).join("");
      var verifyBlock = verifyItems
        ? '<div class="verify-block"><p class="verify-title">Where to verify, before you act</p>' +
          '<ul class="verify-list">' + verifyItems + "</ul></div>"
        : "";

      return '<section class="page-head page-head-cat cat-' + (ACCENT[id] || "green") + '"><div class="shell">' +
        crumb([["Home", "#/"], ["All products", "#/browse"], [category.name, ""]]) +
        '<span class="page-icon">' + icon(category.icon) + "</span>" +
        "<h1>" + esc(category.name) + "</h1>" +
        '<p class="page-lede">' + esc(category.blurb) + "</p>" +
        '<p class="page-meta">Guide · no product records published yet</p></div></section>' +

        '<section class="section"><div class="shell"><div class="split"><div class="split-main">' +
        '<div class="guide-panel">' +
        '<p class="guide-kicker">Why there are no products listed here</p>' +
        '<p class="guide-reason">' + esc(guide.reason || "") + "</p>" +
        '<p class="guide-instead">' + esc(guide.instead || "") + "</p>" +
        '<ul class="source-links">' + guideLinks + "</ul>" + verifyBlock + "</div>" +
        '<h2 class="subhead" style="margin-top:34px">What to check, whichever provider you use</h2>' +
        '<ul class="check-list">' + guideChecks + "</ul>" +
        '<p class="muted" style="margin-top:22px">The two live categories — ' +
        '<a href="#/category/government-schemes">government schemes</a> and ' +
        '<a href="#/category/bonds">government bonds</a> — carry full product records with dated, sourced rates.</p>' +
        "</div>" +
        '<aside class="split-aside"><div class="aside-card"><h2>Other categories</h2><div class="pill-links">' +
        cats().filter(function (c) { return c.id !== id; }).map(function (c) {
          return '<a class="pill-link" href="#/category/' + esc(c.id) + '">' + esc(c.short) + "</a>";
        }).join("") + "</div></div></aside></div></div></section>";
    }

    var members = products().filter(function (p) { return p.category === id; });
    var count = {};
    members.forEach(function (p) { count[p.returnType] = (count[p.returnType] || 0) + 1; });
    var mix = Object.keys(count).map(function (k) {
      return count[k] + " " + rtById(k).label.toLowerCase();
    }).join(" · ");

    return '<section class="page-head page-head-cat cat-' + (ACCENT[id] || "green") + '"><div class="shell">' +
      crumb([["Home", "#/"], ["All products", "#/browse"], [category.name, ""]]) +
      '<span class="page-icon">' + icon(category.icon) + "</span>" +
      "<h1>" + esc(category.name) + "</h1>" +
      '<p class="page-lede">' + esc(category.blurb) + "</p>" +
      '<p class="page-meta">' + members.length + " products · " + esc(mix) + "</p></div></section>" +

      '<section class="section"><div class="shell"><div class="split"><div class="split-main">' +
      '<h2 class="subhead">Products in this category</h2>' +
      '<div class="pcard-grid">' + members.map(productCard).join("") + "</div></div>" +
      '<aside class="split-aside"><div class="aside-card"><h2>What to check first</h2>' +
      checkList(category.whatToCheck) + "</div>" +
      '<div class="aside-card"><h2>Other categories</h2><div class="pill-links">' +
      cats().filter(function (c) { return c.id !== id; }).map(function (c) {
        return '<a class="pill-link" href="#/category/' + esc(c.id) + '">' + esc(c.short) + "</a>";
      }).join("") + "</div></div></aside></div></div></section>";
  }

  // --------------------------------------------------------------- product

  function viewProduct(slug) {
    var p = bySlug(slug);
    if (!p) return viewNotFound();
    var category = catById(p.category);
    var rt = rtById(p.returnType);
    var related = products().filter(function (x) {
      return x.category === p.category && x.slug !== p.slug;
    }).slice(0, 3);

    var glance = [
      factRow("Return type", returnChip(p) + ' <span class="fact-note">' + esc(rt.short) + "</span>"),
      p.rate ? factRow("Rate", esc(p.rate.value) + ' <span class="fact-note">as of ' + esc(prettyDate(p.rate.asOf)) + "</span>") : "",
      factRow("Provider", esc(p.provider)),
      factRow("Minimum", money(p.minInvestment) + (p.minInvestmentNote ? ' <span class="fact-note">' + esc(p.minInvestmentNote) + "</span>" : "")),
      factRow("Tenure", esc(p.tenure)),
      factRow("Payout", esc(p.payout)),
      factRow("Lock-in", esc(p.lockIn || "None")),
      factRow("Risk", riskChip(p)),
      factRow("Last verified", esc(p.lastVerified))
    ].join("");

    var sources = p.sources.map(function (s) {
      return '<li><a href="' + esc(s.url) + '" target="_blank" rel="noopener noreferrer">' + esc(s.label) +
        '<span class="ext" aria-hidden="true">↗</span></a></li>';
    }).join("");

    return '<section class="product-head"><div class="shell">' +
      crumb([["Home", "#/"], [category.short, "#/category/" + category.id], [p.name, ""]]) +
      '<div class="product-head-inner"><div class="product-title"><div class="badge-row">' +
      returnChip(p) + riskChip(p) + '<span class="chip chip-neutral">Verified record</span></div>' +
      "<h1>" + esc(p.name) + "</h1>" +
      '<p class="product-provider">' + esc(p.provider) + " · " + esc(category.name) + "</p>" +
      '<p class="product-oneliner">' + esc(p.oneLiner) + "</p></div></div></div></section>" +

      '<div class="shell">' + ratePanel(p) + sourceBlock(p) + "</div>" +

      '<section class="section product-body"><div class="shell"><div class="split"><div class="split-main">' +

      '<section class="prose-block"><h2>How it works</h2><p>' + esc(p.name) + " is a " +
      esc(category.short.toLowerCase()) + " product from " + esc(p.provider) + ", in the <strong>" +
      esc(rt.label.toLowerCase()) + "</strong> category: " + esc(rt.short.toLowerCase()) + ". " +
      esc(p.oneLiner) + "</p>" +
      '<p class="muted">Because the return type is ' + esc(rt.label.toLowerCase()) +
      ", the questions that matter most are: " + esc(rt.askYourself[0]) + " " + esc(rt.askYourself[1]) + "</p>" +
      '<ul class="uses">' + p.commonUses.map(function (u) { return "<li>" + esc(u) + "</li>"; }).join("") + "</ul></section>" +

      '<section class="prose-block"><h2>Key facts</h2><div class="fact-table">' +
      factRow("Provider", esc(p.provider)) +
      (p.source ? factRow("Source", '<a href="' + esc(p.source.url) + '" target="_blank" rel="noopener noreferrer">' + esc(p.source.label) + " ↗</a> <span class=\"fact-note\">" + esc(p.source.url) + "</span>") : "") +
      (p.rate ? factRow("Rate", esc(p.rate.value) + ' <span class="fact-note">' + esc(p.rate.label) + ", as of " + esc(prettyDate(p.rate.asOf)) + "</span>") : (p.rateRef ? factRow("Rate", '<a href="' + esc(p.rateRef.url) + '" target="_blank" rel="noopener noreferrer">' + esc(p.rateRef.label) + " ↗</a>") : "")) +
      factRow("Category", '<a href="#/category/' + category.id + '">' + esc(category.name) + "</a>") +
      factRow("Minimum investment", money(p.minInvestment) + (p.minInvestmentNote ? ' <span class="fact-note">' + esc(p.minInvestmentNote) + "</span>" : "")) +
      factRow("Tenure", esc(p.tenure)) +
      factRow("Payout", esc(p.payout)) +
      factRow("Eligibility", esc(p.eligibility)) +
      factRow("Getting your money back", esc(p.liquidity)) +
      factRow("Protection", esc(p.protection)) +
      factRow("Tax", esc(p.tax)) +
      "</div></section>" +

      '<section class="prose-block"><h2>What can go wrong</h2>' + riskList(p.risks) + "</section>" +

      '<section class="prose-block"><h2>Before you decide anything</h2>' + checkList(p.check) +
      '<p class="muted">These are questions to take to the provider, not a checklist that makes a product suitable. ' +
      "Whether something fits your situation is a decision only you — or an adviser you choose — can make.</p></section>" +

      '<section class="prose-block"><h2>Official sources</h2><ul class="source-links">' + sources + "</ul>" +
      '<p class="muted">These link to the regulator or provider where the rules for this <em>type</em> of product ' +
      "are set out. They are not pages for this fictional product.</p></section></div>" +

      '<aside class="split-aside"><div class="aside-card aside-glance"><h2>At a glance</h2>' +
      '<div class="fact-table fact-table-tight">' + glance + "</div>" +
      '<a class="btn btn-primary btn-block" href="#/compare?p=' + esc(p.slug) + '">Compare this product ' +
      icon("scale", "icon icon-sm") + "</a></div>" +
      '<div class="aside-card"><h2>Verification</h2>' +
      '<p class="aside-note">Last checked <strong>' + esc(p.lastVerified) + "</strong>. Approved for publication by " +
      esc((p.review && p.review.reviewer) || "an editor") + ".</p>" +
      '<p class="aside-note">Status: <span class="status status-approved">Approved</span></p></div></aside>' +
      "</div></div></section>" +

      (related.length ? '<section class="section section-tint"><div class="shell">' +
        '<div class="section-head"><div><h2>Other products in this category</h2>' +
        '<p class="section-lede">The same rules and the same kind of trade-offs, described the same way.</p></div></div>' +
        '<div class="pcard-grid">' + related.map(productCard).join("") + "</div></div></section>" : "");
  }

  // --------------------------------------------------------------- compare

  function viewCompare(params) {
    var preset = (params.get("p") || "").split(",").filter(Boolean).slice(0, 3);
    var options = products().map(function (p) {
      return '<option value="' + esc(p.slug) + '">' + esc(p.name) + " — " + esc(p.providerShort) + "</option>";
    }).join("");

    var slots = [0, 1, 2].map(function (i) {
      var value = preset[i] || "";
      return '<div class="slot' + (value ? " is-filled" : "") + '" data-slot="' + i + '">' +
        '<label class="slot-label" for="slot-' + i + '">Product ' + (i + 1) + "</label>" +
        '<select class="slot-select" id="slot-' + i + '" data-slot="' + i + '">' +
        '<option value="">Choose a product…</option>' + options + "</select>" +
        '<button class="slot-clear" type="button" data-clear="' + i + '"' + (value ? "" : " hidden") + ">Remove</button></div>";
    }).join("");

    return '<section class="page-head"><div class="shell">' +
      crumb([["Home", "#/"], ["Compare", ""]]) +
      "<h1>Compare up to three products</h1>" +
      '<p class="page-lede">Side by side on the things that are comparable: what you are promised, how long your ' +
      "money is held, how you get it back, and where the risks sit. Prices and rates are deliberately not shown — " +
      "the demo data does not invent them.</p></div></section>" +

      '<section class="section"><div class="shell">' +
      '<div class="compare-slots">' + slots + "</div>" +
      '<p class="compare-hint" id="compare-hint">Pick a product in any slot. You can also add a product straight from its page.</p>' +
      '<div class="compare-wrap" id="compare-wrap" hidden><table class="compare-table" id="compare-table">' +
      '<caption class="sr-only">Comparison of selected financial products</caption>' +
      '<thead id="compare-head"></thead><tbody id="compare-body"></tbody></table></div>' +

      '<div class="compare-notes"><h2>How to read this</h2><ul class="check-list">' +
      "<li>" + icon("check", "icon icon-sm") + "<span><strong>Return type</strong> matters more than any headline number: guaranteed, conditional and market-linked products fail in different ways.</span></li>" +
      "<li>" + icon("check", "icon icon-sm") + "<span><strong>Lock-in</strong> is the real cost of a higher rate. Check what happens if life changes in year two.</span></li>" +
      "<li>" + icon("check", "icon icon-sm") + "<span><strong>No rates are shown.</strong> Inventing an illustrative rate would make an unverifiable comparison look precise.</span></li>" +
      "<li>" + icon("check", "icon icon-sm") + "<span><strong>Nothing here is a recommendation.</strong> A product that ranks well on one row can be wrong for your situation.</span></li>" +
      "</ul></div></div></section>";
  }

  // ---------------------------------------------------------------- method

  function viewMethod() {
    var rtSections = data().returnTypes.map(function (rt) {
      return '<article class="method-rt rt-' + esc(rt.tone) + '" id="rt-' + esc(rt.id) + '">' +
        '<div class="method-rt-head"><span class="rt-dot" aria-hidden="true"></span><h3>' + esc(rt.label) +
        '</h3><span class="rt-tag">' + esc(rt.short) + "</span></div>" +
        "<p>" + esc(rt.definition) + "</p><p>" + esc(rt.detail) + "</p>" +
        '<div class="rt-ask"><p class="rt-ask-title">Ask yourself</p><ul>' +
        rt.askYourself.map(function (a) { return "<li>" + esc(a) + "</li>"; }).join("") + "</ul></div></article>";
    }).join("");

    return '<section class="page-head"><div class="shell">' +
      crumb([["Home", "#/"], ["How we work", ""]]) +
      "<h1>How this catalogue works</h1>" +
      '<p class="page-lede">PaisaClear exists to explain financial products clearly, not to sell them. This page ' +
      "sets out what we publish, how a product gets approved, and what we deliberately do not do.</p></div></section>" +

      '<section class="section"><div class="shell shell-narrow"><div class="prose">' +
      "<h2>Where the numbers come from</h2><p>All five categories carry product records. Government schemes " +
      "and government securities show a rate with the date it applied and a link to where it came from — " +
      "small-savings rates are notified each quarter, while bond yields are pulled from the RBI by a refresh job.</p>" +
      "<p>Mutual funds and ETFs show the published NAV from AMFI's daily file. Bank deposits are the exception: " +
      "the rate depends on the bank, the tenure and the deposit slab, so each entry links straight to that bank's " +
      "own rate card rather than quoting a number that would be wrong for most readers.</p>" +
      "<h2>What we do</h2>" + checkList([
        "Describe how a product works, in the same fields for every entry.",
        "Show the trade-offs plainly: lock-in, access, tax, and what can go wrong.",
        "Link to the regulator or provider where the actual rules live.",
        "Date every page, because rates and rules change."
      ]) +
      "<h2>What we do not do</h2>" +
      '<ul class="cross-list">' +
      "<li>" + icon("alert", "icon icon-sm") + "<span>We do not recommend products, or say what you should buy or sell.</span></li>" +
      "<li>" + icon("alert", "icon icon-sm") + "<span>We do not ask for money, take payments, or offer subscriptions.</span></li>" +
      "<li>" + icon("alert", "icon icon-sm") + "<span>We do not quote rates we cannot verify from a primary source.</span></li>" +
      "<li>" + icon("alert", "icon icon-sm") + "<span>We do not ask for your personal or financial details.</span></li>" +
      "</ul></div></div></section>" +

      '<section class="section section-tint"><div class="shell">' +
      '<div class="section-head"><div><h2>The three return types</h2>' +
      '<p class="section-lede">Every product is filed under one of these. It is the single most useful thing to ' +
      "establish before reading further.</p></div></div>" +
      '<div class="method-rt-grid">' + rtSections + "</div></div></section>" +

      '<section class="section" id="approval"><div class="shell shell-narrow">' +
      '<div class="prose"><h2>How a product gets published</h2>' +
      "<p>Products are never written straight into the website. They move through a small, deliberate pipeline, " +
      "and each stage is visible in the content files.</p></div>" +
      '<ol class="pipeline">' +
      '<li><span class="step-no">1</span><div><strong>Research</strong><p>A product record is drafted with its ' +
      "provider, terms, eligibility, tax position and risks, plus at least one source link.</p>" +
      '<span class="status status-draft">draft</span></div></li>' +
      '<li><span class="step-no">2</span><div><strong>Check</strong><p>A second person verifies each field against ' +
      "the source, and confirms no rate or guarantee is stated without one. The record is marked pending.</p>" +
      '<span class="status status-pending">pending</span></div></li>' +
      '<li><span class="step-no">3</span><div><strong>Approve</strong><p>An editor signs off, and the record carries ' +
      "the reviewer's name and the approval date. Only then can it be built into the site.</p>" +
      '<span class="status status-approved">approved</span></div></li>' +
      '<li><span class="step-no">4</span><div><strong>Publish</strong><p>The build reads only approved records. ' +
      "Anything in draft, pending or rejected is skipped — it cannot leak onto a page by accident.</p>" +
      '<span class="status status-live">live</span></div></li>' +
      "</ol>" +
      '<div class="prose"><h2>Sources and verification</h2><p>Each product lists the regulator or provider where its ' +
      "rules are set out — the RBI, SEBI, PFRDA, the Income Tax Department, NSE, AMFI and similar bodies. The link is " +
      "to the authoritative page for that <em>kind</em> of product, not to the product itself, because these products " +
      "are fictional.</p><p>Every entry carries a <strong>last verified</strong> date. If a page is more than six " +
      "months old, treat its terms as possibly out of date and check the source.</p>" +
      "<h2>Corrections</h2><p>If a field is wrong, the record is corrected and the verification date updated. We " +
      "would rather remove an entry than leave a claim we cannot stand behind.</p></div></div></section>";
  }

  function viewNotFound() {
    return '<section class="page-head"><div class="shell"><h1>That page isn’t here</h1>' +
      '<p class="page-lede">The link may be old, or the product may have been removed from the catalogue.</p>' +
      '<p style="margin-top:22px"><a class="btn btn-primary" href="#/">Back to the homepage</a> ' +
      '<a class="btn btn-ghost" href="#/browse">Browse all products</a></p></div></section>';
  }

  // -------------------------------------------------------------- compare logic

  var RETURN_TYPES = {
    guaranteed: { label: "Guaranteed", tone: "green" },
    conditional: { label: "Conditional", tone: "amber" },
    "market-linked": { label: "Market-linked", tone: "violet" }
  };
  var RISK_LABELS = {
    low: { label: "Low risk", tone: "blue" },
    moderate: { label: "Moderate risk", tone: "amber" },
    high: { label: "High risk", tone: "rose" }
  };

  var COMPARE_ROWS = [
    { label: "Return type", render: function (p) {
      var rt = RETURN_TYPES[p.returnType] || { label: p.returnType, tone: "neutral" };
      return chip(rt.label, rt.tone);
    } },
    { label: "Risk level", render: function (p) {
      var risk = RISK_LABELS[p.riskLevel] || { label: p.riskLevel, tone: "neutral" };
      return chip(risk.label, risk.tone);
    } },
    { label: "Minimum investment", render: function (p) { return money(p.minInvestment); } },
    {
      label: "Rate",
      render: function (p) {
        if (p.rate) return esc(p.rate.value) + ' <span class="fact-note">as of ' + esc(prettyDate(p.rate.asOf)) + "</span>";
        if (p.rateRef) {
          return '<a class="compare-link" href="' + esc(p.rateRef.url) + '" target="_blank" rel="noopener noreferrer">Check at source →</a>';
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

  function mountCompare() {
    var selects = Array.prototype.slice.call(document.querySelectorAll(".slot-select"));
    var slots = Array.prototype.slice.call(document.querySelectorAll(".slot"));
    var wrap = document.getElementById("compare-wrap");
    var head = document.getElementById("compare-head");
    var bodyEl = document.getElementById("compare-body");
    var hint = document.getElementById("compare-hint");
    if (!selects.length || !wrap) return;

    function selected() {
      return selects.map(function (s) { return s.value; }).filter(Boolean);
    }

    function draw() {
      var slugs = selected();

      selects.forEach(function (select) {
        Array.prototype.forEach.call(select.options, function (option) {
          if (!option.value) return;
          option.disabled = option.value !== select.value && slugs.indexOf(option.value) !== -1;
        });
      });
      slots.forEach(function (slot, index) {
        var filled = Boolean(selects[index].value);
        slot.classList.toggle("is-filled", filled);
        var clear = slot.querySelector(".slot-clear");
        if (clear) clear.hidden = !filled;
      });

      if (!slugs.length) {
        wrap.hidden = true;
        hint.hidden = false;
        hint.textContent = "Pick a product in any slot. You can also add a product straight from its page.";
        return;
      }

      var chosen = slugs.map(bySlug).filter(Boolean);
      wrap.hidden = false;
      hint.hidden = false;
      hint.textContent = chosen.length === 1
        ? "Add a second product to see them side by side."
        : "Comparing " + chosen.length + " products. Rates are omitted by design — this compares structure, not price.";

      head.innerHTML = '<tr><th scope="col">Product</th>' + chosen.map(function (p) {
        return '<th scope="col"><span class="compare-name">' + esc(p.name) + "</span>" +
          '<span class="compare-provider">' + esc(p.provider) + "</span>" +
          '<a class="compare-link" href="#/product/' + esc(p.slug) + '">Read the detail →</a></th>';
      }).join("") + "</tr>";

      bodyEl.innerHTML = COMPARE_ROWS.map(function (row) {
        return '<tr><th scope="row">' + esc(row.label) + "</th>" + chosen.map(function (p) {
          var value = row.render ? row.render(p) : esc(p[row.key] || "—");
          return "<td>" + (value || "—") + "</td>";
        }).join("") + "</tr>";
      }).join("");
    }

    selects.forEach(function (select) {
      select.addEventListener("change", function () {
        draw();
        var slugs = selected();
        if (window.history && window.history.replaceState) {
          window.history.replaceState(null, "", "#/compare" + (slugs.length ? "?p=" + slugs.join(",") : ""));
        }
      });
    });

    slots.forEach(function (slot, index) {
      var clear = slot.querySelector(".slot-clear");
      if (clear) clear.addEventListener("click", function () {
        selects[index].value = "";
        draw();
      });
    });

    draw();
  }

  // ----------------------------------------------------------- browse logic

  function mountBrowse(params) {
    var results = document.getElementById("results");
    if (!results) return;

    var cards = Array.prototype.slice.call(results.querySelectorAll(".pcard"));
    var input = document.getElementById("q");
    var categorySelect = document.getElementById("filter-category");
    var sortSelect = document.getElementById("sort");
    var chipsEls = Array.prototype.slice.call(document.querySelectorAll(".filter-chip[data-return]"));
    var countEl = document.getElementById("result-count");
    var empty = document.getElementById("no-results");
    var reset = document.getElementById("reset-filters");
    var resetEmpty = document.getElementById("reset-empty");

    var state = {
      q: params.get("q") || "",
      category: params.get("category") || "all",
      returnType: params.get("return") || "all",
      sort: "default"
    };
    input.value = state.q;
    if (categorySelect.querySelector('option[value="' + state.category + '"]')) {
      categorySelect.value = state.category;
    } else {
      state.category = "all";
    }

    function setReturn(value) {
      state.returnType = value;
      chipsEls.forEach(function (chipEl) {
        var active = chipEl.dataset.return === value;
        chipEl.classList.toggle("is-active", active);
        chipEl.setAttribute("aria-pressed", String(active));
      });
    }

    function apply() {
      var query = state.q.trim().toLowerCase();
      var shown = 0;
      cards.forEach(function (card) {
        var visible = (!query || card.dataset.text.indexOf(query) !== -1) &&
          (state.category === "all" || card.dataset.category === state.category) &&
          (state.returnType === "all" || card.dataset.return === state.returnType);
        card.hidden = !visible;
        if (visible) shown += 1;
      });

      if (state.sort === "name") {
        cards.sort(function (a, b) { return a.dataset.name.localeCompare(b.dataset.name); });
      } else if (state.sort === "min-asc") {
        cards.sort(function (a, b) { return Number(a.dataset.min) - Number(b.dataset.min); });
      }
      cards.forEach(function (card) { results.appendChild(card); });

      countEl.textContent = shown + (shown === 1 ? " product" : " products");
      empty.hidden = shown !== 0;
      results.hidden = shown === 0;
      reset.hidden = !(state.q || state.category !== "all" || state.returnType !== "all" || state.sort !== "default");
    }

    input.addEventListener("input", function () { state.q = input.value; apply(); });
    categorySelect.addEventListener("change", function () { state.category = categorySelect.value; apply(); });
    sortSelect.addEventListener("change", function () { state.sort = sortSelect.value; apply(); });
    chipsEls.forEach(function (chipEl) {
      chipEl.setAttribute("aria-pressed", String(chipEl.dataset.return === state.returnType));
      chipEl.addEventListener("click", function () { setReturn(chipEl.dataset.return); apply(); });
    });

    function resetAll() {
      state.q = "";
      state.category = "all";
      state.sort = "default";
      input.value = "";
      categorySelect.value = "all";
      sortSelect.value = "default";
      setReturn("all");
      apply();
      input.focus();
    }
    reset.addEventListener("click", resetAll);
    if (resetEmpty) resetEmpty.addEventListener("click", resetAll);

    setReturn(state.returnType);
    apply();
  }

  // ---------------------------------------------------------------- router

  function parseHash() {
    var raw = (window.location.hash || "#/").replace(/^#/, "");
    var question = raw.indexOf("?");
    var path = question === -1 ? raw : raw.slice(0, question);
    var query = new URLSearchParams(question === -1 ? "" : raw.slice(question + 1));
    if (!path || path === "/") path = "/";
    return { path: path.replace(/\/$/, "") || "/", params: query };
  }

  function render() {
    var route = parseHash();
    var parts = route.path.split("/").filter(Boolean);
    var html;
    var title = "PaisaClear — understand Indian financial products";

    if (parts.length === 0) {
      html = viewHome();
    } else if (parts[0] === "browse") {
      html = viewBrowse(route.params);
      title = "All products — PaisaClear";
    } else if (parts[0] === "category" && parts[1]) {
      html = viewCategory(parts[1]);
      var cat = catById(parts[1]);
      if (cat) title = cat.name + " — PaisaClear";
    } else if (parts[0] === "product" && parts[1]) {
      html = viewProduct(parts[1]);
      var p = bySlug(parts[1]);
      if (p) title = p.name + " — PaisaClear";
    } else if (parts[0] === "compare") {
      html = viewCompare(route.params);
      title = "Compare products — PaisaClear";
    } else if (parts[0] === "method") {
      html = viewMethod();
      title = "How this catalogue works — PaisaClear";
    } else {
      html = viewNotFound();
      title = "Page not found — PaisaClear";
    }

    var app = document.getElementById("app");
    if (app) app.innerHTML = html;
    document.title = title;

    var navKey = parts[0] === "category" || parts[0] === "product" ? "browse" : parts[0];
    Array.prototype.forEach.call(document.querySelectorAll(".primary-nav .nav-link"), function (link) {
      var target = (link.getAttribute("href") || "").replace(/^#\//, "");
      if (target === navKey) link.setAttribute("aria-current", "page");
      else link.removeAttribute("aria-current");
    });

    if (parts[0] === "browse") mountBrowse(route.params);
    if (parts[0] === "compare") mountCompare();

    if (app) window.scrollTo(0, 0);
    return html;
  }

  function boot() {
    // Search forms live inside the re-rendered region, so delegate once.
    document.addEventListener("submit", function (event) {
      var form = event.target.closest ? event.target.closest("form[data-search]") : null;
      if (!form) return;
      event.preventDefault();
      var field = form.querySelector("input");
      var value = field ? field.value.trim() : "";
      window.location.hash = "#/browse" + (value ? "?q=" + encodeURIComponent(value) : "");
    });

    window.addEventListener("hashchange", render);
    render();
  }

  window.PaisaApp = { render: render, boot: boot };

  if (typeof document !== "undefined" && document.getElementById("app") && window.PAISA_DATA) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", boot);
    } else {
      boot();
    }
  }
})();
