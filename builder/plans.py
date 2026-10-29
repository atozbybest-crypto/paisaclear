"""Plans hub — one page per scheme we cover in depth."""

from __future__ import annotations

from .site import esc, icon


def page(plans: list) -> str:
    cards = "".join(
        f"""<a class="plan-card" href="plans/{esc(p['slug'])}.html">
  <span class="plan-tag">{esc(p['tag'])}</span>
  <span class="plan-name">{esc(p['name'])}</span>
  <span class="plan-line">{esc(p['line'])}</span>
  <span class="plan-meta">{esc(p['meta'])}</span>
  <span class="plan-cta">Read the guide {icon("arrow", "icon icon-sm")}</span>
</a>"""
        for p in plans
    )

    return f"""
<section class="page-head">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
      <li><a href="index.html">Home</a></li><li aria-current="page">Plans</li>
    </ol></nav>
    <h1>Plans, explained in full</h1>
    <p class="page-lede">
      One page per scheme: who can open it, how the money works, what the rules allow, and a calculator that
      shows the arithmetic rather than a single number.
    </p>
    <p class="page-meta">{len(plans)} guide{"s" if len(plans) != 1 else ""} · more being added</p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="plan-grid">{cards}</div>

    <div class="plan-soon">
      <h2 class="subhead">Coming next</h2>
      <p class="muted">
        Public Provident Fund, Senior Citizens' Savings Scheme, National Savings Certificate and the Post
        Office Monthly Income Scheme are next in line, each with the same treatment and its own calculator.
      </p>
      <p class="muted">
        In the meantime, the <a href="rates.html">rates page</a> carries every scheme's current rate with the
        date it applied.
      </p>
    </div>
  </div>
</section>
"""
