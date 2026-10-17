#!/usr/bin/env python3
"""Review workflow for the product catalogue.

    python tools/review.py list                 # everything, grouped by status
    python tools/review.py list pending         # just one status
    python tools/review.py approve <slug>       # draft/pending -> approved
    python tools/review.py reset <slug>         # approved -> pending (pull it offline)
    python tools/review.py reject <slug>        # -> rejected
    python tools/review.py show <slug>          # every field of one record

Run `python build.py` afterwards to regenerate the site.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRODUCTS = ROOT / "content" / "products.json"
STATUSES = ("draft", "pending", "approved", "rejected")


def load() -> list[dict]:
    with PRODUCTS.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def save(products: list[dict]) -> None:
    fd, tmp = tempfile.mkstemp(dir=str(PRODUCTS.parent), prefix=".products-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(products, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        os.replace(tmp, PRODUCTS)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def group(products: list[dict], status: str) -> list[dict]:
    return [p for p in products if p["review"]["status"] == status]


def cmd_list(products: list[dict], only: str | None) -> int:
    statuses = [only] if only else list(STATUSES)
    total = 0
    for status in statuses:
        rows = group(products, status)
        total += len(rows)
        print(f"\n{status.upper()} ({len(rows)})")
        print("-" * 60)
        if not rows:
            print("  none")
            continue
        for product in rows:
            review = product["review"]
            stamp = review.get("approvedAt") or "—"
            print(f"  {product['slug']:<38} {product['category']:<20} {stamp}")
    print(f"\n{total} record(s) shown.")
    if group(products, "approved"):
        print("Only approved records appear on the site. Build with: python build.py")
    return 0


def cmd_show(products: list[dict], slug: str) -> int:
    for product in products:
        if product["slug"] == slug:
            print(json.dumps(product, indent=2, ensure_ascii=False))
            return 0
    print(f"No product with slug '{slug}'", file=sys.stderr)
    return 1


def cmd_set(products: list[dict], slug: str, status: str, reviewer: str) -> int:
    for product in products:
        if product["slug"] != slug:
            continue
        review = product.setdefault("review", {})
        previous = review.get("status")
        review["status"] = status
        if status == "approved":
            review["reviewer"] = reviewer
            review["approvedAt"] = date.today().isoformat()
        elif previous == "approved":
            review["reviewer"] = None
            review["approvedAt"] = None
        save(products)
        print(f"{slug}: {previous} -> {status}")
        if status == "approved":
            print("Run `python build.py` to publish it.")
        elif previous == "approved":
            print("It is no longer approved; rebuild to take the page down.")
        return 0
    print(f"No product with slug '{slug}'", file=sys.stderr)
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Review and approve product records.")
    sub = parser.add_subparsers(dest="command", required=True)
    p_list = sub.add_parser("list")
    p_list.add_argument("status", nargs="?", choices=STATUSES)
    p_show = sub.add_parser("show")
    p_show.add_argument("slug")
    for name, help_text in (
        ("approve", "mark a record approved and publishable"),
        ("reject", "mark a record rejected (never published)"),
        ("reset", "return an approved record to pending"),
    ):
        p = sub.add_parser(name, help=help_text)
        p.add_argument("slug")

    args = parser.parse_args()
    products = load()

    if args.command == "list":
        return cmd_list(products, args.status)
    if args.command == "show":
        return cmd_show(products, args.slug)

    reviewer = os.environ.get("PAISACLEAR_REVIEWER", "editor")
    status = {"approve": "approved", "reject": "rejected", "reset": "pending"}[args.command]
    return cmd_set(products, args.slug, status, reviewer)


if __name__ == "__main__":
    raise SystemExit(main())
