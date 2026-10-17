#!/usr/bin/env python3
"""Produce PaisaClear.html — the entire site in one file.

Double-click it and it runs: no server, no install, no network. The CSS, the
product data and the renderer are all inlined.

    python bundle.py

The multi-page build in site/ is still the one to put on a domain later; this
single file is the "open it now" version.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from build import build_context  # noqa: E402

OUT = ROOT / "PaisaClear.html"
CSS = ROOT / "site" / "assets" / "css" / "styles.css"
APP_JS = ROOT / "spa" / "app.js"

FAVICON = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
    "%3Crect width='64' height='64' rx='14' fill='%230e6b4f'/%3E"
    "%3Cg fill='none' stroke='white' stroke-width='3.4' stroke-linecap='round'%3E"
    "%3Cpath d='M20 15h12a9 9 0 0 1 0 18H20V15Z'/%3E%3Cpath d='M20 33v17'/%3E"
    "%3Cpath d='M37 33l6 10'/%3E%3C/g%3E%3C/svg%3E"
)

# Tokens rather than str.format: the CSS and JS are full of braces.
SHELL = """<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PaisaClear — understand Indian financial products before you invest</title>
<meta name="description" content="Plain-language guides to government schemes, bank deposits, mutual funds, bonds and ETFs. A self-contained demonstration build.">
<meta name="color-scheme" content="light">
<link rel="icon" href="%%FAVICON%%">
<style>
%%CSS%%
</style>
</head>
<body>
<a class="skip-link" href="#app">Skip to content</a>

<header class="masthead">
  <div class="shell masthead-inner">
    <a class="brand" href="#/">
      <span class="brand-mark" aria-hidden="true">
        <svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
          <path d="M10 8h6.2a5 5 0 0 1 0 10H10V8Z"/><path d="M10 24V8"/><path d="M19.5 18l3.5 6"/>
        </svg>
      </span>
      <span class="brand-name">Paisa<span>Clear</span></span>
    </a>

    <nav class="primary-nav" aria-label="Primary">
      <a class="nav-link" href="#/browse">All products</a>
      <a class="nav-link" href="#/compare">Compare</a>
      <a class="nav-link" href="#/method">How we work</a>
    </nav>

    <form class="head-search" role="search" id="head-search">
      <label class="sr-only" for="head-q">Search products</label>
      <input id="head-q" type="search" placeholder="Search products" autocomplete="off">
      <button type="submit" aria-label="Search">
        <svg class="icon icon-sm" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 12h14M13 6.5l5.5 5.5-5.5 5.5"/></svg>
      </button>
    </form>
  </div>
</header>

<main id="app">
  <noscript>
    <div class="shell" style="padding-block:40px">
      <h1>PaisaClear</h1>
      <p>This build renders with JavaScript. The multi-page version in the <code>site/</code> folder
      works without it.</p>
    </div>
  </noscript>
</main>

<footer class="site-footer">
  <div class="shell footer-grid">
    <div class="footer-brand">
      <p class="footer-logo">Paisa<span>Clear</span></p>
      <p class="footer-note">
        A discovery and information site for Indian financial products, written for beginners.
        We do not sell products, take payments, or give personalised advice.
      </p>
    </div>
    <nav class="footer-col" aria-label="Categories">
      <h2>Categories</h2>
      <ul>
        %%CATEGORY_LINKS%%
      </ul>
    </nav>
    <nav class="footer-col" aria-label="Site">
      <h2>The site</h2>
      <ul>
        <li><a href="#/browse">All products</a></li>
        <li><a href="#/compare">Compare products</a></li>
        <li><a href="#/method">How we work</a></li>
        <li><a href="#/method">Editorial approval</a></li>
      </ul>
    </nav>
  </div>
  <div class="shell footer-legal">
    <p>
      <strong>Not financial advice.</strong> PaisaClear is an independent demonstration project. Every product on
      this site is fictional, created to show how a verified catalogue would work. Nothing here is an offer,
      a recommendation, or a statement about any real scheme, rate or guarantee. Always confirm details with the
      official provider and the regulator before acting.
    </p>
    <p class="footer-meta">Self-contained build · %%PRODUCT_COUNT%% products · Content reviewed by hand</p>
  </div>
</footer>

<script>
  // Header search and the "/" shortcut. Kept outside the app so they survive
  // route changes, which only replace #app.
  (function () {
    var form = document.getElementById("head-search");
    var field = document.getElementById("head-q");
    if (!form || !field) return;

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var value = field.value.trim();
      window.location.hash = "#/browse" + (value ? "?q=" + encodeURIComponent(value) : "");
    });

    document.addEventListener("keydown", function (event) {
      var tag = document.activeElement ? document.activeElement.tagName : "";
      if (event.key === "/" && !/^(INPUT|TEXTAREA|SELECT)$/.test(tag)) {
        event.preventDefault();
        field.focus();
        field.select();
      }
    });
  })();
</script>

<script>window.PAISA_DATA = %%DATA%%;</script>
<script>
%%APP_JS%%
</script>
</body>
</html>
"""


def main() -> int:
    ctx = build_context()
    products = ctx["products"]

    payload = {
        "site": {"name": "PaisaClear"},
        "categories": ctx["categories"],
        "returnTypes": ctx["return_types"],
        "collections": ctx["collections"],
        "products": products,
    }
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    category_links = "".join(
        f'<li><a href="#/category/{c["id"]}">{c["name"].replace("&", "&amp;")}</a></li>'
        for c in ctx["categories"]
    )

    html = (
        SHELL.replace("%%FAVICON%%", FAVICON)
        .replace("%%CSS%%", CSS.read_text(encoding="utf-8"))
        .replace("%%DATA%%", data)
        .replace("%%APP_JS%%", APP_JS.read_text(encoding="utf-8"))
        .replace("%%CATEGORY_LINKS%%", category_links)
        .replace("%%PRODUCT_COUNT%%", str(len(products)))
    )

    OUT.write_text(html, encoding="utf-8", newline="\n")
    size_kb = OUT.stat().st_size / 1024
    print("PaisaClear single file")
    print("-" * 46)
    print(f"  products inlined : {len(products):>3}")
    print(f"  categories       : {len(ctx['categories']):>3}")
    print(f"  file             : {OUT.name}  ({size_kb:.0f} KB)")
    print("-" * 46)
    print("  Open it directly in a browser — no server needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
