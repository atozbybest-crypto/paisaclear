#!/usr/bin/env python3
"""Build five 20-second vertical ad decks (9:16) for PaisaClear.

Each deck is a PowerPoint file with automatic slide advance, so PowerPoint's
"Export → Create a Video" produces the MP4 with no editing. Voiceover lines sit
in the speaker notes of every slide.

    python tools/build_ads.py
"""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu, Inches, Pt
from pptx.oxml.ns import qn

OUT = Path(__file__).resolve().parent.parent / "ads"

PAPER = RGBColor(0xF7, 0xF4, 0xEC)
INK = RGBColor(0x14, 0x23, 0x1C)
GREEN = RGBColor(0x0F, 0x51, 0x32)
MUTED = RGBColor(0x6B, 0x74, 0x6E)
AMBER = RGBColor(0xB7, 0x79, 0x1F)

SLIDE_SECONDS = 3.3  # six slides ≈ 20 seconds

ADS = [
    {
        "file": "01-rate-without-a-date.pptx",
        "name": "Rate without a date",
        "script": [
            ("8.20%", "Sukanya Samriddhi", "paper", "Eight point two per cent. That is the Sukanya Samriddhi rate."),
            ("But since when?", "", "light", "But a rate means nothing without the date it applied."),
            ("Most sites never say.", "", "light", "Most finance sites quote the number and never tell you when it was last true."),
            ("PaisaClear dates every rate.", "", "paper", "PaisaClear prints the date next to every figure, and links the source."),
            ("Dated. Sourced.", "Every figure, every page", "dark", "Dated and sourced. So you know whether you are reading today's number or last year's."),
            ("paisaclear.co.in", "Understand the product first", "dark", "PaisaClear dot co dot in. Free, no sign up."),
        ],
    },
    {
        "file": "02-ssy-calculator.pptx",
        "name": "The SSY calculator",
        "script": [
            ("₹1,50,000", "a year, for 15 years", "paper", "One and a half lakh a year. For fifteen years."),
            ("15 years", "then it keeps growing", "light", "That is the deposit period. The account keeps earning for six more years."),
            ("₹71,82,119", "at maturity, year 21", "paper", "At eight point two per cent, it reaches seventy-one lakh eighty-two thousand."),
            ("Every rupee accounted for.", "", "light", "Not a headline. A year-by-year table, so you can see where the money came from."),
            ("Change the rate. See the difference.", "", "light", "Because the rate is revised every quarter, not fixed for the term."),
            ("paisaclear.co.in/plans", "Free calculator", "dark", "Try it at PaisaClear dot co dot in slash plans."),
        ],
    },
    {
        "file": "03-fd-vs-ppf-tax.pptx",
        "name": "Same rate, different money",
        "script": [
            ("7.10%", "the rate you see", "paper", "Seven point one per cent. The same headline rate in two products."),
            ("5.04%", "what an FD actually leaves you", "light", "In the thirty per cent slab, a fixed deposit keeps about five per cent after tax."),
            ("7.10%", "what PPF actually leaves you", "paper", "PPF is tax free at every stage. You keep all of it."),
            ("Same number. Different money.", "", "light", "Two products quoting the same rate can leave you two per cent apart, every year."),
            ("See it year by year.", "", "light", "PaisaClear walks the tax through, so the gap is not abstract."),
            ("paisaclear.co.in", "No advice. Just the arithmetic.", "dark", "PaisaClear dot co dot in."),
        ],
    },
    {
        "file": "04-scam-checker.pptx",
        "name": "The scam checker",
        "script": [
            ('"Your account will be blocked in 24 hours."', "", "dark", "Your account will be blocked in twenty-four hours. You have seen this message."),
            ("It is a scam.", "Every time", "light", "No bank switches off an account by SMS, and no bank asks for an OTP."),
            ("Paste it. See the flags.", "", "light", "PaisaClear's checker reads the message and shows which scam patterns it contains."),
            ("OTP request. Fake deadline. Lookalike link.", "Three flags, in one line", "paper", "It names each pattern and explains why it matters."),
            ("Free. Nothing stored.", "Runs in your browser", "light", "Nothing you paste leaves the page."),
            ("paisaclear.co.in/check", "Check a message", "dark", "Try it free at PaisaClear dot co dot in slash check."),
        ],
    },
    {
        "file": "05-compare.pptx",
        "name": "300 products, one place",
        "script": [
            ("300 products.", "One place", "paper", "Three hundred financial products, in one place."),
            ("Schemes. Deposits. Funds. Bonds. Insurance.", "", "light", "Small savings schemes, bank deposits, mutual funds, ETFs, bonds and insurance."),
            ("Compare them side by side.", "", "light", "Rates, lock-ins, tax treatment and risk, in one table."),
            ("No advice.", "No sign up. No payments.", "paper", "We do not sell products, take payments or make accounts."),
            ("Every figure dated.", "Every figure sourced.", "dark", "So the comparison is worth reading."),
            ("paisaclear.co.in", "Understand the product first", "dark", "PaisaClear dot co dot in."),
        ],
    },
]


def _advance(slide, seconds: float) -> None:
    """Make PowerPoint advance this slide automatically."""
    transition = slide.element.makeelement(qn("p:transition"), {"advTm": str(int(seconds * 1000))})
    # p:transition must sit after p:clrMapOvr in the slide XML
    slide.element.append(transition)


def _text(slide, left, top, width, height, text, size, bold, color, align=PP_ALIGN.LEFT, italic=False):
    box = slide.shapes.add_textbox(left, top, width, height)
    frame = box.text_frame
    frame.word_wrap = True
    para = frame.paragraphs[0]
    para.alignment = align
    run = para.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.name = "Georgia"
    run.font.color.rgb = color
    return box


def build(ad: dict) -> Path:
    prs = Presentation()
    prs.slide_width = Inches(7.5)
    prs.slide_height = Inches(13.333)
    blank = prs.slide_layouts[6]

    for index, (headline, sub, tone, voice) in enumerate(ad["script"]):
        slide = prs.slides.add_slide(blank)

        bg = slide.background.fill
        bg.solid()
        bg.fore_color.rgb = PAPER if tone == "paper" else GREEN
        ink = INK if tone == "paper" else PAPER
        second = MUTED if tone == "paper" else RGBColor(0xC9, 0xD8, 0xCF)

        # brand line, top
        _text(slide, Inches(0.6), Inches(0.5), Inches(6.3), Inches(0.4),
              "PAISACLEAR", 11, True, second)

        headline_size = 60 if len(headline) <= 26 else 40
        _text(slide, Inches(0.6), Inches(4.2), Inches(6.3), Inches(3.2),
              headline, headline_size, True, ink)

        if sub:
            _text(slide, Inches(0.6), Inches(7.4), Inches(6.3), Inches(1.2),
                  sub, 20, False, second)

        # progress dots
        for dot in range(len(ad["script"])):
            left = Inches(0.6 + dot * 0.32)
            dot_shape = slide.shapes.add_shape(1, left, Inches(12.2), Inches(0.16), Inches(0.16))
            dot_shape.fill.solid()
            dot_shape.fill.fore_color.rgb = ink if dot == index else second
            dot_shape.line.fill.background()

        slide.notes_slide.notes_text_frame.text = voice
        _advance(slide, SLIDE_SECONDS)

    OUT.mkdir(exist_ok=True)
    path = OUT / ad["file"]
    prs.save(path)
    return path


def main() -> int:
    OUT.mkdir(exist_ok=True)
    for ad in ADS:
        path = build(ad)
        print(f"  {path.name:<34} {len(ad['script'])} slides  ~{len(ad['script']) * SLIDE_SECONDS:.0f}s")

    script_file = OUT / "voiceover-scripts.txt"
    lines = ["PaisaClear — 20 second ad scripts", "=" * 40, ""]
    for ad in ADS:
        lines.append(ad["name"].upper())
        lines.append("-" * 40)
        for i, (headline, sub, tone, voice) in enumerate(ad["script"], 1):
            lines.append(f"{i}. ON SCREEN: {headline}" + (f" / {sub}" if sub else ""))
            lines.append(f"   VOICEOVER: {voice}")
        lines.append("")
    script_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"  {script_file.name:<34} voiceover lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
