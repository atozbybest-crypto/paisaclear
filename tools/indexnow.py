#!/usr/bin/env python3
"""Tell Bing and Yandex about the sitemap after a deploy (IndexNow)."""

from __future__ import annotations

import json
import re
import ssl
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
HOST = "paisaclear.co.in"


def main() -> int:
    key = json.loads((ROOT / "content/indexnow.json").read_text(encoding="utf-8"))["key"]
    sitemap = (SITE / "sitemap.xml").read_text(encoding="utf-8")
    urls = re.findall(r"<loc>([^<]+)</loc>", sitemap)
    if not urls:
        print("no URLs in the sitemap")
        return 1

    payload = json.dumps({
        "host": HOST,
        "key": key,
        "keyLocation": f"https://{HOST}/{key}.txt",
        "urlList": urls,
    }).encode()

    request = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30, context=ssl.create_default_context()) as response:
            print(f"IndexNow: {response.status} for {len(urls)} URLs")
            return 0
    except Exception as error:
        print(f"IndexNow failed: {type(error).__name__} {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
