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

from builder import answers, calculator, dividends, extra_guides, finder, guides, income_tax, loan, pages, plan, planner, privacy, start  # noqa: E402
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
                    + link("guides/ssy-vs-ppf.html", "SSY vs PPF")
                    + link("guides/scss-vs-fd.html", "SCSS vs FD")
                    + link("guides/sip-vs-fd.html", "SIP vs FD")
                    + link("guides/nps-vs-ppf.html", "NPS vs PPF"),
                    ("guides/",))
            + group("Calculators",
                    link("calculators/salary.html", "Salary and take-home")
                    + link("calculators/savings.html", "Savings and SIP")
                    + link("calculators/spending.html", "Spending planner")
                    + link("calculators/planning.html", "Emergency and retirement")
                    + link("calculators/loan.html", "Loan EMI")
                    + link("calculators/income-tax.html", "Income tax"),
                    ("calculators/",))
            + group("About", link("how-we-work.html", "How we work") + link("privacy.html", "Privacy")
                    + link("feedback.html", "Feedback"),
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

    head_snippet = analytics_snippet if provider in ("ga4", "googleads") else ""
    body_snippet = "" if head_snippet else analytics_snippet

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
        body=income_tax.income_tax(load_json(CONTENT / "tax-rules.json")),
        base="../",
        active="calculator",
        scripts=["assets/js/income-tax.js"],
    ))

    emit("calculators/loan.html", page(
        title="Loan EMI calculator — PaisaClear",
        description="Work out the EMI on a loan, the total interest, and the year-by-year repayment schedule, including the effect of an extra monthly payment.",
        body=loan.loan_page(),
        base="../",
        active="calculator",
        scripts=["assets/js/loan.js"],
    ))

    emit("calculators/planning.html", page(
        title="Emergency fund and retirement planners — PaisaClear",
        description="Work out an emergency fund target and a retirement corpus from your own figures, and see which products your amounts can reach.",
        body=plan.plan_page(products),
        base="../",
        active="calculator",
        scripts=["assets/js/plan.js"],
    ))

    emit("calculators/spending.html", page(
        title="Spending planner — PaisaClear",
        description="Log what you spend, see which categories take the most, and find products your balance can already start. Stored in your browser only.",
        body=planner.planner_page(products),
        base="../",
        active="calculator",
        scripts=["assets/js/planner.js"],
    ))

    emit("calculators/savings.html", page(
        title="Savings, SIP and deposit calculator — PaisaClear",
        description="Work out what a monthly SIP, a one-time investment or a fixed deposit could grow to, including the value in today's money.",
        body=calculator.money_calculator(),
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

    emit("privacy.html", page(
        title="Privacy — PaisaClear",
        description="What this site collects: feedback you send, server-side visit statistics without cookies, and planners that stay in your browser.",
        body=privacy.privacy(ctx),
        active="",
    ))

    emit("feedback.html", page(
        title="Feedback — PaisaClear",
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
        emit(rel, page(title=title + " — PaisaClear", description=desc, body=body,
                       base="../", active="browse"))

    emit("rates.html", page(
        title="Today's rates — PaisaClear",
        description="Every small-savings rate and government bond yield this site tracks, with the date each applied.",
        body=extra_guides.rates_hub(guide_rates),
        active="browse",
    ))
    emit("calculators/salary.html", page(
        title="Salary & take-home calculator — PaisaClear",
        description="Work out your take-home pay from CTC under both the new and old tax regimes, with HRA, 80C, 80D and home-loan interest.",
        body=calculator.salary_calculator(tax_rules),
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
        else:
            body = pages.product_page(ctx, product)
        emit(f"products/{product['slug']}.html", page(
            title=f"{product['name']} — PaisaClear",
            description=product["oneLiner"],
            body=body,
            base="../",
            active="browse",
        ))

    # Sitemap: every page we just wrote, minus the utility ones.
    base_url = "https://paisaclear.co.in"
    skip = {"404.html", "feedback-thanks.html"}
    urls = []
    for rel in sorted(written):
        if not rel.endswith(".html") or rel in skip:
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
    print(f"  output            : {SITE}")
    print("-" * 46)

    missing_icons = [c["icon"] for c in ctx["categories"] if c["icon"] not in ICONS]
    if missing_icons:
        print(f"  warning: unknown icons {missing_icons}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
