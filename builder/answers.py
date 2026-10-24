"""Answers page — the explainer, built from hand-written Q&A over the data."""

from __future__ import annotations

import json

from .site import esc


def _groups(faq: list) -> list[str]:
    order: list[str] = []
    for item in faq:
        if item["cat"] not in order:
            order.append(item["cat"])
    return order


def body(faq: list) -> str:
    groups = _groups(faq)
    chips = "".join(
        f'<button class="faq-chip{" is-on" if i == 0 else ""}" type="button" data-faq-cat="{esc(g)}">'
        f"{esc(g)}</button>"
        for i, g in enumerate(groups)
    )
    chips = '<button class="faq-chip is-on" type="button" data-faq-cat="all">All</button>' + "".join(
        f'<button class="faq-chip" type="button" data-faq-cat="{esc(g)}">{esc(g)}</button>' for g in groups
    )

    sections = []
    for group in groups:
        items = [f for f in faq if f["cat"] == group]
        rows = []
        for item in items:
            links = "".join(
                f'<a class="text-link" href="{esc(link["url"])}">{esc(link["label"])} →</a>'
                for link in item.get("links", [])
            )
            rows.append(
                f'<details class="faq-item" data-cat="{esc(group)}">'
                f'<summary><span>{esc(item["q"])}</span></summary>'
                f'<div class="faq-answer"><p>{esc(item["a"])}</p>'
                + (f'<p class="faq-links">{links}</p>' if links else "")
                + "</div></details>"
            )
        sections.append(
            f'<section class="faq-group" data-cat="{esc(group)}">'
            f'<h2 class="faq-group-title">{esc(group)}</h2>' + "".join(rows) + "</section>"
        )

    return f"""
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="index.html">Home</a></li><li aria-current="page">Answers</li>
    </ol></nav>
    <h1>Answers</h1>
    <p class="page-lede">
      {len(faq)} questions people actually ask, answered from the same data as the rest of the site. No chatbot,
      no guessing — if the answer is not here, it is not something we claim to know.
    </p>
  </div>
</section>

<section class="section">
  <div class="shell faq-shell">
    <div class="faq-tools">
      <input id="faq-search" class="it-input faq-search" type="search" placeholder="Search the answers" autocomplete="off" aria-label="Search answers">
      <div class="faq-chips">{chips}</div>
    </div>

    <p class="faq-count" id="faq-count">{len(faq)} answers</p>

    <div class="faq-list" id="faq-list">
      {"".join(sections)}
    </div>

    <p class="faq-empty" id="faq-empty" hidden>Nothing matches that. Try a shorter phrase, or use the search on the browse page.</p>

    <p class="calc-fineprint">
      Answers describe how these products work in general. They are not advice, and they do not account for your
      income, tax position or goals. Where a figure is involved it is dated on the page it links to.
    </p>
  </div>
</section>
"""


def jsonld(faq: list) -> str:
    payload = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["q"],
                "acceptedAnswer": {"@type": "Answer", "text": item["a"]},
            }
            for item in faq
        ],
    }
    return '<script type="application/ld+json">' + json.dumps(payload, ensure_ascii=False).replace("</", "<\\/") + "</script>"
