"""Shared page shell and presentational components for PaisaClear."""

from __future__ import annotations

import html
from datetime import datetime
from typing import Any

TONES = {
    "guaranteed": "green",
    "conditional": "amber",
    "market-linked": "violet",
}

CATEGORY_ACCENT = {
    "government-schemes": "green",
    "bank-deposits": "blue",
    "mutual-funds": "violet",
    "bonds": "amber",
    "etfs": "rose",
    "lic-life-insurance": "violet",
}

ICONS: dict[str, str] = {
    "shield": '<path d="M12 3 5 6v5.5c0 4.2 2.9 7.6 7 9.5 4.1-1.9 7-5.3 7-9.5V6l-7-3Z"/><path d="m9.2 12 2 2 3.6-3.8"/>',
    "bank": '<path d="M3.5 9.5 12 4l8.5 5.5"/><path d="M5.5 10.5v7M9.8 10.5v7M14.2 10.5v7M18.5 10.5v7"/><path d="M3.5 20.5h17M3 17.8h18"/>',
    "layers": '<path d="m12 3.5 8 4.2-8 4.2-8-4.2 8-4.2Z"/><path d="m4 12.2 8 4.2 8-4.2"/><path d="m4 16.4 8 4.2 8-4.2"/>',
    "certificate": '<rect x="3.5" y="4.5" width="17" height="12" rx="1.6"/><path d="M7 8.5h6M7 12h4"/><circle cx="17" cy="17.5" r="2.6"/><path d="m15.8 19.6-.6 2 1.8-1 1.8 1-.6-2"/>',
    "chart": '<path d="M4 19.5V4.5M4 19.5h16"/><path d="m7.5 15 3.4-4.4 3 2.4 3.4-5"/>',
    "calendar": '<rect x="3.8" y="5.4" width="16.4" height="14.6" rx="1.8"/><path d="M8 3.5v3.4M16 3.5v3.4M3.8 10h16.4"/><path d="M8.5 14h2M13.5 14h2M8.5 17h2M13.5 17h2"/>',
    "compass": '<circle cx="12" cy="12" r="8.4"/><path d="m15.2 8.8-2 4.4-4.4 2 2-4.4 4.4-2Z"/>',
    "seedling": '<path d="M12 20.5v-7.4"/><path d="M12 13.1C12 9.4 9.4 6.6 5.5 6.6c0 3.9 2.8 6.5 6.5 6.5Z"/><path d="M12 13.1c0-3 2.2-5.4 5.6-5.4 0 3.3-2.4 5.4-5.6 5.4Z"/><path d="M8.5 20.5h7"/>',
    "clock": '<circle cx="12" cy="12" r="8.4"/><path d="M12 7.4V12l3 1.9"/>',
    "receipt": '<path d="M6 3.6h12v16.8l-2.4-1.6-2.4 1.6-2.4-1.6-2.4 1.6L6 20.4Z"/><path d="M9 8.4h6M9 12.2h6"/>',
    "arrow": '<path d="M4.5 12h14M13 6.5l5.5 5.5-5.5 5.5"/>',
    "check": '<path d="m5 12.5 4.4 4.4L19 6.8"/>',
    "alert": '<path d="M12 4.2 21 19.8H3L12 4.2Z"/><path d="M12 10v4.2M12 17h.01"/>',
    "link": '<path d="M10.5 13.5a4 4 0 0 0 5.7 0l2.6-2.6a4 4 0 0 0-5.7-5.7L11.6 6.7"/><path d="M13.5 10.5a4 4 0 0 0-5.7 0L5.2 13a4 4 0 0 0 5.7 5.7l1.4-1.4"/>',
    "scale": '<path d="M12 4v16M7 20h10"/><path d="M4 8h16"/><path d="m7.5 8-2.8 5.4h5.6L7.5 8ZM16.5 8l-2.8 5.4h5.6L16.5 8Z"/>',
    "info": '<circle cx="12" cy="12" r="8.4"/><path d="M12 11v5.2M12 8h.01"/>',
    "umbrella": '<path d="M3.6 12a8.4 8.4 0 0 1 16.8 0Z"/><path d="M12 12v6.2a2.2 2.2 0 0 0 4.4 0"/><path d="M12 3.6V5"/>',
}


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def pretty_date(value: str | None) -> str:
    """2026-10-01 -> 1 Oct 2026."""
    if not value:
        return "—"
    try:
        return datetime.strptime(value, "%Y-%m-%d").strftime("%-d %b %Y")
    except ValueError:
        try:
            return datetime.strptime(value, "%Y-%m-%d").strftime("%d %b %Y").lstrip("0")
        except ValueError:
            return value


def rate_line(rate: dict | None) -> str:
    """Compact rate display used on product cards."""
    if not rate:
        return ""
    return (
        '<p class="pcard-rate">'
        f'<span class="rate-value">{esc(rate["value"])}</span>'
        f'<span class="rate-note">{esc(rate["label"])} · as of {esc(pretty_date(rate["asOf"]))}</span>'
        "</p>"
    )


def rate_ref_line(ref: dict | None) -> str:
    """For products whose figure genuinely varies by provider or tenure.

    Deliberately not a link: this sits inside the card's own <a>, and nesting
    anchors is invalid HTML. The product page carries the real source link.
    """
    if not ref:
        return ""
    return (
        '<p class="pcard-rate pcard-rate-ref">'
        f'<span class="rate-note">{esc(ref["label"])}</span>'
        '<span class="rate-link">Source on the detail page →</span>'
        "</p>"
    )


def icon(name: str, cls: str = "icon") -> str:
    path = ICONS.get(name, ICONS["info"])
    return (
        f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false" '
        f'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
        f'stroke-linejoin="round">{path}</svg>'
    )


def money(amount: Any) -> str:
    """Format an integer with Indian digit grouping: 100000 -> 1,00,000."""
    if amount is None:
        return "—"
    if isinstance(amount, str):
        return amount
    text = f"{int(amount):d}"
    if len(text) <= 3:
        return f"₹{text}"
    head, tail = text[:-3], text[-3:]
    groups = []
    while len(head) > 2:
        groups.insert(0, head[-2:])
        head = head[:-2]
    if head:
        groups.insert(0, head)
    return "₹" + ",".join(groups) + "," + tail


def min_investment_label(product: dict) -> str:
    label = money(product.get("minInvestment"))
    note = product.get("minInvestmentNote")
    return f"{label} <span class=\"fact-note\">{esc(note)}</span>" if note else label


def tone_for(return_type: str) -> str:
    return TONES.get(return_type, "green")


def chip(label: str, tone: str, cls: str = "chip") -> str:
    return f'<span class="{cls} chip-{tone}">{esc(label)}</span>'


def return_chip(product: dict, return_types: dict) -> str:
    rt = return_types[product["returnType"]]
    return chip(rt["label"], tone_for(product["returnType"]), "chip chip-return")


RISK_BAND_LABEL = {
    "low": "Low",
    "low-to-moderate": "Low to moderate",
    "moderate": "Moderate",
    "moderately-high": "Moderately high",
    "high": "High",
    "very-high": "Very high",
}

RISK_BAND_TONE = {
    "low": "blue",
    "low-to-moderate": "blue",
    "moderate": "amber",
    "moderately-high": "amber",
    "high": "rose",
    "very-high": "rose",
}


def risk_chip(product: dict) -> str:
    band = product.get("riskBand")
    if band:
        return chip(
            RISK_BAND_LABEL.get(band, band) + " risk",
            RISK_BAND_TONE.get(band, "amber"),
            "chip chip-risk",
        )
    level = product.get("riskLevel", "moderate")
    tone = {"low": "blue", "moderate": "amber", "high": "rose"}.get(level, "amber")
    return chip(level.capitalize() + " risk", tone, "chip chip-risk")


def fmt_pct(value) -> str:
    if value is None:
        return "—"
    return f"{value:+.2f}%"


def returns_line(product: dict) -> str:
    """Compact 1Y / 3Y / 5Y row for a product card."""
    returns = product.get("returns")
    if not returns:
        return ""
    cells = []
    for key, label in (("oneYear", "1Y"), ("threeYear", "3Y"), ("fiveYear", "5Y")):
        value = returns.get(key)
        cls = "ret-neg" if isinstance(value, (int, float)) and value < 0 else ""
        cells.append(
            f'<span class="ret {cls}"><span class="ret-k">{label}</span>{fmt_pct(value)}</span>'
        )
    return (
        '<p class="pcard-returns">' + "".join(cells)
        + '<span class="ret-note">CAGR from NAV</span></p>'
    )


def product_card(product: dict, base: str, return_types: dict, categories: dict) -> str:
    cat = categories[product["category"]]
    if product.get("rate"):
        figure = rate_line(product["rate"])
    elif product.get("rateRef"):
        figure = rate_ref_line(product["rateRef"])
    else:
        figure = ""
    return f"""<article class="pcard" data-slug="{esc(product['slug'])}"
  data-category="{esc(product['category'])}"
  data-return="{esc(product['returnType'])}"
  data-risk="{esc(product.get('riskLevel', ''))}"
  data-riskband="{esc(product.get('riskRank', ''))}"
  data-min="{esc(product.get('minInvestment') if isinstance(product.get('minInvestment'), int) else 0)}"
  data-payout="{esc((product.get('payoutFrequency') or '').lower())}"
  data-lockin="{'yes' if product.get('lockIn') else 'no'}"
  data-tax="{'yes' if 'tax-saving' in product.get('collections', []) else 'no'}"
  data-bucket="{esc(product.get('bucket', ''))}"
  data-name="{esc(product['name'].lower())}"
  data-text="{esc((product['name'] + ' ' + product['provider'] + ' ' + product.get('oneLiner', '')).lower())}">
  <a class="pcard-link" href="{base}products/{esc(product['slug'])}.html">
    <div class="pcard-badges">
      {return_chip(product, return_types)}
      {risk_chip(product)}
      <span class="pcard-cat">{esc(cat['short'])}</span>
    </div>
    <h3 class="pcard-name">{esc(product['name'])}</h3>
    <p class="pcard-provider">{esc(product['provider'])}</p>
    <p class="pcard-line">{esc(product.get('oneLiner', ''))}</p>
    {figure}
    {returns_line(product)}
    <dl class="pcard-facts">
      <div><dt>Minimum</dt><dd>{money(product.get('minInvestment')) if isinstance(product.get('minInvestment'), int) else ('Varies' if product.get('minInvestment') is None else esc(product.get('minInvestment')))}</dd></div>
      <div><dt>Tenure</dt><dd>{esc(product.get('tenure') or '—')}</dd></div>
      <div><dt>Payout</dt><dd>{esc(product.get('payout') or '—')}</dd></div>
    </dl>
    <span class="pcard-cta">Read the detail {icon("arrow", "icon icon-sm")}</span>
  </a>
</article>"""


def category_card(category: dict, count: int, base: str) -> str:
    accent = CATEGORY_ACCENT.get(category["id"], "green")
    is_guide = category.get("status") == "guide"
    if is_guide:
        foot = '<span class="cat-count cat-guide">Verify at source</span>'
    else:
        foot = f'<span class="cat-count">{count} product{"s" if count != 1 else ""}</span>'
    return f"""<a class="cat-card cat-{accent}" href="{base}categories/{esc(category['slug'])}.html">
  <span class="cat-icon">{icon(category['icon'])}</span>
  <span class="cat-name">{esc(category['name'])}</span>
  <span class="cat-tagline">{esc(category['tagline'])}</span>
  <span class="cat-foot">
    {foot}
    {icon("arrow", "icon icon-sm")}
  </span>
</a>"""


def breadcrumb(items: list[tuple[str, str]]) -> str:
    """items: (label, href-or-empty-for-current)."""
    parts = ['<nav class="crumbs" aria-label="Breadcrumb"><ol>']
    for label, href in items:
        if href:
            parts.append(f'<li><a href="{href}">{esc(label)}</a></li>')
        else:
            parts.append(f'<li aria-current="page">{esc(label)}</li>')
    parts.append("</ol></nav>")
    return "".join(parts)


def page(
    *,
    title: str,
    description: str,
    body: str,
    base: str = "",
    active: str = "",
    body_class: str = "",
    scripts: list[str] | None = None,
) -> str:
    def nav_link(href: str, label: str, key: str) -> str:
        current = ' aria-current="page"' if key == active else ""
        return f'<a class="nav-link" href="{base}{href}"{current}>{label}</a>'

    extra_scripts = "".join(
        f'<script src="{base}{esc(path)}" defer></script>\n' for path in (scripts or [])
    )

    return f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="color-scheme" content="light">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="PaisaClear">
<meta property="og:locale" content="en_IN">
<meta property="og:image" content="https://paisaclear.co.in/assets/img/og-default.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="https://paisaclear.co.in/assets/img/og-default.png">
<meta name="theme-color" content="#0f5132">
<!--CANONICAL-->
<link rel="icon" href="{base}assets/img/favicon-48.png" sizes="48x48" type="image/png">
<link rel="icon" href="{base}assets/img/favicon-96.png" sizes="96x96" type="image/png">
<link rel="icon" href="{base}assets/img/favicon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="{base}assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="{base}assets/css/styles.css">
<script src="{base}assets/js/site.js" defer></script>
</head>
<body class="{esc(body_class)}">
<a class="skip-link" href="#main">Skip to content</a>

<header class="masthead">
  <div class="shell masthead-inner">
    <a class="brand" href="{base}index.html">
      <span class="brand-mark" aria-hidden="true">
        <svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
          <path d="M10 8h6.2a5 5 0 0 1 0 10H10V8Z"/><path d="M10 24V8"/><path d="M19.5 18l3.5 6"/>
        </svg>
      </span>
      <span class="brand-name">Paisa<span>Clear</span></span>
    </a>

    <button class="nav-toggle" type="button" aria-controls="sidebar" aria-expanded="false">
      <span class="nav-toggle-bars" aria-hidden="true"></span>
      <span class="sr-only">Sections</span>
    </button>

    <nav class="primary-nav" aria-label="Primary">
      {nav_link("browse.html", "All products", "browse")}
      {nav_link("compare.html", "Compare", "compare")}
      {nav_link("how-we-work.html", "How we work", "method")}
    </nav>

    <form class="head-search" action="{base}browse.html" method="get" role="search">
      <label class="sr-only" for="head-q">Search products</label>
      <input id="head-q" type="search" name="q" placeholder="Search products" autocomplete="off">
      <button type="submit" aria-label="Search">{icon("arrow", "icon icon-sm")}</button>
    </form>
  </div>
</header>

<div class="layout">
<!--SIDEBAR-->
<main id="main">
{body}
</main>
</div>

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
        <li><a href="{base}categories/lic-life-insurance.html">LIC &amp; life insurance</a></li>
        <li><a href="{base}categories/government-schemes.html">Government &amp; Post Office</a></li>
        <li><a href="{base}categories/bank-deposits.html">Bank savings &amp; FDs</a></li>
        <li><a href="{base}categories/mutual-funds.html">Mutual funds</a></li>
        <li><a href="{base}categories/bonds.html">Bonds &amp; fixed income</a></li>
        <li><a href="{base}categories/etfs.html">ETFs &amp; market-linked</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="Site">
      <h2>The site</h2>
      <ul>
        <li><a href="{base}browse.html">All products</a></li>
        <li><a href="{base}compare.html">Compare products</a></li>
        <li><a href="{base}calculators/salary.html">Salary calculator</a></li>
        <li><a href="{base}calculators/savings.html">Savings calculator</a></li>
        <li><a href="{base}calculators/spending.html">Spending planner</a></li>
        <li><a href="{base}calculators/planning.html">Emergency & retirement</a></li>
        <li><a href="{base}calculators/loan.html">Loan EMI</a></li>
        <li><a href="{base}guides/ppf-vs-fd-vs-nsc.html">Guides</a></li>
        <li><a href="{base}privacy.html">Privacy</a></li>
        <li><a href="{base}feedback.html">Feedback</a></li>
        <li><a href="{base}how-we-work.html">How we work</a></li>
        <li><a href="{base}how-we-work.html#approval">Editorial approval</a></li>
      </ul>
    </nav>
  </div>
  <div class="shell footer-legal">
    <p>
      <strong>Not financial advice.</strong> PaisaClear is an independent information site. We do not sell products,
      take payments, or give personalised recommendations. Rates and rules change: every figure here carries the
      date it applied and a link to where it came from. Confirm with the official provider or regulator before acting.
    </p>
    <p class="footer-meta">Rates dated and sourced · Product records reviewed by hand</p>
  </div>
</footer>
{extra_scripts}<!--ANALYTICS--></body>
</html>"""
