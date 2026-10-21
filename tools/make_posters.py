#!/usr/bin/env python3
"""Generate social posters from the site's own data.

Every poster that carries a figure also carries the date and the source, the
same rule the site follows.

    python tools/make_posters.py
"""

from __future__ import annotations

import json
import pathlib

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "social-posters"
SIZE = 1080

PAPER = (247, 244, 236)
INK = (20, 35, 28)
GREEN = (15, 81, 50)
MUTED = (90, 104, 96)
LINE = (214, 208, 194)

FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_SEMI = r"C:\Windows\Fonts\seguisb.ttf"
FONT_REG = r"C:\Windows\Fonts\segoeui.ttf"


def font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def wrap(draw, text: str, fnt, max_width: int) -> list[str]:
    words, lines, current = text.split(), [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit(draw, text: str, path: str, start: int, max_width: int, max_lines: int, min_size: int):
    size = start
    while size > min_size:
        fnt = font(path, size)
        lines = wrap(draw, text, fnt, max_width)
        if len(lines) <= max_lines:
            return fnt, lines, size
        size -= 4
    fnt = font(path, min_size)
    return fnt, wrap(draw, text, fnt, max_width)[:max_lines], min_size


def nice_date(iso: str) -> str:
    try:
        from datetime import date
        d = date.fromisoformat(iso)
        return f"{d.day} {d.strftime('%b %Y')}"
    except Exception:
        return iso


def poster(spec: dict, index: int) -> pathlib.Path:
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, SIZE, 12], fill=GREEN)

    f_brand = font(FONT_BOLD, 38)
    d.text((72, 68), "Paisa", font=f_brand, fill=INK)
    w = d.textlength("Paisa", font=f_brand)
    d.text((72 + w, 68), "Clear", font=f_brand, fill=GREEN)

    if spec.get("chip"):
        f_chip = font(FONT_SEMI, 22)
        chip = spec["chip"].upper()
        cw = d.textlength(chip, font=f_chip)
        d.text((SIZE - 72 - cw, 78), chip, font=f_chip, fill=MUTED)

    # ---- measure every block first, so the group can be centred
    blocks = []
    if spec.get("eyebrow"):
        blocks.append(("eyebrow", spec["eyebrow"].upper(), font(FONT_SEMI, 26), 26, 48, GREEN, True))
    if spec.get("hero"):
        hs = spec.get("hero_size", 168)
        blocks.append(("hero", spec["hero"], font(FONT_BOLD, hs), hs, int(hs * 1.12), INK, False))
    if spec.get("headline"):
        f_head, lines, size = fit(d, spec["headline"], FONT_BOLD, spec.get("headline_size", 62),
                                  SIZE - 144, spec.get("headline_lines", 3), 34)
        blocks.append(("headline", lines, f_head, size, int(size * 1.22), INK, True))
    if spec.get("sub"):
        f_sub, lines, size = fit(d, spec["sub"], FONT_REG, 36, SIZE - 144, 4, 24)
        blocks.append(("sub", lines, f_sub, size, int(size * 1.4), MUTED, True))

    TOP, BOTTOM = 200, SIZE - 240
    total = sum(b[4] * (len(b[1]) if isinstance(b[1], list) else 1) for b in blocks)
    total += 26 * (len(blocks) - 1)

    y = TOP + max(0, (BOTTOM - TOP - total) // 2)

    for kind, content, fnt, size, line_h, colour, multiline in blocks:
        if isinstance(content, list):
            for line in content:
                d.text((72, y), line, font=fnt, fill=colour)
                y += line_h
        else:
            d.text((68 if kind == "hero" else 72, y), content, font=fnt, fill=colour)
            y += line_h
        y += 26

    d.line([(72, SIZE - 220), (SIZE - 72, SIZE - 220)], fill=LINE, width=2)
    d.text((72, SIZE - 186), "paisaclear.co.in", font=font(FONT_BOLD, 44), fill=GREEN)

    f_meta = font(FONT_REG, 24)
    meta_y = SIZE - 120
    for line in spec.get("meta", "").split("|"):
        line = line.strip()
        if line:
            d.text((72, meta_y), line, font=f_meta, fill=MUTED)
            meta_y += 32

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{index:02d}-{spec['slug']}.png"
    img.save(path, "PNG", optimize=True)
    return path


def contact_sheet(paths: list[pathlib.Path]) -> pathlib.Path:
    cols, rows, thumb = 5, 6, 300
    gap = 16
    sheet = Image.new("RGB", (cols * (thumb + gap) + gap, rows * (thumb + gap) + gap), (255, 255, 255))
    for i, p in enumerate(paths[: cols * rows]):
        im = Image.open(p).resize((thumb, thumb), Image.LANCZOS)
        x = gap + (i % cols) * (thumb + gap)
        y = gap + (i // cols) * (thumb + gap)
        sheet.paste(im, (x, y))
    out = OUT / "contact-sheet.png"
    sheet.save(out, "PNG", optimize=True)
    return out


def main() -> int:
    rates = json.loads((ROOT / "content" / "rates.json").read_text(encoding="utf-8"))["values"]

    def rate(key: str) -> str:
        return rates.get(key, {}).get("value", "—")

    def asof(key: str) -> str:
        return nice_date(rates.get(key, {}).get("asOf", ""))

    small_savings_date = asof("ppf")

    specs = [
        {"slug": "ppf-rate", "chip": "Government scheme", "eyebrow": "Public Provident Fund",
         "hero": rate("ppf"), "headline": "Tax-free at all three stages.",
         "sub": "You get the deduction, the interest is not taxed, and the maturity amount is not taxed.",
         "meta": f"Rate notified for the quarter from {small_savings_date} · National Savings Institute"},
        {"slug": "nsc-rate", "chip": "Government scheme", "eyebrow": "National Savings Certificate",
         "hero": rate("nsc"), "headline": "Five years, backed by the government.",
         "sub": "Section 80C on the way in. The interest is taxable at your slab.",
         "meta": f"Rate as of {small_savings_date} · National Savings Institute"},
        {"slug": "ssy-rate", "chip": "Government scheme", "eyebrow": "Sukanya Samriddhi",
         "hero": rate("ssy"), "headline": "For a daughter under ten.",
         "sub": "The highest rate in the small-savings family, and entirely tax-free.",
         "meta": f"Rate as of {small_savings_date} · National Savings Institute"},
        {"slug": "scss-rate", "chip": "Government scheme", "eyebrow": "Senior Citizens' Savings",
         "hero": rate("scss"), "headline": "Paid out every quarter.",
         "sub": "Open to anyone over 60. Interest is taxable, 80C applies on the deposit.",
         "meta": f"Rate as of {small_savings_date} · National Savings Institute"},
        {"slug": "kvp-rate", "chip": "Government scheme", "eyebrow": "Kisan Vikas Patra",
         "hero": rate("kvp"), "headline": "Money doubles in about 115 months.",
         "sub": "A government certificate with no market risk and no early exit.",
         "meta": f"Rate as of {small_savings_date} · National Savings Institute"},
        {"slug": "mis-rate", "chip": "Government scheme", "eyebrow": "Post Office MIS",
         "hero": rate("mis"), "headline": "Monthly income from the post office.",
         "sub": "Deposit a lump sum and receive the interest every month.",
         "meta": f"Rate as of {small_savings_date} · National Savings Institute"},
        {"slug": "po-td", "chip": "Government scheme", "eyebrow": "Post Office Time Deposit",
         "hero": rate("po-td-5y"), "headline": "Five years, no market risk.",
         "sub": "The five-year deposit also counts towards 80C.",
         "meta": f"Rate as of {small_savings_date} · National Savings Institute"},
        {"slug": "gsec-2041", "chip": "Bonds", "eyebrow": "Government of India",
         "hero": "7.06%", "headline": "A 15-year government bond.",
         "sub": "7.06% coupon paid twice a year, face value repaid in 2041. The market yield moves daily.",
         "meta": f"Yield {rate('gs-2041')} as of {asof('gs-2041')} · RBI Retail Direct",
         "hero_size": 150},
        {"slug": "tbill", "chip": "Bonds", "eyebrow": "Treasury Bill",
         "hero": "6.49%", "headline": "A one-year government borrowing.",
         "sub": "Bought at a discount, repaid at face value. No payments in between.",
         "meta": f"Cut-off yield as of {asof('tbill-364')} · RBI"},
        {"slug": "sgb", "chip": "Bonds", "eyebrow": "Sovereign Gold Bond",
         "hero": "Gold + 2.5%", "headline": "A bond priced in grams.",
         "sub": "The coupon is fixed. The redemption value follows the gold price, so capital is not protected.",
         "meta": "Issued in tranches by the RBI · terms per tranche", "hero_size": 110},
        {"slug": "fd-vs-ppf", "chip": "Comparison", "eyebrow": "The tax arithmetic",
         "headline": "An FD needs 10.1% to beat a 7.1% PPF.",
         "sub": "PPF interest is tax-free. FD interest is taxed at your slab every year.",
         "meta": f"PPF rate as of {small_savings_date} · after-tax arithmetic at a 30% slab",
         "headline_size": 66},
        {"slug": "regime", "chip": "Tax", "eyebrow": "Old vs new regime",
         "hero": "₹50,000", "headline": "What the new regime saves at ₹15 lakh.",
         "sub": "Even with ₹3.5 lakh of deductions, the old regime comes out behind.",
         "meta": "FY 2026-27 slabs · after 4% cess", "hero_size": 128},
        {"slug": "salary-calc", "chip": "Calculator", "eyebrow": "Free tool",
         "headline": "CTC to take-home, in one screen.",
         "sub": "Both tax regimes side by side, with HRA, 80C, 80D and home-loan interest.",
         "meta": "paisaclear.co.in/calculators/salary", "headline_size": 76},
        {"slug": "sip-math", "chip": "Calculator", "eyebrow": "Monthly investing",
         "hero": "₹9.2 lakh", "headline": "₹5,000 a month for 10 years at 8%.",
         "sub": "₹6 lakh put in. The rest is compounding — and no fund earns 8% every year.",
         "meta": "Illustrative arithmetic, not a forecast", "hero_size": 130},
        {"slug": "sip-vs-lump", "chip": "Guide", "eyebrow": "SIP vs lump sum",
         "headline": "Same fund. Very different experience.",
         "sub": "A SIP spreads the timing risk. A lump sum concentrates it on one day.",
         "meta": "Full comparison on the site", "headline_size": 68},
        {"slug": "emi", "chip": "Calculator", "eyebrow": "Loan EMI",
         "hero": "₹17,356", "headline": "₹20 lakh at 8.5% for 20 years.",
         "sub": "Total interest ₹21.6 lakh — more than the loan. The schedule shows every year.",
         "meta": "Reducing-balance arithmetic · not a lender quote", "hero_size": 128},
        {"slug": "emergency", "chip": "Planner", "eyebrow": "Emergency fund",
         "headline": "How many months could you cover?",
         "sub": "Enter your own expenses and months. It tells you the gap and the monthly saving.",
         "meta": "No account needed · nothing leaves your browser", "headline_size": 60},
        {"slug": "retirement", "chip": "Planner", "eyebrow": "Retirement",
         "hero": "₹1.72 lakh", "headline": "What ₹40,000 a month becomes at 60.",
         "sub": "At 5% inflation over 30 years. Then see what corpus it needs.",
         "meta": "Your inflation, your returns, your numbers", "hero_size": 118},
        {"slug": "spending", "chip": "Planner", "eyebrow": "Spending planner",
         "headline": "See where the month actually goes.",
         "sub": "Log a spend, get the category split, and the products your balance can reach.",
         "meta": "Stored in your browser only · no sign-up", "headline_size": 64},
        {"slug": "catalogue", "chip": "Catalogue", "eyebrow": "PaisaClear",
         "hero": "226", "headline": "products, every figure dated.",
         "sub": "Six categories. Where a number varies, we link to the source instead of inventing one.",
         "meta": "paisaclear.co.in", "hero_size": 200},
        {"slug": "three-types", "chip": "Explainer", "eyebrow": "The one idea to start with",
         "headline": "Guaranteed. Conditional. Market-linked.",
         "sub": "Mixing these up is where most beginners get hurt. Every product says which it is.",
         "meta": "Explained in plain language", "headline_size": 64},
        {"slug": "dicgc", "chip": "Safety", "eyebrow": "Deposit insurance",
         "hero": "₹5 lakh", "headline": "The most a bank deposit is insured for.",
         "sub": "Per depositor, per bank, across all your accounts with that bank.",
         "meta": "DICGC · statutory limit", "hero_size": 186},
        {"slug": "no-selling", "chip": "About", "eyebrow": "How this site works",
         "headline": "We don't sell anything.",
         "sub": "No payments, no accounts, no personalised advice. Every figure carries a date and a source.",
         "meta": "Read the method at paisaclear.co.in", "headline_size": 72},
        {"slug": "ppf-guide", "chip": "Guide", "eyebrow": "PPF vs FD vs NSC",
         "headline": "Three safe places. Not interchangeable.",
         "sub": "Rate, term, tax and access side by side — with the after-tax arithmetic.",
         "meta": "paisaclear.co.in/guides", "headline_size": 66},
        {"slug": "saral-pension", "chip": "Insurance", "eyebrow": "LIC Saral Pension",
         "headline": "Pension for life, capital returned.",
         "sub": "An IRDAI standard annuity: identical terms at every insurer, so the rate is the only difference.",
         "meta": "UIN 512N342V05 · terms per LIC", "headline_size": 62},
        {"slug": "annuity", "chip": "Insurance", "eyebrow": "Immediate annuity",
         "headline": "A pension that starts next month.",
         "sub": "You pay once, the income is fixed for life. The rate is locked on the day you buy.",
         "meta": "LIC Jeevan Akshay-VII · UIN 512N337V07", "headline_size": 62},
        {"slug": "nps", "chip": "Retirement", "eyebrow": "National Pension System",
         "headline": "Two tiers, one retirement account.",
         "sub": "Tier I is locked until 60. Tier II is the one you can withdraw from.",
         "meta": "Regulated by PFRDA · rules per tier", "headline_size": 64},
        {"slug": "pmjjby", "chip": "Government scheme", "eyebrow": "PMJJBY",
         "headline": "Life cover for a small annual premium.",
         "sub": "₹2 lakh cover through your bank account, renewed every year.",
         "meta": "Terms and premium per the scheme notification", "headline_size": 62},
        {"slug": "apy", "chip": "Government scheme", "eyebrow": "Atal Pension Yojana",
         "headline": "A pension you build month by month.",
         "sub": "Contribution depends on your age and the pension you choose. The government guarantees the amount.",
         "meta": "Terms per PFRDA notification", "headline_size": 62},
        {"slug": "start-here", "chip": "Start", "eyebrow": "New to all this?",
         "headline": "Start with the product, not the pitch.",
         "sub": "Look a product up, run a calculator, or read how the figures are sourced.",
         "meta": "paisaclear.co.in/start", "headline_size": 68},
    ]

    paths = [poster(spec, i + 1) for i, spec in enumerate(specs)]
    sheet = contact_sheet(paths)
    print(f"posters: {len(paths)} -> {OUT}")
    print("contact sheet:", sheet.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
