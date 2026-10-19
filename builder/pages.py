"""Page bodies. Each function returns the HTML that goes inside <main>."""

from __future__ import annotations

from typing import Any

from .site import (
    CATEGORY_ACCENT,
    RISK_BAND_LABEL,
    breadcrumb,
    category_card,
    chip,
    esc,
    fmt_pct,
    icon,
    min_investment_label,
    money,
    pretty_date,
    product_card,
    return_chip,
    risk_chip,
    tone_for,
)

FEATURED_COLLECTIONS = ["monthly-income", "government-backed", "tax-saving"]


# --------------------------------------------------------------------- parts

def section_head(title: str, lede: str = "", link: tuple[str, str] | None = None) -> str:
    link_html = ""
    if link:
        label, href = link
        link_html = f'<a class="section-link" href="{href}">{esc(label)} {icon("arrow", "icon icon-sm")}</a>'
    lede_html = f'<p class="section-lede">{esc(lede)}</p>' if lede else ""
    return f"""<div class="section-head">
  <div><h2>{esc(title)}</h2>{lede_html}</div>
  {link_html}
</div>"""


def fact_row(label: str, value_html: str, *, icon_name: str = "") -> str:
    return (
        f'<div class="fact">'
        f'<dt>{esc(label)}</dt><dd>{value_html}</dd>'
        f"</div>"
    )


def check_list(items: list[str], cls: str = "check-list") -> str:
    lis = "".join(
        f'<li>{icon("check", "icon icon-sm")}<span>{esc(item)}</span></li>' for item in items
    )
    return f'<ul class="{cls}">{lis}</ul>'


def risk_list(items: list[str]) -> str:
    lis = "".join(
        f'<li>{icon("alert", "icon icon-sm")}<span>{esc(item)}</span></li>' for item in items
    )
    return f'<ul class="risk-list">{lis}</ul>'


def source_block(product: dict) -> str:
    """The exact page the record was built from, with the URL shown in full."""
    src = product.get("source")
    if not src or not src.get("url"):
        return ""
    display = src["url"].split("://", 1)[-1].rstrip("/")
    return f"""<div class="source-strip">
  <div class="source-strip-head">
    <span class="source-strip-label">Source</span>
    <a class="source-strip-link" href="{esc(src['url'])}" target="_blank" rel="noopener noreferrer">{esc(src['label'])} <span aria-hidden="true">↗</span></a>
  </div>
  <p class="source-strip-url">{esc(display)}</p>
  <p class="source-strip-note">{esc(src.get('note', ''))}</p>
</div>"""


def rate_panel(product: dict) -> str:
    rate = product.get("rate")
    if not rate:
        ref = product.get("rateRef")
        if not ref:
            return ""
        return f"""<div class="rate-panel rate-panel-ref">
  <div class="rate-main">
    <span class="rate-label-lg">{esc(ref["label"])}</span>
    <span class="rate-label">Not published as a number here — it varies by provider, tenure or plan.</span>
  </div>
  <div class="rate-meta">
    <p>{esc(ref.get("note", ""))}</p>
    <p><a class="btn btn-ghost" href="{esc(ref["url"])}" target="_blank" rel="noopener noreferrer">
      Check the official page {icon("arrow", "icon icon-sm")}</a></p>
  </div>
</div>"""
    via = ""
    if rate.get("confirmedVia"):
        via = (
            f' · confirmed via <a href="{esc(rate.get("confirmedViaUrl") or rate["sourceUrl"])}" '
            f'target="_blank" rel="noopener noreferrer">{esc(rate["confirmedVia"])}</a>'
        )
    return f"""<div class="rate-panel">
  <div class="rate-main">
    <span class="rate-value">{esc(rate["value"])}</span>
    <span class="rate-label">{esc(rate["label"])} · {esc(rate["cadence"])}</span>
  </div>
  <div class="rate-meta">
    <p>As of <strong>{esc(pretty_date(rate["asOf"]))}</strong>. Rates change — check the source before acting.</p>
    <p>Source: <a href="{esc(rate["sourceUrl"])}" target="_blank" rel="noopener noreferrer">{esc(rate["sourceLabel"])}</a>{via}</p>
  </div>
</div>"""


# --------------------------------------------------------------------- home

def home(ctx: dict) -> str:
    cats = ctx["categories"]
    cats_by_id = ctx["categories_by_id"]
    products = ctx["products"]
    counts = ctx["counts_by_category"]
    return_types = ctx["return_types_by_id"]

    cat_cards = "".join(category_card(c, counts.get(c["id"], 0), "") for c in cats)

    collection_blocks = []
    for cid in FEATURED_COLLECTIONS:
        collection = ctx["collections_by_id"][cid]
        members = [p for p in products if cid in p.get("collections", [])]
        if not members:
            continue
        cards = "".join(
            product_card(p, "", return_types, cats_by_id) for p in members[:4]
        )
        collection_blocks.append(f"""<div class="collection">
  <div class="collection-head">
    <span class="collection-icon">{icon(collection['icon'])}</span>
    <div>
      <h3>{esc(collection['title'])}</h3>
      <p>{esc(collection['blurb'])}</p>
    </div>
  </div>
  <div class="pcard-row">{cards}</div>
</div>""")

    return_cards = []
    for rt in ctx["return_types"]:
        asks = "".join(f"<li>{esc(a)}</li>" for a in rt["askYourself"])
        return_cards.append(f"""<article class="rt-card rt-{esc(rt['tone'])}">
  <p class="rt-label">{esc(rt['label'])}</p>
  <p class="rt-short">{esc(rt['short'])}</p>
  <p class="rt-def">{esc(rt['definition'])}</p>
  <div class="rt-ask">
    <p class="rt-ask-title">Ask yourself</p>
    <ul>{asks}</ul>
  </div>
  <a class="text-link" href="how-we-work.html#returns">Read the full explanation {icon("arrow", "icon icon-sm")}</a>
</article>""")

    total = len(products)
    return f"""
<section class="hero">
  <div class="shell">
    <p class="eyebrow">Indian financial products, explained without the sales pitch</p>
    <h1>Understand the <em>product</em><br>before you put money in it.</h1>
    <p class="hero-lede">
      Plain-language detail on how each option works, what it pays, when you can get your money back,
      and what can go wrong — with the official sources to check.
    </p>

    <form class="search-panel" action="browse.html" method="get" role="search">
      <span class="search-panel-icon">{icon("compass")}</span>
      <label class="sr-only" for="hero-q">Search financial products</label>
      <input id="hero-q" type="search" name="q" autocomplete="off"
             placeholder="Try “monthly income”, “tax saving”, “government”">
      <button class="btn btn-primary" type="submit">Search products</button>
    </form>
  </div>
</section>

<section class="section">
  <div class="shell">
    {section_head("Start with a category", "Different kinds of product, each with its own rules about what you are promised and what you can do with your money.", ("See all products", "browse.html"))}
    <div class="cat-grid">{cat_cards}</div>
  </div>
</section>

<section class="section section-tint">
  <div class="shell">
    {section_head("Ways in", "Collections that cut across categories — organised by what you might actually be trying to do.")}
    <div class="collections">{''.join(collection_blocks)}</div>
    <a class="more-link" href="browse.html">Browse all {total} products {icon("arrow", "icon icon-sm")}</a>
  </div>
</section>

<section class="section" id="returns">
  <div class="shell">
    {section_head("Guaranteed, conditional, market-linked", "Almost every product falls into one of these three buckets. Knowing which one you are looking at answers most of the important questions.", ("Full explanation", "how-we-work.html#returns"))}
    <div class="rt-grid">{''.join(return_cards)}</div>
  </div>
</section>

<section class="cta-band">
  <div class="shell cta-inner">
    <div>
      <h2>Comparing two or three options?</h2>
      <p>Put them side by side — minimum investment, tenure, payout, access to your money, risk and tax.</p>
    </div>
    <a class="btn btn-primary" href="compare.html">Open the comparison table {icon("arrow", "icon icon-sm")}</a>
  </div>
</section>
"""


# ------------------------------------------------------------------- browse

def browse(ctx: dict) -> str:
    products = ctx["products"]
    cats = ctx["categories"]
    return_types = ctx["return_types"]
    cats_by_id = ctx["categories_by_id"]
    rt_by_id = ctx["return_types_by_id"]

    cards = "".join(product_card(p, "", rt_by_id, cats_by_id) for p in products)

    cat_options = "".join(f'<option value="{esc(c["id"])}">{esc(c["name"])}</option>' for c in cats)
    rt_chips = "".join(
        f'<button class="filter-chip" type="button" data-return="{esc(rt["id"])}">{esc(rt["label"])}</button>'
        for rt in return_types
    )

    body = f"""
<section class="page-head">
  <div class="shell">
    {breadcrumb([("Home", "index.html"), ("All products", "")])}
    <h1>All products</h1>
    <p class="page-lede">
      {len(products)} products across all five categories. Each record names its provider and terms, and every
      figure is either dated and sourced or replaced with a link to the provider's own page where it genuinely
      varies — a bank's deposit rate being the clearest case.
    </p>
  </div>
</section>

<section class="shell">
  <div class="filter-bar" role="search">
    <div class="filter-search">
      <label class="sr-only" for="q">Search products</label>
      <input id="q" type="search" placeholder="Search by name, provider or feature" autocomplete="off">
    </div>

    <div class="filter-row">
      <label class="select-wrap">
        <span class="select-label">Category</span>
        <select id="filter-category">
          <option value="all">All categories</option>
          {cat_options}
        </select>
      </label>

      <label class="select-wrap">
        <span class="select-label">Sort</span>
        <select id="sort">
          <option value="default">Featured order</option>
          <option value="risk-asc">Risk: low to high</option>
          <option value="min-asc">Minimum investment: low to high</option>
          <option value="name">Name A–Z</option>
        </select>
      </label>
    </div>

    <div class="filter-returns" role="group" aria-label="Filter by return type">
      <span class="filter-label">What you are promised</span>
      <button class="filter-chip is-active" type="button" data-return="all">Any</button>
      {rt_chips}
    </div>

    <div class="filter-status">
      <p id="result-count" role="status" aria-live="polite">{len(products)} products</p>
      <button class="text-link" type="button" id="reset-filters" hidden>Reset filters</button>
    </div>
  </div>

  <div class="pcard-grid" id="results">{cards}</div>

  <div class="empty-state" id="no-results" hidden>
    <p class="empty-title">Nothing matches those filters.</p>
    <p>Try a broader search, or <button class="text-link" type="button" id="reset-empty">clear the filters</button>.</p>
  </div>
</section>
"""
    return body


# ----------------------------------------------------------------- category

def category_page(ctx: dict, category: dict) -> str:
    cats_by_id = ctx["categories_by_id"]
    rt_by_id = ctx["return_types_by_id"]
    members = [p for p in ctx["products"] if p["category"] == category["id"]]

    accent = CATEGORY_ACCENT.get(category["id"], "green")

    if category.get("status") == "guide":
        guide = category.get("guide", {})
        links = "".join(
            f'<li><a href="{esc(link["url"])}" target="_blank" rel="noopener noreferrer">{esc(link["label"])}'
            f'<span class="ext" aria-hidden="true">↗</span></a></li>'
            for link in guide.get("links", [])
        )
        checks = "".join(
            f"<li>{icon('check', 'icon icon-sm')}<span>{esc(item)}</span></li>"
            for item in category["whatToCheck"]
        )
        verify = "".join(
            f'<li><a href="{esc(item["url"])}" target="_blank" rel="noopener noreferrer">{esc(item["label"])}'
            f'<span class="ext" aria-hidden="true">↗</span></a>'
            f'<span class="verify-note">{esc(item["note"])}</span></li>'
            for item in guide.get("verify", [])
        )
        verify_block = (
            f'<div class="verify-block"><p class="verify-title">Where to verify, before you act</p>'
            f'<ul class="verify-list">{verify}</ul></div>'
            if verify else ""
        )
        others = "".join(
            f'<a class="pill-link" href="{esc(c["slug"])}.html">{esc(c["short"])}</a>'
            for c in ctx["categories"] if c["id"] != category["id"]
        )
        return f"""
<section class="page-head page-head-cat cat-{accent}">
  <div class="shell">
    {breadcrumb([("Home", "../index.html"), ("All products", "../browse.html"), (category["name"], "")])}
    <span class="page-icon">{icon(category["icon"])}</span>
    <h1>{esc(category["name"])}</h1>
    <p class="page-lede">{esc(category["blurb"])}</p>
    <p class="page-meta">Guide · no product records published yet</p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="split">
      <div class="split-main">
        <div class="guide-panel">
          <p class="guide-kicker">Why there are no products listed here</p>
          <p class="guide-reason">{esc(guide.get("reason", ""))}</p>
          <p class="guide-instead">{esc(guide.get("instead", ""))}</p>
          <ul class="source-links">{links}</ul>
          {verify_block}
        </div>

        <h2 class="subhead" style="margin-top:34px">What to check, whichever provider you use</h2>
        <ul class="check-list">{checks}</ul>

        <p class="muted" style="margin-top:22px">
          The two live categories — <a href="government-schemes.html">government schemes</a> and
          <a href="bonds.html">government bonds</a> — carry full product records with dated, sourced rates.
        </p>
      </div>

      <aside class="split-aside">
        <div class="aside-card">
          <h2>Other categories</h2>
          <div class="pill-links">{others}</div>
        </div>
      </aside>
    </div>
  </div>
</section>
"""

    cards = "".join(product_card(p, "../", rt_by_id, cats_by_id) for p in members)

    breakdown: dict[str, int] = {}
    for p in members:
        breakdown[p["returnType"]] = breakdown.get(p["returnType"], 0) + 1
    mix = " · ".join(
        f"{breakdown[rt]} {rt_by_id[rt]['label'].lower()}" for rt in breakdown
    )

    checks = "".join(f"<li>{icon('check', 'icon icon-sm')}<span>{esc(item)}</span></li>" for item in category["whatToCheck"])

    others = [c for c in ctx["categories"] if c["id"] != category["id"]]
    other_links = "".join(
        f'<a class="pill-link" href="{esc(c["slug"])}.html">{esc(c["short"])}</a>' for c in others
    )

    return f"""
<section class="page-head page-head-cat cat-{accent}">
  <div class="shell">
    {breadcrumb([("Home", "../index.html"), ("All products", "../browse.html"), (category["name"], "")])}
    <span class="page-icon">{icon(category["icon"])}</span>
    <h1>{esc(category["name"])}</h1>
    <p class="page-lede">{esc(category["blurb"])}</p>
    <p class="page-meta">{len(members)} products · {esc(mix)}</p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="split">
      <div class="split-main">
        <h2 class="subhead">Products in this category</h2>
        <div class="pcard-grid">{cards}</div>
      </div>

      <aside class="split-aside">
        <div class="aside-card">
          <h2>What to check first</h2>
          <ul class="check-list">{checks}</ul>
        </div>
        <div class="aside-card">
          <h2>Other categories</h2>
          <div class="pill-links">{other_links}</div>
        </div>
      </aside>
    </div>
  </div>
</section>
"""


# ------------------------------------------------------------------ product

def returns_block(product: dict) -> str:
    returns = product.get("returns")
    if not returns:
        return ""
    cells = []
    for key, label in (("oneYear", "1 year"), ("threeYear", "3 years"), ("fiveYear", "5 years")):
        value = returns.get(key)
        cls = "ret-v ret-neg" if isinstance(value, (int, float)) and value < 0 else "ret-v"
        cells.append(
            f'<div class="ret-cell"><span class="ret-k">{label}</span>'
            f'<span class="{cls}">{fmt_pct(value)}</span></div>'
        )
    return f"""<section class="prose-block">
          <h2>Returns, from its own NAV</h2>
          <div class="returns-grid">{"".join(cells)}</div>
          <p class="muted">
            Annualised (CAGR) figures computed by PaisaClear from AMFI NAV data as on
            {esc(pretty_date(returns.get("asOf")))}. They are not a fund-house or SEBI figure, they ignore
            exit loads and tax, and past performance does not indicate future returns.
          </p>
        </section>

        """


def product_page(ctx: dict, product: dict) -> str:
    cats_by_id = ctx["categories_by_id"]
    rt_by_id = ctx["return_types_by_id"]
    category = cats_by_id[product["category"]]
    rt = rt_by_id[product["returnType"]]

    related = [
        p for p in ctx["products"]
        if p["category"] == product["category"] and p["slug"] != product["slug"]
    ][:3]
    related_cards = "".join(product_card(p, "../", rt_by_id, cats_by_id) for p in related)

    sources = "".join(
        f'<li><a href="{esc(s["url"])}" rel="noopener noreferrer" target="_blank">{esc(s["label"])}'
        f'<span class="ext" aria-hidden="true">↗</span></a></li>'
        for s in product["sources"]
    )

    uses = "".join(f"<li>{esc(u)}</li>" for u in product.get("commonUses", []))

    glance = "".join([
        fact_row("Return type", f'{chip(rt["label"], tone_for(product["returnType"]), "chip chip-return")} <span class="fact-note">{esc(rt["short"])}</span>'),
        fact_row("Rate", f'{esc(product["rate"]["value"])} <span class="fact-note">as of {esc(pretty_date(product["rate"]["asOf"]))}</span>') if product.get("rate") else "",
        fact_row("Provider", esc(product["provider"])),
        fact_row("Minimum", min_investment_label(product)),
        fact_row("Tenure", esc(product["tenure"])),
        fact_row("Payout", esc(product["payout"])),
        fact_row("Lock-in", esc(product.get("lockIn") or "None")),
        fact_row("Risk", risk_chip(product)),
        fact_row("Last verified", esc(product["lastVerified"])),
    ])

    review = product.get("review", {})

    return f"""
<section class="product-head">
  <div class="shell">
    {breadcrumb([("Home", "../index.html"), (category["short"], f"../categories/{category['slug']}.html"), (product["name"], "")])}

    <div class="product-head-inner">
      <div class="product-title">
        <div class="badge-row">
          {return_chip(product, rt_by_id)}
          {risk_chip(product)}
          <span class="chip chip-neutral">Verified record</span>
        </div>
        <h1>{esc(product["name"])}</h1>
        <p class="product-provider">{esc(product["provider"])} · {esc(category["name"])}</p>
        <p class="product-oneliner">{esc(product["oneLiner"])}</p>
      </div>
    </div>
  </div>
</section>

<div class="shell">
  {rate_panel(product)}
  {source_block(product)}
</div>

<section class="section product-body">
  <div class="shell">
    <div class="split">
      <div class="split-main">

        <section class="prose-block">
          <h2>How it works</h2>
          <p>
            {esc(product["name"])} is a {esc(category["short"].lower())} product from {esc(product["provider"])},
            in the <strong>{esc(rt["label"].lower())}</strong> category: {esc(rt["short"].lower())}.
            {esc(product["oneLiner"])}
          </p>
          <p class="muted">
            Because the return type is {esc(rt["label"].lower())}, the questions that matter most are:
            {esc(rt["askYourself"][0])} {esc(rt["askYourself"][1])}
          </p>
          <ul class="uses">{uses}</ul>
        </section>

        {returns_block(product)}

        <section class="prose-block">
          <h2>Key facts</h2>
          <div class="fact-table">
            {fact_row("Provider", esc(product["provider"]))}
            {fact_row("UIN", esc(product["uin"])) if product.get("uin") else ""}
            {fact_row("Risk band", esc(RISK_BAND_LABEL.get(product.get("riskBand", ""), "")) + f' <span class="fact-note">PaisaClear classification by scheme category, not the SEBI riskometer</span>') if product.get("riskBand") else ""}
            {fact_row("Source", f'<a href="{esc(product["source"]["url"])}" target="_blank" rel="noopener noreferrer">{esc(product["source"]["label"])} ↗</a> <span class="fact-note">{esc(product["source"]["url"])}</span>') if product.get("source") else ""}
            {fact_row("Rate", f'{esc(product["rate"]["value"])} <span class="fact-note">{esc(product["rate"]["label"])}, as of {esc(pretty_date(product["rate"]["asOf"]))}</span>') if product.get("rate") else (fact_row("Rate", f'<a href="{esc(product["rateRef"]["url"])}" target="_blank" rel="noopener noreferrer">{esc(product["rateRef"]["label"])} ↗</a>') if product.get("rateRef") else "")}
            {fact_row("Category", f'<a href="../categories/{category["slug"]}.html">{esc(category["name"])}</a>')}
            {fact_row("Minimum investment", min_investment_label(product))}
            {fact_row("Tenure", esc(product["tenure"]))}
            {fact_row("Payout", esc(product["payout"]))}
            {fact_row("Eligibility", esc(product["eligibility"]))}
            {fact_row("Getting your money back", esc(product["liquidity"]))}
            {fact_row("Protection", esc(product["protection"]))}
            {fact_row("Tax", esc(product["tax"]))}
          </div>
        </section>

        <section class="prose-block">
          <h2>What can go wrong</h2>
          {risk_list(product["risks"])}
        </section>

        <section class="prose-block">
          <h2>Before you decide anything</h2>
          {check_list(product["check"])}
          <p class="muted">
            These are questions to take to the provider, not a checklist that makes a product suitable.
            Whether something fits your situation is a decision only you — or an adviser you choose — can make.
          </p>
        </section>

        <section class="prose-block">
          <h2>Official sources</h2>
          <ul class="source-links">{sources}</ul>
          <p class="muted">
            These link to the regulator or provider where the rules for this <em>type</em> of product are set out.
            They are the pages worth checking before you act, because they are the ones that get updated.
          </p>
        </section>

      </div>

      <aside class="split-aside">
        <div class="aside-card aside-glance">
          <h2>At a glance</h2>
          <div class="fact-table fact-table-tight">{glance}</div>
          <a class="btn btn-primary btn-block" href="../compare.html?p={esc(product['slug'])}">
            Compare this product {icon("scale", "icon icon-sm")}
          </a>
        </div>

        <div class="aside-card">
          <h2>Verification</h2>
          <p class="aside-note">
            Last checked <strong>{esc(product["lastVerified"])}</strong>.
            Approved for publication by {esc(review.get("reviewer") or "an editor")}.
          </p>
          <p class="aside-note">
            Status: <span class="status status-approved">Approved</span>
          </p>
        </div>
      </aside>
    </div>
  </div>
</section>

{_related_section(related_cards) if related_cards else ""}
"""


def _related_section(cards: str) -> str:
    return f"""
<section class="section section-tint">
  <div class="shell">
    {section_head("Other products in this category", "The same rules and the same kind of trade-offs, described the same way.")}
    <div class="pcard-grid">{cards}</div>
  </div>
</section>"""


# ------------------------------------------------------------------ compare

def compare(ctx: dict, catalog_json: str) -> str:
    products = ctx["products"]
    options = "".join(
        f'<option value="{esc(p["slug"])}">{esc(p["name"])} — {esc(p["providerShort"])}</option>'
        for p in products
    )

    slots = "".join(
        f"""<div class="slot" data-slot="{i}">
  <label class="slot-label" for="slot-{i}">Product {i + 1}</label>
  <select class="slot-select" id="slot-{i}" data-slot="{i}">
    <option value="">Choose a product…</option>
    {options}
  </select>
  <button class="slot-clear" type="button" data-clear="{i}" hidden>Remove</button>
</div>"""
        for i in range(3)
    )

    return f"""
<section class="page-head">
  <div class="shell">
    {breadcrumb([("Home", "index.html"), ("Compare", "")])}
    <h1>Compare up to three products</h1>
    <p class="page-lede">
      Side by side on the things that are comparable: what you are promised, how long your money is held,
      how you get it back, and where the risks sit. Prices and rates are deliberately not shown — the demo
      data does not invent them.
    </p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="compare-slots">{slots}</div>

    <p class="compare-hint" id="compare-hint">
      Pick a product in any slot. You can also add a product straight from its page.
    </p>

    <div class="compare-wrap" id="compare-wrap" hidden>
      <table class="compare-table" id="compare-table">
        <caption class="sr-only">Comparison of selected financial products</caption>
        <thead id="compare-head"></thead>
        <tbody id="compare-body"></tbody>
      </table>
    </div>

    <noscript>
      <p class="notice notice-static">Choosing and comparing products needs JavaScript. Every product is also
      listed on the <a href="browse.html">all products</a> page.</p>
    </noscript>

    <div class="compare-notes">
      <h2>How to read this</h2>
      <ul class="check-list">
        <li>{icon("check", "icon icon-sm")}<span><strong>Return type</strong> matters more than any headline number: guaranteed, conditional and market-linked products fail in different ways.</span></li>
        <li>{icon("check", "icon icon-sm")}<span><strong>Lock-in</strong> is the real cost of a higher rate. Check what happens if life changes in year two.</span></li>
        <li>{icon("check", "icon icon-sm")}<span><strong>No rates are shown.</strong> Inventing an illustrative rate would make an unverifiable comparison look precise.</span></li>
        <li>{icon("check", "icon icon-sm")}<span><strong>Nothing here is a recommendation.</strong> A product that ranks well on one row can be wrong for your situation.</span></li>
      </ul>
    </div>
  </div>
</section>

<script type="application/json" id="catalog">{catalog_json}</script>
<script src="assets/js/compare.js" defer></script>
"""


# ------------------------------------------------------------------- method

def method(ctx: dict) -> str:
    rt_sections = []
    for rt in ctx["return_types"]:
        asks = "".join(f"<li>{esc(a)}</li>" for a in rt["askYourself"])
        rt_sections.append(f"""<article class="method-rt rt-{esc(rt['tone'])}" id="rt-{esc(rt['id'])}">
  <div class="method-rt-head">
    <span class="rt-dot" aria-hidden="true"></span>
    <h3>{esc(rt['label'])}</h3>
    <span class="rt-tag">{esc(rt['short'])}</span>
  </div>
  <p>{esc(rt['definition'])}</p>
  <p>{esc(rt['detail'])}</p>
  <div class="rt-ask">
    <p class="rt-ask-title">Ask yourself</p>
    <ul>{asks}</ul>
  </div>
</article>""")

    return f"""
<section class="page-head">
  <div class="shell">
    {breadcrumb([("Home", "index.html"), ("How we work", "")])}
    <h1>How this catalogue works</h1>
    <p class="page-lede">
      PaisaClear exists to explain financial products clearly, not to sell them. This page sets out what we
      publish, how a product gets approved, and what we deliberately do not do.
    </p>
  </div>
</section>

<section class="section">
  <div class="shell shell-narrow">
    <div class="prose">
      <h2>Where the numbers come from</h2>
      <p>
        All five categories carry product records. Government schemes and government securities show a rate with
        the date it applied and a link to where it came from — small-savings rates are notified each quarter,
        while bond yields are pulled from the RBI by a refresh job.
      </p>
      <p>
        Mutual funds and ETFs show the published NAV from AMFI's daily file. Bank deposits are the exception: the
        rate depends on the bank, the tenure and the deposit slab, so each entry links straight to that bank's own
        rate card rather than quoting a number that would be wrong for most readers.
      </p>

      <h2>What we do</h2>
      <ul class="check-list">
        <li>{icon("check", "icon icon-sm")}<span>Describe how a product works, in the same fields for every entry.</span></li>
        <li>{icon("check", "icon icon-sm")}<span>Show the trade-offs plainly: lock-in, access, tax, and what can go wrong.</span></li>
        <li>{icon("check", "icon icon-sm")}<span>Link to the regulator or provider where the actual rules live.</span></li>
        <li>{icon("check", "icon icon-sm")}<span>Date every page, because rates and rules change.</span></li>
      </ul>

      <h2>What we do not do</h2>
      <ul class="cross-list">
        <li>{icon("alert", "icon icon-sm")}<span>We do not recommend products, or say what you should buy or sell.</span></li>
        <li>{icon("alert", "icon icon-sm")}<span>We do not ask for money, take payments, or offer subscriptions.</span></li>
        <li>{icon("alert", "icon icon-sm")}<span>We do not quote rates we cannot verify from a primary source.</span></li>
        <li>{icon("alert", "icon icon-sm")}<span>We do not ask for your personal or financial details.</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="section section-tint" id="returns">
  <div class="shell">
    {section_head("The three return types", "Every product is filed under one of these. It is the single most useful thing to establish before reading further.")}
    <div class="method-rt-grid">{''.join(rt_sections)}</div>
  </div>
</section>

<section class="section" id="approval">
  <div class="shell shell-narrow">
    <div class="prose">
      <h2>How a product gets published</h2>
      <p>
        Products are never written straight into the website. They move through a small, deliberate pipeline,
        and each stage is visible in the content files.
      </p>
    </div>

    <ol class="pipeline">
      <li>
        <span class="step-no">1</span>
        <div>
          <strong>Research</strong>
          <p>A product record is drafted with its provider, terms, eligibility, tax position and risks, plus at least one source link.</p>
          <span class="status status-draft">draft</span>
        </div>
      </li>
      <li>
        <span class="step-no">2</span>
        <div>
          <strong>Check</strong>
          <p>A second person verifies each field against the source, and confirms no rate or guarantee is stated without one. The record is marked pending.</p>
          <span class="status status-pending">pending</span>
        </div>
      </li>
      <li>
        <span class="step-no">3</span>
        <div>
          <strong>Approve</strong>
          <p>An editor signs off, and the record carries the reviewer's name and the approval date. Only then can it be built into the site.</p>
          <span class="status status-approved">approved</span>
        </div>
      </li>
      <li>
        <span class="step-no">4</span>
        <div>
          <strong>Publish</strong>
          <p>The build reads only approved records. Anything in draft, pending or rejected is skipped — it cannot leak onto a page by accident.</p>
          <span class="status status-live">live</span>
        </div>
      </li>
    </ol>

    <div class="prose">
      <h2 id="sources">Sources and verification</h2>
      <p>
        Each product lists the regulator or provider where its rules are set out — the RBI, SEBI, PFRDA, the
        Income Tax Department, NSE, AMFI and similar bodies. The link is to the authoritative page for that
        <em>kind</em> of product, because that is the page that is updated when a rule or rate changes.
      </p>
      <p>
        Every entry carries a <strong>last verified</strong> date. If a page is more than six months old, treat
        its terms as possibly out of date and check the source.
      </p>

      <h2>Corrections</h2>
      <p>
        If a field is wrong, the record is corrected and the verification date updated. We would rather remove
        an entry than leave a claim we cannot stand behind.
      </p>
    </div>
  </div>
</section>
"""


# ---------------------------------------------------------------- not found

def not_found(ctx: dict) -> str:
    return """
<section class="page-head">
  <div class="shell">
    <h1>That page isn’t here</h1>
    <p class="page-lede">The link may be old, or the product may have been removed from the catalogue.</p>
    <p style="margin-top:22px">
      <a class="btn btn-primary" href="index.html">Back to the homepage</a>
      <a class="btn btn-ghost" href="browse.html">Browse all products</a>
    </p>
  </div>
</section>
"""
