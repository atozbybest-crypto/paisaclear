#!/usr/bin/env python3
"""Build the PaisaClear static site from the content files.

Only records whose review status is "approved" are ever rendered. Everything
else is counted and reported, so a draft cannot reach a page by accident.

    python build.py

Exit codes: 0 built, 1 validation failed.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from builder import (answers, articles, articles2, articles_extra1, articles_extra2, articles_extra3, articles_extra4,
                     articles_long1, bbbp, calculator, calc_notes, checker, dividends, editorial, extra_guides, game, guide_notes, health, finder, guides, income_tax, legal, loan, news, pages, plan_schemes, plans, plan, planner, privacy, ssy, start, us_funds, us_market, articles_us)  # noqa: E402
import builder.site as site_mod  # noqa: E402
from builder.site import ICONS, page  # noqa: E402

CONTENT = ROOT / "content"
SITE = ROOT / "site"

REQUIRED_FIELDS = [
    "slug", "name", "provider", "providerShort", "providerType", "category",
    "returnType", "oneLiner", "minInvestment", "tenure", "payout", "eligibility",
    "tax", "protection", "riskLevel", "risks", "commonUses", "check",
    "collections", "sources", "lastVerified", "review",
]
VALID_STATUSES = {"draft", "pending", "approved", "rejected"}
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def validate(
    products: list[dict],
    categories: dict,
    return_types: dict,
    collections: dict,
    rates: dict,
) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    rate_values = rates.get("values", {})

    for index, product in enumerate(products):
        slug = product.get("slug") or f"#{index}"
        for field in REQUIRED_FIELDS:
            if field == "minInvestment":
                continue  # validated separately: a null is allowed with a note
            if field not in product or product[field] in (None, "", []):
                errors.append(f"{slug}: missing required field '{field}'")

        if not SLUG_RE.match(str(product.get("slug", ""))):
            errors.append(f"{slug}: slug must be lower-case words separated by hyphens")
        if slug in seen:
            errors.append(f"{slug}: duplicate slug")
        seen.add(slug)

        if product.get("category") not in categories:
            errors.append(f"{slug}: unknown category '{product.get('category')}'")
        if product.get("returnType") not in return_types:
            errors.append(f"{slug}: unknown return type '{product.get('returnType')}'")
        if product.get("riskLevel") not in {"low", "moderate", "high"}:
            errors.append(f"{slug}: riskLevel must be low, moderate or high")

        rate_key = product.get("rateKey")
        if rate_key and rate_key not in rate_values:
            errors.append(f"{slug}: rateKey '{rate_key}' is not in rates.json")
        rate_ref = product.get("rateRef") or {}
        if rate_ref and not str(rate_ref.get("url", "")).startswith("http"):
            errors.append(f"{slug}: rateRef needs an http url")
        if product.get("review", {}).get("status") == "approved" and not rate_key and not rate_ref:
            errors.append(f"{slug}: approved products need a rateKey or a rateRef link")

        for collection in product.get("collections", []):
            if collection not in collections:
                errors.append(f"{slug}: unknown collection '{collection}'")

        if product.get("minInvestment") is None:
            # Insurance premiums depend on age, term and sum assured; a null is
            # acceptable only when the record explains why.
            if not product.get("minInvestmentNote"):
                errors.append(f"{slug}: minInvestment is null without a note explaining it")
        elif not isinstance(product.get("minInvestment"), (int, float)):
            errors.append(f"{slug}: minInvestment must be a number or null")

        for source in product.get("sources", []):
            if not str(source.get("url", "")).startswith("http"):
                errors.append(f"{slug}: source url must start with http")

        review = product.get("review") or {}
        status = review.get("status")
        if status not in VALID_STATUSES:
            errors.append(f"{slug}: review.status '{status}' is not one of {sorted(VALID_STATUSES)}")
        if status == "approved" and not review.get("approvedAt"):
            errors.append(f"{slug}: approved records need review.approvedAt")
        if status == "approved" and not review.get("reviewer"):
            errors.append(f"{slug}: approved records need review.reviewer")

    return errors


def build_context() -> dict:
    categories = load_json(CONTENT / "categories.json")
    return_types = load_json(CONTENT / "return-types.json")
    collections = load_json(CONTENT / "collections.json")
    products = load_json(CONTENT / "products.json")
    rates = load_json(CONTENT / "rates.json")

    categories_by_id = {c["id"]: c for c in categories}
    return_types_by_id = {r["id"]: r for r in return_types}

    errors = validate(
        products,
        categories_by_id,
        return_types_by_id,
        {c["id"]: c for c in collections},
        rates,
    )
    if errors:
        print("Content validation failed:\n", file=sys.stderr)
        for error in errors:
            print(f"  ✗ {error}", file=sys.stderr)
        raise SystemExit(1)

    status_counts: dict[str, int] = {}
    for product in products:
        status = product["review"]["status"]
        status_counts[status] = status_counts.get(status, 0) + 1

    approved = [p for p in products if p["review"]["status"] == "approved"]
    approved.sort(key=lambda p: (p["category"], p["name"]))

    # Attach the current rate so templates never reach into rates.json themselves.
    for product in approved:
        key = product.get("rateKey")
        if key:
            product["rate"] = rates["values"][key]

    counts_by_category: dict[str, int] = {}
    for product in approved:
        counts_by_category[product["category"]] = counts_by_category.get(product["category"], 0) + 1

    return {
        "categories": categories,
        "categories_by_id": categories_by_id,
        "return_types": return_types,
        "return_types_by_id": return_types_by_id,
        "collections": collections,
        "collections_by_id": {c["id"]: c for c in collections},
        "products": approved,
        "counts_by_category": counts_by_category,
        "status_counts": status_counts,
        "all_products": products,
        "rates": rates,
    }


def catalog_json(products: list[dict]) -> str:
    """Compact record set for the comparison page, embedded so no fetch is needed."""
    slim = [
        {
            "slug": p["slug"],
            "name": p["name"],
            "provider": p["provider"],
            "providerShort": p["providerShort"],
            "category": p["category"],
            "returnType": p["returnType"],
            "riskLevel": p["riskLevel"],
            "minInvestment": p["minInvestment"],
            "tenure": p["tenure"],
            "payout": p["payout"],
            "lockIn": p.get("lockIn") or "None",
            "liquidity": p["liquidity"],
            "eligibility": p["eligibility"],
            "tax": p["tax"],
            "protection": p["protection"],
            "lastVerified": p["lastVerified"],
            "rate": p.get("rate"),
            "rateRef": p.get("rateRef"),
        }
        for p in products
    ]
    return json.dumps(slim, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def _product_description(product: dict, ctx: dict) -> str:
    """Unique, specific description — never the same sentence twice."""
    cat = next((c for c in ctx["categories"] if c["id"] == product["category"]), None)
    cat_name = cat["name"] if cat else "financial product"
    bits = [f"{product['name']} from {product.get('provider', 'the provider')}.",
            product.get("oneLiner", "").rstrip(".") + "."]
    returns = (product.get("returns") or {}).get("threeYear")
    if returns is not None:
        bits.append(f"Three-year return {returns}% from NAV history.")
    if product.get("minInvestment"):
        bits.append(f"Minimum {product['minInvestment']}.")
    if product.get("lockIn"):
        bits.append(f"Lock-in {product['lockIn']}.")
    bits.append(f"Listed under {cat_name}; every figure carries the date it applied.")
    return " ".join(b for b in bits if b)[:300]


def _article_body(html: str, extra: str) -> str:
    """Append the long-form sections just before the closing source note."""
    if not extra:
        return html
    anchor = '    <p class="guide-src">'
    return html.replace(anchor, extra + anchor, 1)


def main() -> int:
    ctx = build_context()
    products = ctx["products"]
    status_counts = ctx["status_counts"]

    # Clean generated pages so a record that loses approval cannot linger.
    for folder in ("products", "categories"):
        target = SITE / folder
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True, exist_ok=True)

    written: list[str] = []

    # Hash the CSS/JS once per build so their URLs can be cached forever.
    import hashlib
    _digest = hashlib.sha1()
    for _asset in sorted((SITE / 'assets/css').glob('*.css')) + sorted((SITE / 'assets/js').glob('*.js')):
        _digest.update(_asset.read_bytes())
    site_mod.ASSET_VERSION = _digest.hexdigest()[:8]

    def sidebar_for(rel: str) -> str:
        base = "../" if "/" in rel else ""
        current = rel

        def link(href: str, label: str, count: str = "") -> str:
            active = ' aria-current="page"' if current == href else ""
            badge = f'<span class="side-count">{count}</span>' if count else ""
            return f'<a class="side-link" href="{base}{href}"{active}><span>{label}</span>{badge}</a>'

        def group(title: str, body: str, member_prefixes: tuple) -> str:
            open_attr = " open" if any(current.startswith(pref) for pref in member_prefixes) else ""
            return (
                f'<details class="side-group"{open_attr}>'
                f'<summary class="side-summary"><span>{title}</span>'
                '<svg class="side-chev" viewBox="0 0 12 12" aria-hidden="true">'
                '<path d="M3 4.5 6 7.5 9 4.5" fill="none" stroke="currentColor" '
                'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
                '</summary><div class="side-items">' + body + "</div></details>"
            )

        cat_links = "".join(
            link(f"categories/{c['slug']}.html", c["name"], str(ctx["counts_by_category"].get(c["id"], 0)))
            for c in ctx["categories"]
        )

        groups = (
            '<div class="side-home">'
            + link("start.html", "Dashboard")
            + "</div>"
            + group("Browse", link("browse.html", "All products", str(len(products))) + link("compare.html", "Compare"),
                    ("browse.html", "compare.html", "products/"))
            + group("Categories", cat_links, ("categories/", "products/"))
            + group("Guides",
                    link("rates.html", "Today's rates")
                    + link("guides/ppf-vs-fd-vs-nsc.html", "PPF vs FD vs NSC")
                    + link("guides/sip-vs-lump-sum.html", "SIP vs lump sum")
                    + link("guides/old-vs-new-tax-regime.html", "Old vs new tax regime")
                    + link("guides/small-savings-compared.html", "Small savings compared")
                    + link("plans.html", "All plans")
                    + link("guides/ssy-vs-ppf.html", "SSY vs PPF")
                    + link("guides/scss-vs-fd.html", "SCSS vs FD")
                    + link("guides/sip-vs-fd.html", "SIP vs FD")
                    + link("guides/nps-vs-ppf.html", "NPS vs PPF"),
                    ("guides/",))
            + group("Plans <span class=\"badge-new\">New</span>",
                    link("plans.html", "All plans")
                    + link("plans/sukanya-samriddhi.html", "Sukanya Samriddhi")
                    + link("plans/beti-bachao-beti-padhao.html", "Beti Bachao Beti Padhao")
                    + link("plans/public-provident-fund.html", "Public Provident Fund")
                    + link("plans/national-savings-certificate.html", "National Savings Certificate")
                    + link("plans/senior-citizens-savings-scheme.html", "Senior Citizens' Savings")
                    + link("plans/kisan-vikas-patra.html", "Kisan Vikas Patra")
                    + link("plans/post-office-monthly-income-scheme.html", "Post Office MIS"),
                    ("plans/", "plans.html"))
            + group("Calculators",
                    link("calculators/salary.html", "Salary and take-home")
                    + link("calculators/savings.html", "Savings and SIP")
                    + link("calculators/spending.html", "Spending planner")
                    + link("calculators/planning.html", "Emergency and retirement")
                    + link("calculators/loan.html", "Loan EMI")
                    + link("calculators/income-tax.html", "Income tax"),
                    ("calculators/",))
            + group("Markets",
                    link("us-market.html", "US markets")
                    + link("us-funds.html", "US funds")
                    + link("us-compare.html", "Compare US funds"),
                    ("us-market.html",))
            + group("Money news <span class=\"badge-new\">New</span>",
                    link("news.html", "Today's headlines")
                    + link("check.html", "Scam checker")
                    + link("market-game.html", "Market game"),
                    ("news.html", "check.html", "market-game.html"))
            + group("About", link("how-we-work.html", "How we work") + link("privacy.html", "Privacy")
                    + link("feedback.html", "Contact us")
                    + link("about-editor.html", "About the editor")
                    + link("articles.html", "All articles")
                    + link("terms.html", "Terms of use")
                    + link("disclaimer.html", "Disclaimer"),
                    ("how-we-work.html", "privacy.html", "feedback.html"))
        )
        return (
            '<aside class="sidebar" id="sidebar" aria-label="Sections">'
            '<nav class="side-nav">' + groups + "</nav></aside>"
        )

    site_cfg = load_json(CONTENT / "site.json") if (CONTENT / "site.json").exists() else {}
    analytics_cfg = site_cfg.get("analytics") or {}
    provider = (analytics_cfg.get("provider") or "none").strip().lower()
    token = (analytics_cfg.get("token") or "").strip()

    analytics_snippet = ""
    if token and provider == "cloudflare":
        analytics_snippet = (
            '<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
            "data-cf-beacon='{\"token\":\"" + token + "\"}'></script>"
        )
    elif token and provider == "goatcounter":
        analytics_snippet = (
            '<script data-goatcounter="https://' + token + '.goatcounter.com/count" '
            'async src="https://gc.zgo.at/count.js"></script>'
        )
    elif token and provider == "plausible":
        analytics_snippet = (
            '<script defer data-domain="paisaclear.co.in" '
            'src="https://plausible.io/js/script.js"></script>'
        )
    elif token and provider in ("ga4", "googleads"):
        analytics_snippet = (
            '<script async src="https://www.googletagmanager.com/gtag/js?id=' + token + '"></script>'
            "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
            "gtag('js',new Date());gtag('config','" + token + "');</script>"
        )

    google_token = ((site_cfg.get("verification") or {}).get("google") or "").strip()
    verify_tag = (
        '<meta name="google-site-verification" content="' + google_token + '">'
        if google_token else ""
    )

    adsense_client = (site_cfg.get("adsense") or {}).get("client", "")
    adsense_snippet = (
        '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client='
        + adsense_client + '" crossorigin="anonymous"></script>'
    ) if adsense_client else ""

    head_snippet = (analytics_snippet if provider in ("ga4", "googleads") else "") + adsense_snippet
    body_snippet = "" if provider in ("ga4", "googleads") else analytics_snippet

    # Pages Google should not index: aggregated news, and the two sections
    # that are templated per record. They stay live for readers.
    noindex_pages: set[str] = set()
    _us_fund_tickers: set[str] = set()

    def _is_noindex(rel_page: str) -> bool:
        # The product catalogue is templated per record: 310 pages sharing 83% of
        # their text. They stay live for readers and for comparison, but only the
        # category hubs, plans, guides and articles are offered for indexing.
        if rel_page in ("news.html", "404.html", "feedback-thanks.html"):
            return True
        if rel_page.startswith("products/"):
            return True
        if rel_page.startswith("us-funds/") and rel_page.count("/") == 1:
            slug = rel_page.split("/")[1][:-5]
            return slug in _us_fund_tickers  # ticker pages, not category pages
        return False

    def emit(rel: str, markup: str) -> None:
        url = "https://paisaclear.co.in/" + rel.replace("index.html", "").replace(".html", "")
        canonical = (
            '<link rel="canonical" href="' + url + '">\n'
            '<meta property="og:url" content="' + url + '">'
        )
        og_image = "https://paisaclear.co.in/assets/img/og-default.png"
        if rel.startswith("categories/"):
            og_image = "https://paisaclear.co.in/assets/img/og-cat-" + rel.split("/", 1)[1][:-5] + ".png"
        elif rel.startswith("products/"):
            slug = rel.split("/", 1)[1][:-5]
            prod = next((p for p in products if p["slug"] == slug), None)
            if prod:
                cat = next((c for c in ctx["categories"] if c["id"] == prod["category"]), None)
                if cat:
                    og_image = "https://paisaclear.co.in/assets/img/og-cat-" + cat["slug"] + ".png"
        markup = markup.replace("https://paisaclear.co.in/assets/img/og-default.png", og_image)
        markup = markup.replace("<!--CANONICAL-->", canonical)
        if "<!--SIDEBAR-->" in markup:
            markup = markup.replace("<!--SIDEBAR-->", sidebar_for(rel))
        if _is_noindex(rel):
            noindex_pages.add(rel)
            markup = markup.replace(
                "</head>",
                '<meta name="robots" content="noindex,follow">\n</head>', 1,
            )
        markup = markup.replace("<!--ANALYTICS-->", body_snippet)
        if head_snippet:
            markup = markup.replace("</head>", head_snippet + "\n</head>", 1)
        if verify_tag:
            markup = markup.replace("</head>", verify_tag + "\n</head>", 1)
        write(SITE / rel, markup)
        written.append(rel)

    jsonld = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite","name":"PaisaClear","url":"https://paisaclear.co.in/","inLanguage":"en-IN","potentialAction":{"@type":"SearchAction","target":"https://paisaclear.co.in/browse?q={search_term_string}","query-input":"required name=search_term_string"}}</script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"PaisaClear","url":"https://paisaclear.co.in/","logo":"https://paisaclear.co.in/assets/img/og-default.png"}</script>
</head>"""
    emit("index.html", page(
        title="PaisaClear — understand Indian financial products before you invest",
        description="Plain-language guides to Indian financial products: schemes, deposits, funds, bonds and insurance. Every figure dated and sourced.",
        body=pages.home(ctx),
        active="home",
    ).replace("</head>", jsonld))

    emit("start.html", page(
        title="Start here — PaisaClear",
        description="New to Indian financial products? Three ways in: look a product up, run a calculator, or read how the figures are sourced.",
        body=start.start_here(ctx),
        active="start",
    ))

    emit("browse.html", page(
        title="All products — PaisaClear",
        description="Browse every product in the catalogue. Filter by category, by return type, or by minimum investment.",
        body=pages.browse(ctx),
        active="browse",
        scripts=["assets/js/browse.js"],
    ))

    _excluded = {c["id"] for c in ctx["categories"] if c.get("excludeFromCompare")}
    write(SITE / "assets/data/catalog.json",
          catalog_json([p for p in products if p["category"] not in _excluded]))

    emit("compare.html", page(
        title="Compare products — PaisaClear",
        description="Put up to three financial products side by side: return type, minimum investment, tenure, payout, access, risk and tax.",
        body=pages.compare(ctx, catalog_json(products)),
        active="compare",
    ))

    emit("how-we-work.html", page(
        title="How this catalogue works — PaisaClear",
        description="What we publish, how a product record is researched and approved, and what we deliberately do not do.",
        body=pages.method(ctx),
        active="method",
    ))

    emit("paisadiscover.html", page(
        title="PaisaDiscover — find products that fit what you need",
        description="Answer five questions and narrow 253 Indian financial products to those whose terms match what you need.",
        body=finder.finder(products),
        active="discover",
        scripts=["assets/js/finder.js"],
    ))

    emit("calculators/income-tax.html", page(
        title="Income tax calculator — PaisaClear",
        description="Calculate income tax for 2026-27 for individuals, HUF, firms, companies and local authorities, with rebate, surcharge and cess.",
        body=income_tax.income_tax(load_json(CONTENT / "tax-rules.json")) + calc_notes.NOTES["calculators/income-tax.html"],
        base="../",
        active="calculator",
        scripts=["assets/js/income-tax.js"],
    ))

    emit("calculators/loan.html", page(
        title="Loan EMI calculator — PaisaClear",
        description="Work out the EMI on a loan, the total interest, and the year-by-year repayment schedule, including the effect of an extra monthly payment.",
        body=loan.loan_page() + calc_notes.NOTES["calculators/loan.html"],
        base="../",
        active="calculator",
        scripts=["assets/js/loan.js"],
    ))

    emit("calculators/planning.html", page(
        title="Emergency fund and retirement planners — PaisaClear",
        description="Work out an emergency fund target and a retirement corpus from your own figures, and see which products your amounts can reach.",
        body=plan.plan_page(products) + calc_notes.NOTES["calculators/planning.html"],
        base="../",
        active="calculator",
        scripts=["assets/js/plan.js"],
    ))

    emit("calculators/spending.html", page(
        title="Spending planner — PaisaClear",
        description="Log what you spend, see which categories take the most, and find products your balance can already start. Stored in your browser only.",
        body=planner.planner_page(products) + calc_notes.NOTES["calculators/spending.html"],
        base="../",
        active="calculator",
        scripts=["assets/js/planner.js"],
    ))

    emit("calculators/savings.html", page(
        title="Savings, SIP and deposit calculator — PaisaClear",
        description="Work out what a monthly SIP, a one-time investment or a fixed deposit could grow to, including the value in today's money.",
        body=calculator.money_calculator() + calc_notes.NOTES["calculators/savings.html"],
        base="../",
        active="calculator",
        scripts=["assets/js/money.js"],
    ))

    faq = load_json(CONTENT / "faq.json")
    emit("answers.html", page(
        title="Answers — PaisaClear",
        description="Straight answers on PPF, FDs, mutual funds, bonds, insurance and tax, drawn from the same dated data as the catalogue.",
        body=answers.body(faq),
        active="answers",
        scripts=["assets/js/faq.js"],
    ).replace("</head>", answers.jsonld(faq) + "</head>"))

    editor_cfg = site_cfg.get("editor") or {}
    emit("about-editor.html", page(
        title="About the editor — PaisaClear",
        description="Who writes PaisaClear, how the figures are checked, and how to hold the site to its standard.",
        body=editorial.page(editor_cfg, "15 November 2026"),
        active="",
    ))

    _LONG = {
        "dividend-streak.html": (articles_long1.DIVIDEND,
                                 articles_extra1.EXTRAS["dividend"] + articles_extra3.EXTRAS["dividend"]
                                 + articles_extra4.EXTRAS["dividend"]),
        "scss-vs-fd.html": (articles_long1.SCSS,
                            articles_extra1.EXTRAS["scss"] + articles_extra3.EXTRAS["scss"]
                                 + articles_extra4.EXTRAS["scss"]),
        "health-insurance-after-60.html": (articles2.PARENTS,
                                           articles_extra2.EXTRAS["parents"] + articles_extra3.EXTRAS["parents"]
                                 + articles_extra4.EXTRAS["parents"]),
        "small-savings-rates.html": (articles2.RATES,
                                     articles_extra2.EXTRAS["rates"] + articles_extra3.EXTRAS["rates"]
                                 + articles_extra4.EXTRAS["rates"]),
        "emergency-fund.html": (articles2.EMERGENCY,
                                articles_extra2.EXTRAS["emergency"] + articles_extra3.EXTRAS["emergency"]
                                 + articles_extra4.EXTRAS["emergency"]),
    }

    for _slug, _file, _name, _line, _when, _html in articles2.EXTRA:
        _base, _extra = _LONG.get(_file, (_html, ""))
        _html = _article_body(_base, _extra)
        articles.ARTICLES.append((_file, _name, _line, _when))
        emit(_file, page(
            title=_name + " — PaisaClear",
            description=_line,
            body=_html,
            active="",
        ))

    _us = load_json(CONTENT / "us_market.json") if (CONTENT / "us_market.json").exists() else {}
    emit("us-market.html", page(
        title="US markets — indices, Treasury yields, ETFs and deposit rates",
        description="US market data for Indian readers: S&P 500, Nasdaq, Treasury yields, the largest ETFs and index funds, with the date each figure was observed.",
        body=us_market.page(_us),
        active="us",
    ))

    _us_funds = load_json(CONTENT / "us_funds.json") if (CONTENT / "us_funds.json").exists() else {}
    if _us_funds.get("records"):
        _us_fund_tickers.update(r["ticker"].lower() for r in _us_funds["records"])
        emit("us-funds.html", page(
            title="US funds and ETFs — categories, returns and comparison",
            description="US-listed mutual funds and ETFs with price history, returns and distribution yield, grouped by category and dated.",
            body=us_funds.hub(_us_funds),
            active="us",
        ))
        for _cat in _us_funds["categories"]:
            emit(f"us-funds/{us_funds.slugify(_cat)}.html", page(
                title=f"{_cat} funds — US market",
                description=f"US {_cat.lower()} mutual funds and ETFs with returns and the date each price was observed.",
                body=us_funds.category_page(_us_funds, _cat),
                base="../",
                active="us",
            ))
        for _r in _us_funds["records"]:
            emit(f"us-funds/{_r['ticker'].lower()}.html", page(
                title=f"{_r['name']} ({_r['ticker']}) — returns and price history",
                description=f"{_r['name']}: {_r['kind']} in the {_r['category']} category, with one, three and five-year returns and the price as of {_r['asOf']}.",
                body=us_funds.product_page(_r),
                base="../",
                active="us",
            ))
        emit("us-compare.html", page(
            title="Compare US funds — returns and yield side by side",
            description="All US funds and ETFs on this site in one table: price, one, three and five-year returns and distribution yield.",
            body=us_funds.compare_page(_us_funds),
            active="us",
        ))

    emit("market-game.html", page(
        title="The Market Game — PaisaClear",
        description="A simulated stock market with fake money. Trade, lose, and learn why buying after a rally or selling into a fall is a bad habit.",
        body=game.page(),
        active="game",
        scripts=["assets/js/market-game.js"],
    ))

    articles.ARTICLES.append(("us-investing-from-india.html",
        "Buying US stocks from India: rules, taxes and the estate-tax trap",
        "Remittance limits, TCS, dividend withholding and a US estate-tax exposure most investors never hear about.",
        "15 November 2026"))
    emit("us-investing-from-india.html", page(
        title="Buying US stocks from India: rules, taxes and the estate-tax trap",
        description="How an Indian resident buys US shares: LRS limits, TCS, dividend withholding, capital gains and the US estate-tax exposure.",
        body=articles_us.ARTICLE,
        active="",
    ))

    emit("articles.html", page(
        title="Articles — PaisaClear",
        description="Long-form pieces on the parts of Indian financial products that decide whether they work for you.",
        body=articles.index(),
        active="",
    ))

    emit("health-insurance-policy-clauses.html", page(
        title="How to read a health insurance policy — PaisaClear",
        description="The five clauses that decide a health insurance claim: waiting periods, room rent limits, sub-limits, co-payment and restoration.",
        body=_article_body(articles_long1.HEALTH_POLICY,
                                  articles_extra1.EXTRAS["health-policy"] + articles_extra3.EXTRAS["health-policy"]
                                  + articles_extra4.EXTRAS["health-policy"]),
        active="",
    ))

    emit("ppf-vs-fd-vs-nsc-tax.html", page(
        title="PPF vs FD vs NSC: the tax arithmetic — PaisaClear",
        description="After-tax returns for PPF, fixed deposits and NSC, with a worked fifteen-year example at three tax slabs.",
        body=_article_body(articles_long1.TAX,
                                  articles_extra1.EXTRAS["tax"] + articles_extra3.EXTRAS["tax"]
                                  + articles_extra4.EXTRAS["tax"]),
        active="",
    ))

    emit("terms.html", page(
        title="Terms of use — PaisaClear",
        description="The rules for using PaisaClear: what the site is, how it is accurate, its limits and your rights.",
        body=legal.terms(),
        active="",
    ))

    emit("disclaimer.html", page(
        title="Disclaimer — PaisaClear",
        description="PaisaClear is general information, not investment advice. How the figures, calculators and third-party data should be read.",
        body=legal.disclaimer(),
        active="",
    ))

    emit("privacy.html", page(
        title="Privacy — PaisaClear",
        description="What this site collects: feedback you send, server-side visit statistics without cookies, and planners that stay in your browser.",
        body=privacy.privacy(ctx),
        active="",
    ))

    emit("feedback.html", page(
        title="Contact us — PaisaClear",
        description="Report a wrong figure, a missing product or a broken page. Corrections are checked against the source before anything changes.",
        body=pages.feedback(ctx),
    ))

    emit("feedback-thanks.html", page(
        title="Thank you — PaisaClear",
        description="Your feedback has been sent.",
        body=pages.feedback_thanks(ctx),
    ))

    tax_rules = load_json(CONTENT / "tax-rules.json")
    guide_rates = load_json(CONTENT / "rates.json")["values"]
    for rel, title, desc, body in (
        ("guides/ppf-vs-fd-vs-nsc.html", "PPF vs FD vs NSC — which suits what",
         "Compare a PPF, a bank fixed deposit and an NSC on rate, term, tax and access, with the after-tax arithmetic.",
         guides.ppf_vs_fd_vs_nsc(ctx, guide_rates)),
        ("guides/sip-vs-lump-sum.html", "SIP vs lump sum — the real difference",
         "What changes when you invest monthly instead of all at once: timing risk, cash flow, and when each makes sense.",
         guides.sip_vs_lump_sum(ctx, guide_rates)),
        ("guides/old-vs-new-tax-regime.html", "Old vs new tax regime, compared",
         "The two slab tables side by side, a worked example at 15 lakh, and what the old regime still allows.",
         guides.old_vs_new_regime(ctx, guide_rates, tax_rules)),
        ("plans/beti-bachao-beti-padhao.html", "Beti Bachao Beti Padhao — what it is and what it is not",
         "The girl-child campaign explained: objectives, what it does not pay, and the savings scheme to use instead.",
         bbbp.page(guide_rates.get("ssy", {}).get("value", ""), guide_rates.get("ssy", {}).get("asOf", ""))),
        ("plans/sukanya-samriddhi.html", "Sukanya Samriddhi Yojana — the full guide",
         "Who can open an SSY account, the deposit rules, partial withdrawal, tax treatment and a 21-year calculator.",
         ssy.page(tax_rules, guide_rates)),
        ("guides/ssy-vs-ppf.html", "SSY vs PPF — who each one is for",
         "Sukanya Samriddhi and PPF compared on rate, term, limits and access.",
         extra_guides.ssy_vs_ppf(guide_rates)),
        ("guides/scss-vs-fd.html", "SCSS vs bank FD — the rate and the safety",
         "A quarterly-paying government scheme for over-60s against a flexible bank deposit.",
         extra_guides.scss_vs_fd(guide_rates)),
        ("guides/sip-vs-fd.html", "SIP vs FD — promise versus possibility",
         "A fixed deposit and a monthly equity investment compared on risk, tax and time horizon.",
         extra_guides.sip_vs_fd(guide_rates)),
        ("guides/nps-vs-ppf.html", "NPS vs PPF — pension against provident fund",
         "Market-linked pension with a lock-in to 60, against a guaranteed tax-free account.",
         extra_guides.nps_vs_ppf(guide_rates)),
        ("guides/small-savings-compared.html", "Small savings schemes compared",
         "PPF, SSY, SCSS, NSC, KVP, MIS and post office deposits in one table: rate, term, limits, tax and access.",
         guides.small_savings_compared(ctx, guide_rates)),
    ):
        body = body + guide_notes.NOTES.get(rel, "")
        emit(rel, page(title=title + " — PaisaClear", description=desc, body=body,
                       base="../", active="browse"))

    plan_registry = [
        {"slug": "sukanya-samriddhi", "tag": "Government scheme", "name": "Sukanya Samriddhi Yojana",
         "line": "The highest small-savings rate, entirely tax-free, for a daughter under ten.",
         "meta": f"{guide_rates.get('ssy', {}).get('value', '')} · 21 years · calculator included"},
        {"slug": "beti-bachao-beti-padhao", "tag": "Campaign", "name": "Beti Bachao Beti Padhao",
         "line": "The national girl-child campaign — awareness and delivery, not a money product.",
         "meta": "No deposit · no interest · no calculator"},
    ]

    for scheme in plan_schemes.SCHEMES:
        emit(f"plans/{scheme['slug']}.html", page(
            title=f"{scheme['name']} — rate, rules and calculator",
            description=scheme["intro"][:155],
            body=plan_schemes.page(scheme, guide_rates),
            base="../",
            active="plans",
        ))
        rate = (guide_rates.get(scheme["rate_key"]) or {}).get("value", "")
        plan_registry.append({
            "slug": scheme["slug"], "tag": scheme["tag"], "name": scheme["name"],
            "line": scheme["intro"], "meta": f"{rate} · {scheme['term']} · calculator included",
        })

    emit("plans.html", page(
        title="Plans, explained in full — PaisaClear",
        description="One page per scheme: eligibility, deposit rules, withdrawal rules, tax treatment and a working calculator.",
        body=plans.page(plan_registry),
        active="plans",
    ))

    emit("news.html", page(
        title="Money news — markets, policy and personal finance",
        description="Daily headlines from Indian finance publishers: markets, RBI policy and personal money, each linked to the original report.",
        body=news.page(load_json(CONTENT / "news.json") if (CONTENT / "news.json").exists() else {"items": []}),
        active="news",
        scripts=["assets/js/news.js"],
    ))

    emit("check.html", page(
        title="Scam checker — PaisaClear",
        description="Paste a message, number or link and see which patterns commonly used in financial scams it contains.",
        body=checker.page(),
        active="",
    ))

    emit("rates.html", page(
        title="Today's rates — PaisaClear",
        description="Every small-savings rate and government bond yield this site tracks, with the date each applied.",
        body=extra_guides.rates_hub(guide_rates),
        active="browse",
    ))
    emit("calculators/salary.html", page(
        title="Salary & take-home calculator — PaisaClear",
        description="Work out your take-home pay from CTC under both the new and old tax regimes, with HRA, 80C, 80D and home-loan interest.",
        body=calculator.salary_calculator(tax_rules) + calc_notes.NOTES["calculators/salary.html"],
        base="../",
        active="calculator",
        scripts=["assets/js/salary.js"],
    ))

    emit("404.html", page(
        title="Page not found — PaisaClear",
        description="That page could not be found.",
        body=pages.not_found(ctx),
        base="",
        active="",
    ))

    for category in ctx["categories"]:
        emit(f"categories/{category['slug']}.html", page(
            title=f"{category['name']} — PaisaClear",
            description=(category["blurb"][:152].rsplit(" ", 1)[0] + "…"
                         if len(category["blurb"]) > 158 else category["blurb"]),
            body=pages.category_page(ctx, category),
            base="../",
            active="browse",
        ))

    for product in products:
        if product["category"] == "dividend-champions":
            body = dividends.page(ctx, product)
        elif product["category"] == "health-insurance":
            body = health.page(ctx, product)
        else:
            body = pages.product_page(ctx, product)
        emit(f"products/{product['slug']}.html", page(
            title=f"{product['name']} — PaisaClear",
            description=_product_description(product, ctx),
            body=body,
            base="../",
            active="browse",
        ))

    # Sitemap: every page we just wrote, minus the utility ones.
    base_url = "https://paisaclear.co.in"
    skip = {"404.html", "feedback-thanks.html"}
    urls = []
    for rel in sorted(written):
        if not rel.endswith(".html") or rel in skip or rel in noindex_pages:
            continue
        loc = base_url + "/" + rel.replace("index.html", "").replace(".html", "")
        loc = loc.rstrip("/") if loc != base_url + "/" else loc
        urls.append(
            "  <url><loc>" + loc + "</loc>"
            + ("<lastmod>" + TODAY + "</lastmod>" if "TODAY" in globals() else "")
            + "</url>"
        )
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n</urlset>\n"
    )
    (SITE / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (SITE / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: " + base_url + "/sitemap.xml\n",
        encoding="utf-8",
    )
    written.append("sitemap.xml")

    # Report
    print("PaisaClear build")
    print("-" * 46)
    print(f"  approved products : {len(products):>3}")
    for status in ("draft", "pending", "rejected"):
        if status_counts.get(status):
            print(f"  {status:<17} : {status_counts[status]:>3}  (excluded)")
    print(f"  categories        : {len(ctx['categories']):>3}")
    print(f"  pages written     : {len(written):>3}")
    print(f"  noindexed         : {len(noindex_pages):>3}  (kept live, out of sitemap)")
    print(f"  output            : {SITE}")
    print("-" * 46)

    missing_icons = [c["icon"] for c in ctx["categories"] if c["icon"] not in ICONS]
    if missing_icons:
        print(f"  warning: unknown icons {missing_icons}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
