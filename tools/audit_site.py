#!/usr/bin/env python3
"""Deployment and content audit.

Checks the built site, the live deployment and the data files. Exits non-zero
if anything needs action, so the daily workflow fails loudly and GitHub emails.

    python tools/audit_site.py
    python tools/audit_site.py --local-only
"""

from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
import urllib.request
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
UA = "Mozilla/5.0 (compatible; PaisaClearAudit/1.0)"
CTX = ssl.create_default_context()

problems: list[str] = []
notes: list[str] = []


def fail(message: str) -> None:
    problems.append(message)


def note(message: str) -> None:
    notes.append(message)


def get(url: str, accept: str = "text/html") -> tuple[int, bytes]:
    request = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    with urllib.request.urlopen(request, timeout=25, context=CTX) as response:
        return response.status, response.read()


def audit_local() -> None:
    pages = {str(p.relative_to(SITE)).replace("\\", "/"): p for p in SITE.rglob("*.html")}
    if not pages:
        fail("site/ has no HTML — the build did not run")
        return
    note(f"pages: {len(pages)}")

    broken = []
    thin = []
    for rel, path in pages.items():
        html = path.read_text(encoding="utf-8")
        for href in re.findall(r'(?:href|src)="([^"]+)"', html):
            if href.startswith(("http", "mailto:", "#", "tel:", "data:")):
                continue
            target = (path.parent / urlsplit(href).path).resolve()
            if not target.exists():
                broken.append(f"{rel} -> {href}")
        if 'rel="canonical"' not in html or "og:image" not in html or "<h1" not in html:
            thin.append(rel)

    if broken:
        fail(f"{len(broken)} broken internal link(s), e.g. {broken[0]}")
    else:
        note("internal links: 0 broken")
    if thin:
        fail(f"{len(thin)} page(s) missing canonical, og:image or h1, e.g. {thin[0]}")
    else:
        note("metadata: canonical, og:image and h1 on every page")

    sitemap = (SITE / "sitemap.xml").read_text(encoding="utf-8")
    urls = re.findall(r"<loc>([^<]+)</loc>", sitemap)
    expected = len([p for p in pages if not p.endswith(("404.html", "feedback-thanks.html"))])
    if abs(len(urls) - expected) > 2:
        fail(f"sitemap has {len(urls)} URLs but there are {expected} indexable pages")
    else:
        note(f"sitemap: {len(urls)} URLs")

    robots = (SITE / "robots.txt").read_text(encoding="utf-8")
    if "Sitemap:" not in robots:
        fail("robots.txt does not point at the sitemap")

    # data health
    rates = json.loads((ROOT / "content/rates.json").read_text(encoding="utf-8"))["values"]
    today = date.today()
    stale = []
    for key, entry in rates.items():
        try:
            age = (today - date.fromisoformat(entry["asOf"])).days
        except (KeyError, ValueError):
            stale.append(f"{key}: bad date")
            continue
        limit = 10 if key.startswith("nav-") else 100
        if age > limit:
            stale.append(f"{key}: {age} days old")
    if stale:
        fail(f"{len(stale)} rate(s) outside their window, e.g. {stale[0]}")
    else:
        note(f"rates: {len(rates)} entries, all within window")

    products = json.loads((ROOT / "content/products.json").read_text(encoding="utf-8"))
    counts = Counter(p["category"] for p in products)
    note("products: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))

    withheld = [p["name"] for p in products
                if (p.get("returns") or {}).get("oneYear") is None and p.get("returns")]
    if withheld:
        note(f"returns withheld for {len(withheld)} fund(s)")

    dupes = [name for name, n in Counter(p["name"].lower() for p in products).items() if n > 1]
    if dupes:
        fail(f"duplicate product names: {dupes[:3]}")

    for asset in ("assets/css/styles.css", "assets/js/site.js", "assets/data/catalog.json"):
        if not (SITE / asset).exists():
            fail(f"missing asset: {asset}")

    home = (SITE / "index.html").read_text(encoding="utf-8")
    if "?v=" not in home:
        fail("asset URLs are not versioned — caching may serve stale CSS")

    refresh = (ROOT / ".github/workflows/refresh.yml").read_text(encoding="utf-8")
    crons = re.findall(r'cron:\s*"([^"]+)"', refresh)
    if len(crons) != 1:
        fail(f"refresh.yml should have exactly one schedule, found {len(crons)}")
    else:
        note(f"daily refresh cron: {crons[0]}")


def audit_live() -> None:
    checks = {
        "homepage": "https://paisaclear.co.in/",
        "sitemap": "https://paisaclear.co.in/sitemap.xml",
        "robots": "https://paisaclear.co.in/robots.txt",
        "calculator": "https://paisaclear.co.in/calculators/salary",
        "guide": "https://paisaclear.co.in/guides/ppf-vs-fd-vs-nsc",
        "discover": "https://paisaclear.co.in/paisadiscover",
        "answers": "https://paisaclear.co.in/answers",
        "rates": "https://paisaclear.co.in/rates",
    }
    down = []
    for name, url in checks.items():
        try:
            status, _ = get(url)
            if status != 200:
                down.append(f"{name} {status}")
        except Exception as error:
            down.append(f"{name} {type(error).__name__}")
    if down:
        fail("live pages failing: " + ", ".join(down))
    else:
        note(f"live: all {len(checks)} key pages return 200")

    try:
        status, body = get("https://paisaclear.co.in/")
        html = body.decode("utf-8", "replace")
        if "AW-" not in html:
            fail("Google Ads tag missing from the live homepage")
        else:
            note("live: Google tag present")
        match = re.search(r'assets/css/styles\.css\?v=(\w+)', html)
        if match:
            css_status, _ = get("https://paisaclear.co.in/assets/css/styles.css?v=" + match.group(1),
                                "text/css")
            if css_status != 200:
                fail(f"versioned stylesheet returned {css_status}")
    except Exception as error:
        fail(f"live homepage check failed: {type(error).__name__}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local-only", action="store_true")
    args = parser.parse_args()

    audit_local()
    if not args.local_only:
        audit_live()

    print("PaisaClear audit")
    print("-" * 52)
    for item in notes:
        print(f"  ok    {item}")
    for item in problems:
        print(f"  FAIL  {item}")
    print("-" * 52)
    print(f"{len(problems)} problem(s), {len(notes)} check(s) passed")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
