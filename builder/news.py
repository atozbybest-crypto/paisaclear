"""Money News page — headlines from Indian finance publishers, refreshed daily."""

from __future__ import annotations

from datetime import datetime

from .site import esc


def _when(iso: str) -> str:
    try:
        stamp = datetime.fromisoformat(iso)
        return stamp.strftime("%d %b, %H:%M")
    except (TypeError, ValueError):
        return ""


def page(news: dict) -> str:
    items = news.get("items", [])
    updated = news.get("updatedAt", "")
    sections = []
    for item in items:
        if item["section"] not in sections:
            sections.append(item["section"])

    chips = '<button class="faq-chip is-on" type="button" data-news-cat="all">All</button>' + "".join(
        f'<button class="faq-chip" type="button" data-news-cat="{esc(s)}">{esc(s)}</button>'
        for s in sections
    )

    cards = []
    for item in items:
        cards.append(f"""
<a class="news-item" href="{esc(item['link'])}" target="_blank" rel="noopener noreferrer" data-cat="{esc(item['section'])}">
  <p class="news-meta"><span class="news-source">{esc(item['source'])}</span>
     <span class="news-section">{esc(item['section'])}</span>
     <span class="news-time">{esc(_when(item['published']))}</span></p>
  <p class="news-title">{esc(item['title'])}</p>
  {f'<p class="news-summary">{esc(item["summary"])}</p>' if item.get("summary") else ''}
</a>""")

    return f"""
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="index.html">Home</a></li><li aria-current="page">Money news</li>
    </ol></nav>
    <h1>Money news</h1>
    <p class="page-lede">
      Markets, policy and personal money, collected from Indian finance publishers each morning.
      Headlines and links only — the reporting stays with them.
    </p>
    <p class="page-meta">Updated {esc(_when(updated))} IST · {len(items)} stories</p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="faq-tools">
      <div class="faq-chips">{chips}</div>
    </div>

    <div class="news-grid" id="news-grid">
      {"".join(cards)}
    </div>

    <p class="calc-fineprint">
      Headlines link to the original publisher. PaisaClear does not write or edit these stories, and a link
      here is not an endorsement. Sources: Economic Times, Livemint, Business Standard, Moneycontrol, RBI.
    </p>
  </div>
</section>
"""
