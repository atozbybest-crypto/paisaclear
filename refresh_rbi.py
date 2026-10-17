#!/usr/bin/env python3
"""Pull current rates from the RBI homepage into content/rates.json.

Only entries whose feed is marked "rbi" are touched; the quarterly small-savings
values are left exactly as they are.

    python refresh_rbi.py            fetch, compare, write
    python refresh_rbi.py --dry-run  fetch and show what would change

Exit codes: 0 success (with or without changes), 1 fetch or parse failure —
in which case rates.json is left untouched.
"""

from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RATES = ROOT / "content" / "rates.json"
SOURCE_URL = "https://www.rbi.org.in/"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

RUPEE_NOTES = re.compile(r"<[^>]+>")


def fetch(url: str, timeout: int = 30) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-IN,en;q=0.9",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout, context=ssl.create_default_context()) as response:
        return response.read().decode("utf-8", "replace")


def to_text(markup: str) -> str:
    """Crude but sufficient: drop scripts/styles, then tags, then squeeze spaces."""
    markup = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", markup, flags=re.S | re.I)
    text = RUPEE_NOTES.sub(" ", markup)
    text = text.replace("&nbsp;", " ").replace("&amp;", "&").replace("&#39;", "'")
    return re.sub(r"[ \t\u00a0]+", " ", text)


def find(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text)
    return match.group(1).strip() if match else None


def parse_date(text: str) -> str:
    """Find 'as at ... October 16, 2026' or 'as on October 15, 2026'."""
    match = re.search(
        r"as (?:at|on)[^A-Za-z]*(?:\d{1,2}[.,:0-9 ]*)?(January|February|March|April|May|June|July|August|"
        r"September|October|November|December)\s+(\d{1,2}),?\s+(\d{4})",
        text,
        re.I,
    )
    if match:
        month, day, year = match.groups()
        try:
            parsed = datetime.strptime(f"{day} {month} {year}", "%d %B %Y")
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            pass
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def collect(text: str) -> dict[str, str]:
    """Map rates.json keys to the value found on the page."""
    found: dict[str, str] = {}

    repo = find(r"Policy\s*Repo\s*Rate\s*:?\s*([\d.]+)\s*%", text)
    if repo:
        found["repo"] = f"{repo}%"

    savings = find(r"Savings\s*Deposit\s*Rate\s*:?\s*([\d.]+)\s*%", text)
    if savings:
        found["savings"] = f"{savings}%"

    term = find(r"Term\s*Deposit\s*Rate\s*>\s*1\s*Year\s*:?\s*([\d.]+)\s*%\s*-\s*([\d.]+)\s*%", text)
    if term:
        found["term-deposit"] = term

    for days in ("91", "182", "364"):
        value = find(rf"{days}\s*day\s*T-?bills?\s*:?\s*([\d.]+)\s*%", text)
        if value:
            found[f"tbill-{days}"] = f"{value}%"

    # Named securities: "6.94% GS 2036 : 7.3865%"
    for match in re.finditer(r"(\d{1,2}\.\d{1,2})\s*%\s*GS\s*(\d{4})\s*:?\s*([\d.]+)\s*%", text):
        coupon, year, value = match.groups()
        found[f"gs-{year}"] = f"{value}%"

    return found


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh RBI-sourced rates.")
    parser.add_argument("--dry-run", action="store_true", help="show changes without writing")
    args = parser.parse_args()

    try:
        markup = fetch(SOURCE_URL)
    except (urllib.error.URLError, TimeoutError, ssl.SSLError) as exc:
        print(f"Fetch failed: {exc}", file=sys.stderr)
        print("rates.json left unchanged.", file=sys.stderr)
        return 1

    text = to_text(markup)
    found = collect(text)
    if not found:
        print("Parsed the page but recognised no rates. The layout may have changed.", file=sys.stderr)
        print("rates.json left unchanged.", file=sys.stderr)
        return 1

    as_of = parse_date(text)
    stamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    rates = json.loads(RATES.read_text(encoding="utf-8"))
    values = rates["values"]

    # The site keys are explicit (gs-2029), the page speaks in years (GS 2029).
    aliases = {
        "tbill-91": "tbill-91",
        "tbill-182": "tbill-182",
        "tbill-364": "tbill-364",
        "gs-2029": "gs-2029",
        "gs-2031": "gs-2031",
        "gs-2036": "gs-2036",
        "gs-2041": "gs-2041",
        "gs-2056": "gs-2056",
    }

    changed: list[tuple[str, str, str]] = []
    missing: list[str] = []

    for key, alias in aliases.items():
        if alias not in found:
            if key in values:
                missing.append(key)
            continue
        new_value = found[alias]
        entry = values.get(key)
        if entry is None:
            continue
        if entry.get("value") != new_value or entry.get("asOf") != as_of:
            changed.append((key, entry.get("value", "—"), new_value))
            if not args.dry_run:
                entry["value"] = new_value
                entry["asOf"] = as_of

    if not args.dry_run:
        rates["feeds"]["rbi"]["fetchedAt"] = stamp
        rates["generatedAt"] = stamp
        RATES.write_text(
            json.dumps(rates, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
        )

    print(f"RBI rates — as of {as_of}")
    print("-" * 52)
    if changed:
        for key, before, after in changed:
            print(f"  {key:<14} {before:>10}  ->  {after}")
    else:
        print("  no changes; values already match the source")
    if missing:
        print(f"  not found on the page (left alone): {', '.join(missing)}")
    print("-" * 52)
    print("Dry run — nothing written." if args.dry_run else f"Updated {RATES.name}.")
    print("Rebuild with: python build.py && python bundle.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
