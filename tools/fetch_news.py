#!/usr/bin/env python3
"""Pull Indian finance and economy headlines into content/news.json.

Only headlines, a short summary and a link back to the publisher — never the
full article. Runs from the daily refresh.
"""

from __future__ import annotations

import html
import json
import re
import ssl
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content" / "news.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

FEEDS = [
    ("Markets", "Economic Times", "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms"),
    ("Economy", "Economic Times", "https://economictimes.indiatimes.com/economy/rssfeeds/1373380680.cms"),
    ("Money", "Livemint", "https://www.livemint.com/rss/money"),
    ("Markets", "Business Standard", "https://www.business-standard.com/rss/markets-106.rss"),
    ("Business", "Moneycontrol", "https://www.moneycontrol.com/rss/business.xml"),
    ("Policy", "RBI", "https://www.rbi.org.in/pressreleases_rss.xml"),
]

MAX_PER_FEED = 8
SUMMARY_CHARS = 180


def clean(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def parse_date(value: str) -> str:
    if not value:
        return ""
    try:
        return parsedate_to_datetime(value).astimezone(timezone.utc).isoformat(timespec="minutes")
    except (TypeError, ValueError):
        pass
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt).replace(tzinfo=timezone.utc).isoformat(timespec="minutes")
        except ValueError:
            continue
    return ""


def fetch(section: str, source: str, url: str) -> list[dict]:
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=25, context=ssl.create_default_context()) as response:
        raw = response.read()

    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return []

    items = []
    for node in root.iter("item"):
        title = clean(node.findtext("title", ""))
        link = (node.findtext("link") or "").strip()
        if not title or not link.startswith("http"):
            continue
        summary = clean(node.findtext("description", ""))[:SUMMARY_CHARS]
        items.append({
            "title": title,
            "link": link,
            "summary": summary,
            "source": source,
            "section": section,
            "published": parse_date(node.findtext("pubDate", "")),
        })
        if len(items) >= MAX_PER_FEED:
            break
    return items


def main() -> int:
    collected: list[dict] = []
    seen: set[str] = set()
    failures = []

    for section, source, url in FEEDS:
        try:
            for item in fetch(section, source, url):
                if item["title"].lower() in seen:
                    continue
                seen.add(item["title"].lower())
                collected.append(item)
        except Exception as error:
            failures.append(f"{source} ({section}): {type(error).__name__}")

    collected.sort(key=lambda i: i["published"], reverse=True)

    payload = {
        "updatedAt": datetime.now(timezone.utc).isoformat(timespec="minutes"),
        "items": collected,
    }
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"news: {len(collected)} headlines from {len(FEEDS) - len(failures)}/{len(FEEDS)} feeds")
    for failure in failures:
        print("  failed:", failure)
    if collected:
        print("  newest:", collected[0]["title"][:70], "|", collected[0]["source"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
