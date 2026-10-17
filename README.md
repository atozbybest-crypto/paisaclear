# PaisaClear

A responsive discovery and information site for Indian financial products, written for people who are
new to them. Real products, real rates, every figure dated and linked to its source.

**Not financial advice.** No payments, no accounts, no recommendations.

---

## Run it

### The quick way — one file, nothing installed

Double-click **`PaisaClear.html`**.

The entire site in a single 164 KB file: all CSS, all 32 products, the comparison table and the router.
Works from a USB stick, an email attachment, or a folder with no internet.

### The full way — the multi-page site

```bash
python build.py        # generate pages into site/
python serve.py        # serve them and open the browser
```

Or double-click **`start.bat`** (Windows) / run `start.ps1`. It finds Python, starts the server on the
first free port and opens the browser.

This version has real URLs (`/products/…`, `/categories/…`), works without JavaScript, and is the one
to put on a domain later.

Requires Python 3.12+ (standard library only).

---

## What is actually on the site

| Category | Products | Figure shown |
|---|---|---|
| Government & Post Office Schemes | 9 | Notified rate, dated quarterly |
| Government Bonds & Fixed-Income | 8 | Market yield from the RBI |
| Bank Savings & Fixed Deposits | 5 | **Link to the bank's own rate card** |
| Mutual Funds | 5 | AMFI NAV, dated daily |
| ETFs & Market-Linked | 5 | AMFI NAV, dated daily |

Bank deposits are the one place a number is deliberately withheld. The rate depends on the bank, the
tenure and the deposit slab, and the banks' own pages render their charts in JavaScript, so any figure
we quoted would be wrong for most readers. Each bank entry links straight to that bank's rate card
instead. Everywhere else the figure is a dated number with a source.

### Where the numbers come from

| Source | What it gives | How it updates |
|---|---|---|
| `rbi.org.in` | G-Sec yields, T-bill cut-offs, policy rates | `python refresh_rbi.py` |
| AMFI NAV file (via `api.mfapi.in`) | Mutual fund and ETF NAVs | Fetched per scheme, dated |
| Small-savings notification | PPF, NSC, SSY, SCSS, KVP, MIS, PO TD rates | Entered by hand each quarter |
| Bank rate cards | Deposit rates, tenure by tenure | Linked, not copied |

Every value in `content/rates.json` carries `asOf` (the date it applied), `cadence` (how often it
changes) and `sourceUrl`. The UI shows all three. Verified on **17 October 2026**:

- Small savings for Oct–Dec 2026: PPF 7.10%, NSC 7.70%, SSY 8.20%, SCSS 8.20%, KVP 7.50%, MIS 7.40%, PO TD (5y) 7.50%
- RBI, as on 15–16 Oct 2026: 91-day T-bill 5.7281%, 182-day 6.2896%, 364-day 6.4891%; 6.20% GS 2029 at 6.8845%, 6.94% GS 2036 at 7.3865%, 7.63% GS 2056 at 7.7811%

The NSI site is not machine-readable from this environment, so the small-savings values were confirmed
via published reporting of the 1 October notification. `rates.json` records that provenance
(`confirmedVia`) rather than pretending the figure came from a primary feed.

---

## Refreshing rates

```bash
python refresh_rbi.py --dry-run    # fetch, show what would change
python refresh_rbi.py              # write rates.json
python build.py && python bundle.py
```

The refresh job parses the RBI homepage for named securities (`6.94% GS 2036 : 7.3865%`), T-bill
cut-offs and the `as on` date. If the page cannot be fetched or nothing is recognised, it exits 1 and
leaves `rates.json` untouched — a failed refresh never silently blanks a rate.

Only entries whose feed is `rbi` are touched. The quarterly small-savings values stay exactly as
entered until a person updates them, which is correct: they change four times a year, not daily.

### Keeping it current once it is public

`.github/workflows/refresh.yml` runs the whole chain on GitHub's servers at 07:00 IST every day:
pull RBI rates → rebuild → check freshness → commit → your host redeploys. No laptop needs to be on,
and nothing needs checking by hand.

| Part | Automatic? |
|---|---|
| Bond yields and T-bill cut-offs | Yes — daily |
| Rebuild and redeploy | Yes — on every successful run |
| Small-savings rates | No — four times a year, about two minutes |

`tools/check_freshness.py` fails the run if any published rate is older than its own cycle — 10 days
for market yields, 100 days for quarterly small savings. So a stopped cron, a changed RBI layout, or a
forgotten January update shows up as a red workflow and an email, not as quietly stale numbers on the
live site.

To set it up: push this folder to GitHub, connect the repo to Cloudflare Pages (or Netlify), and the
scheduled job does the rest. See **Deploying** below.

---

## Content model

```
content/
├─ categories.json     5 categories; `status: live|guide`, icons, "what to check"
├─ return-types.json   guaranteed / conditional / market-linked
├─ collections.json    discovery collections
├─ products.json       one record per product
└─ rates.json          the current rate for each product, with provenance
```

A product references a rate rather than storing one:

```json
{
  "slug": "public-provident-fund",
  "name": "Public Provident Fund (PPF)",
  "category": "government-schemes",
  "returnType": "guaranteed",
  "rateKey": "ppf",
  "minInvestment": 500,
  "tenure": "15 years",
  "review": { "status": "approved", "reviewer": "…", "approvedAt": "2026-10-17" }
}
```

and `rates.json` holds:

```json
"ppf": {
  "value": "7.10%",
  "label": "Interest rate",
  "asOf": "2026-10-01",
  "cadence": "Notified quarterly; current for Oct–Dec 2026",
  "sourceUrl": "https://www.nsiindia.gov.in/",
  "sourceLabel": "National Savings Institute",
  "confirmedVia": "Outlook Money, 1 October 2026"
}
```

Keeping them apart means a rate refresh never touches editorial copy, and an editorial edit can never
change a number by accident. The build fails if a published product points at a rate that does not exist.

---

## The approval gate

`review.status` decides what can reach the site:

- `draft` — being researched
- `pending` — researched, waiting for a second check
- `approved` — signed off with a reviewer name and date (rendered)
- `rejected` — kept for the record, never rendered

```bash
python tools/review.py list
python tools/review.py show public-provident-fund
python tools/review.py approve <slug>
python tools/review.py reset <slug>     # back to pending; rebuild removes the page
python build.py
```

The build deletes `site/products/` and `site/categories/` before regenerating, so a record that loses
approval cannot leave a live page behind. There is one `pending` record in the repo
(`treasury-bill-182-day`) so the gate is visible in the build output.

Validation on every build: required fields, slug format, duplicate slugs, unknown categories,
collections or rate keys, approved records without a reviewer or date, and source URLs that are not
`http(s)`.

---

## Adding a product

1. Add the rate to `content/rates.json` with `value`, `asOf`, `cadence`, `sourceUrl`, `sourceLabel`.
2. Append the product to `content/products.json` with `review.status: "draft"` and the matching `rateKey`.
3. Fill every field; keep `sources` to primary sources.
4. Move to `pending` after a second read-through.
5. `python tools/review.py approve <slug>`, then `python build.py && python bundle.py`.

Writing rules:

- Never state a rate without an `asOf` date and a source.
- No "best", "should", "recommended", "safe". Describe trade-offs.
- Keep `risks` specific to the product.
- Update `lastVerified` whenever a field changes.

Moving a guide category to live: set `"status": "live"` in `categories.json`, remove its `guide` block,
add product records, rebuild.

---

## Design decisions

**Rate first, on every card.** A number without a date is a claim. The card shows the rate and "as of",
the product page shows the cadence and both the primary link and how it was confirmed.

**Return type is the primary filter.** Guaranteed, conditional and market-linked explain a product
better than its category does.

**Guide pages rather than invented data.** A category with no verifiable feed ships as an explanation
with links, not as a list of approximate numbers.

**Works without JavaScript.** The multi-page build renders everything into HTML; only filtering and the
comparison table need JS.

**No analytics, cookies or third-party requests.**

---

## Deploying

See **[DEPLOY.md](DEPLOY.md)** for the full walkthrough — Netlify Drop, GitHub + Netlify/Render, and
the GoDaddy DNS records.

The short version: publish the **`site/`** folder (not the project root), leave the build command
empty, and set the publish directory to `site`. `netlify.toml` and `render.yaml` are already
configured for that.

`site/assets/` is hand-authored; only HTML is generated. Nothing in the build needs to know the domain.

Before going live, decide how often `refresh_rbi.py` runs. Daily is reasonable for bond yields; the
small-savings values need a calendar reminder four times a year (1 April, 1 July, 1 October, 1 January).

---

## Known limitations

- **Bank deposit rates are not published as numbers**, only linked. That is a deliberate trade: a
  number would be stale within days and wrong for most deposit slabs.
- **NAV is not a return.** A higher NAV than another fund means nothing; the site is careful not to
  imply otherwise.
- **Minimum investment is marked "typical"** for funds and banks, because it varies by scheme and
  channel. Confirm on the provider's page.
- **Small-savings rates are entered by hand**, so they are only as current as the last edit. The
  `asOf` date makes the lag visible rather than hidden.
- **G-Sec availability varies.** What is on offer through RBI Retail Direct changes; the records describe
  the security, not whether it is currently purchasable.
- **No pre-rendered sitemap** until a domain exists.
- **The single-file build renders with JavaScript.** The `site/` build does not.
