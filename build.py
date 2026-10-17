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

from builder import pages  # noqa: E402
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

        if not isinstance(product.get("minInvestment"), (int, float)):
            errors.append(f"{slug}: minInvestment must be a number")

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

    def emit(rel: str, markup: str) -> None:
        write(SITE / rel, markup)
        written.append(rel)

    emit("index.html", page(
        title="PaisaClear — understand Indian financial products before you invest",
        description="Plain-language guides to government schemes, bank deposits, mutual funds, bonds and ETFs. Compare what you are promised, how long your money is locked in, and what can go wrong.",
        body=pages.home(ctx),
        active="home",
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
            description=category["blurb"],
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
