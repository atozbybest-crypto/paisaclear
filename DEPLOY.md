# Going live

Two routes. **Route A needs no tools** and puts the site online in about two minutes. Route B
connects the repo so the daily rate refresh runs by itself.

The folder that gets published is `site/`. Never the project root — the root contains Python and
content files that should not be served.

---

## Route A — Netlify Drop, no git, no account setup first

1. Open **https://app.netlify.com/drop**
2. Drag the **`site`** folder onto the page.
   (Or drag `paisaclear-site.zip` from this folder — Netlify unpacks it.)
3. You get a URL like `https://sparkly-fox-1a2b3c.netlify.app`. That is the live site.

Done. Add the custom domain whenever you like.

**Limitation:** Netlify Drop does not watch for changes. When the rates refresh, you re-drop the
folder. Use Route B for automatic updates.

---

## Route B — GitHub repo, then Netlify or Render

### B1. Get the code into a repo

No git is installed on this machine. Pick one:

**Option 1 — GitHub Desktop** (bundles git, easiest)
1. Install GitHub Desktop, sign in.
2. **File → Add local repository** → choose this folder.
3. It will say "not a git repository" → click **create a repository here**.
4. Commit everything, then **Publish repository**.

**Option 2 — Git for Windows**
```powershell
winget install --id Git.Git -e
cd C:\Users\Gowtham_Sravya\Documents\deepseek-harness\default-workspace\paisaclear
git init -b main
git add .
git commit -m "PaisaClear: initial site"
git remote add origin https://github.com/<you>/paisaclear.git
git push -u origin main
```

**Option 3 — GitHub web upload** (no tools, slowest)
Create the repo, click **Add file → Upload files**, then drag the **contents** of this folder into
the browser. Subfolders are preserved.

### B2. Connect the host

**Netlify**
1. **Add new site → Import an existing project → GitHub** → pick the repo.
2. Build command: leave **empty**.
3. Publish directory: **`site`**.
4. Deploy. `netlify.toml` already sets these, so they should pre-fill.

**Render**
1. **New → Static Site** → connect the repo.
2. Build command: leave **empty**.
3. Publish directory: **`site`**.
4. Deploy. `render.yaml` is there if you prefer a Blueprint instead.

Both redeploy automatically on every push — which is exactly what the refresh workflow does.

### B3. Turn on the rate refresh

Repo → **Settings → Actions → General → Workflow permissions** → *Read and write*.

Then **Actions → Refresh rates and redeploy → Run workflow** once to confirm it works. Job runs daily
at 07:00 IST (`cron: "30 1 * * *"` in `.github/workflows/refresh.yml`).

`quarterly-reminder.yml` opens an issue on your repo each quarter so the small-savings rates get
checked.

---

## Custom domain on GoDaddy

Do this after the site is live on a `*.netlify.app` or `*.onrender.com` address.

1. In Netlify/Render: **Domain settings → Add custom domain** → enter `paisaclear.in` (or yours).
   The panel then shows the exact DNS values to use — **always copy them from there**, because hosts
   occasionally change IPs.
2. In GoDaddy: **My Products → Domains → DNS** for that domain.
3. Add these records (typical values; confirm against the host panel):

   | Type | Name | Value | TTL |
   |---|---|---|---|
   | A | `@` | Netlify `75.2.60.5` / Render `216.24.57.1` | 600 |
   | CNAME | `www` | `your-site.netlify.app` / `your-site.onrender.com` | 600 |

4. **Delete GoDaddy's default parking records** — the "WebsiteBuilder" A record and any `@` CNAME.
   These are the usual cause of a domain that "doesn't update".
5. Wait for propagation (minutes to a couple of hours). Check with `nslookup paisaclear.in`.
6. Back in the host: enable **HTTPS** (both issue a free certificate automatically once DNS resolves).

**Don't** touch the nameservers unless you want GoDaddy to stop managing DNS entirely — leave them
on GoDaddy's defaults and use the A/CNAME records above.

### WWW vs non-WWW

Pick one and redirect the other in the host's domain settings. Netlify does this for you under
*Domain management → Primary domain*.

---

## After go-live checklist

- [ ] `https://your-domain/` loads and the five category cards show product counts
- [ ] A product page opens and the **Source** link goes to the right provider page
- [ ] `https://your-domain/anything` shows your 404 page, not the host's default
- [ ] `robots.txt` is reachable
- [ ] HTTPS padlock shows, and `http://` redirects to `https://`
- [ ] The daily Actions run has gone green at least once
- [ ] GoDaddy auto-renew is on, and the registrant email is one you read

---

## Rebuilding after content changes

```bash
python build.py        # regenerates site/ (42 pages)
python bundle.py       # regenerates PaisaClear.html
```

Commit both, push, and the host redeploys. The refresh workflow does the rate part on its own.
