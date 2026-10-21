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

from builder import calculator, loan, pages, plan, planner, privacy, start  # noqa: E402
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

    def sidebar_for(rel: str) -> str:
        base = "../" if "/" in rel else ""
        current = rel

        def link(href: str, label: str, count: str = "") -> str:
            active = ' aria-current="page"' if current == href else ""
            badge = f'<span class="side-count">{count}</span>' if count else ""
            return f'<a class="side-link" href="{base}{href}"{active}><span>{label}</span>{badge}</a>'

        cat_links = "".join(
            link(f"categories/{c['slug']}.html", c["name"], str(ctx["counts_by_category"].get(c["id"], 0)))
            for c in ctx["categories"]
        )
        return (
            '<aside class="sidebar" id="sidebar" aria-label="Sections">'
            '<nav class="side-nav">'
            '<p class="side-title">Browse</p>'
            + link("start.html", "Start here")
            + link("browse.html", "All products", str(len(products)))
            + link("compare.html", "Compare")
            + '<p class="side-title">Categories</p>' + cat_links
            + '<p class="side-title">Calculators</p>'
            + link("calculators/salary.html", "Salary and take-home")
            + link("calculators/savings.html", "Savings and SIP")
            + link("calculators/spending.html", "Spending planner")
            + link("calculators/planning.html", "Emergency and retirement")
            + link("calculators/loan.html", "Loan EMI")
            + '<p class="side-title">About</p>'
            + link("how-we-work.html", "How we work")
            + link("privacy.html", "Privacy")
            + link("feedback.html", "Feedback")
            + "</nav></aside>"
        )

    site_cfg = load_json(CONTENT / "site.json") if (CONTENT / "site.json").exists() else {}
    analytics_cfg = site_cfg.get("analytics") or {}
    provider = (analytics_cfg.get("provider") or "none").strip().lower()
    token = (analytics_cfg.get("token") or "").strip()

    analytics_snippet = ""
    if token and provider == "cloudflare":
        analytics_snippet = (
            '<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
            'data-cf-beacon=\'{"token":"' + token + '"}\'></script>'
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
    elif token and provider == "ga4":
        analytics_snippet = (
            '<script async src="https://www.googletagmanager.com/gtag/js?id=' + token + '"></script>'
            '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
            'gtag("js",new Date());gtag("config","' + token + '");</script>'
        )

    google_token = ((site_cfg.get("verification") or {}).get("google") or "").strip()
    verify_tag = (
        '<meta name="google-site-verification" content="' + google_token + '">'
        if google_token else ""
    )

    def emit(rel: str, markup: str) -> None:
        url = "https://paisaclear.co.in/" + rel.replace("index.html", "").replace(".html", "")
        canonical = (
            '<link rel="canonical" href="' + url + '">\n'
            '<meta property="og:url" content="' + url + '">'
        )
        markup = markup.replace("<!--CANONICAL-->", canonical)
        if "<!--SIDEBAR-->" in markup:
            markup = markup.replace("<!--SIDEBAR-->", sidebar_for(rel))
        markup = markup.replace("<!--ANALYTICS-->", analytics_snippet)
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
        emit(f"products/{product['slug']}.html", page(
            title=f"{product['name']} — PaisaClear",
            description=product["oneLiner"],
            body=pages.product_page(ctx, product),
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
