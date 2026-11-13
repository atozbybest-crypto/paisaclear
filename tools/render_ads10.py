#!/usr/bin/env python3
"""Render ten dramatic 20-second vertical ads for PaisaClear.

Every frame is drawn in code — no footage, no people. Each ad mixes five visual
templates so they don't look alike: big number count-ups, growing comparison
bars, kinetic word reveals, manifesto lines, and dark punch cuts.

    python tools/render_ads10.py           # all ten
    python tools/render_ads10.py 03        # one ad
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "ads" / "videos"
W, H = 1080, 1920
FPS = 30
SECONDS = 20.0
TOTAL = int(FPS * SECONDS)

PAPER = (247, 244, 236)
INK = (20, 35, 28)
GREEN = (15, 81, 50)
DEEP = (10, 32, 22)
MUTED = (107, 116, 110)
SOFT = (201, 216, 207)
AMBER = (214, 158, 46)
RED = (140, 40, 28)

FB = "C:/Windows/Fonts/georgiab.ttf"
FR = "C:/Windows/Fonts/georgia.ttf"
FU = "C:/Windows/Fonts/segoeuib.ttf"
FUN = "C:/Windows/Fonts/segoeui.ttf"

_cache: dict = {}


def font(path: str, size: int):
    key = (path, size)
    if key not in _cache:
        try:
            _cache[key] = ImageFont.truetype(path, size)
        except OSError:
            _cache[key] = ImageFont.load_default()
    return _cache[key]


def indian(n: int) -> str:
    s = str(int(n))
    if len(s) <= 3:
        return s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return ",".join(parts) + "," + tail


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def ease_out_back(t: float) -> float:
    t = max(0.0, min(1.0, t))
    c = 1.9
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2


def wrap(draw, text, fnt, max_width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def palette(tone: str):
    return {
        "paper": (PAPER, INK, MUTED),
        "green": (GREEN, PAPER, SOFT),
        "deep": (DEEP, PAPER, SOFT),
        "red": (RED, PAPER, (240, 200, 194)),
    }[tone]


def centered(draw, lines, fnt, ink, y, line_gap=None, alpha=1.0, bg=None):
    gap = line_gap or fnt.size * 1.16
    for line in lines:
        width = draw.textlength(line, font=fnt)
        draw.text(((W - width) / 2, y), line, font=fnt, fill=ink)
        y += gap
    return y


def brand(draw, second, key_index, total):
    draw.text((72, 92), "PAISACLEAR", font=font(FU, 28), fill=second)
    draw.text((W - 118, 92), f"{key_index}/{total}", font=font(FU, 24), fill=second)


def progress(draw, overall, bg, second):
    y = H - 70
    mid = tuple(int((bg[i] + second[i]) / 2) for i in range(3))
    draw.rectangle([72, y, W - 72, y + 5], fill=mid)
    draw.rectangle([72, y, 72 + (W - 144) * max(0.0, min(1.0, overall)), y + 5], fill=AMBER)


# ---------------------------------------------------------------- templates

def t_big(frame, spec, local):
    headline, sub, tone, count_to, prefix, suffix = spec
    bg, ink, second = palette(tone)
    draw = ImageDraw.Draw(frame)
    draw.rectangle([0, 0, W, H], fill=bg)

    text = headline
    if count_to is not None:
        p = ease(min(1.0, local / 1.5))
        value = count_to * p
        if count_to >= 1000:
            text = f"{prefix}{indian(int(round(value)))}{suffix}"
        elif count_to < 20:
            text = f"{prefix}{value:.2f}{suffix}"
        else:
            text = f"{prefix}{int(round(value))}{suffix}"

    size = 118
    fnt = font(FB, size)
    lines = wrap(draw, text, fnt, W - 170)
    while len(lines) > 3 and size > 56:
        size -= 10
        fnt = font(FB, size)
        lines = wrap(draw, text, fnt, W - 170)

    slide = int((1 - ease(min(1.0, local / 0.6))) * 60)
    y = 700 + slide
    width_one = max(draw.textlength(l, font=fnt) for l in lines)
    scale = ease_out_back(min(1.0, local / 0.8))
    if scale < 1.0:
        y += int((1 - scale) * 30)
    centered(draw, lines, fnt, ink, y)

    if sub:
        a = ease(min(1.0, max(0.0, (local - 0.4) / 0.7)))
        if a > 0:
            sfnt = font(FR, 42)
            slines = wrap(draw, sub, sfnt, W - 240)
            tint = tuple(int(bg[i] + (second[i] - bg[i]) * a) for i in range(3))
            centered(draw, slines, sfnt, tint, y + len(lines) * size * 1.16 + 34)
    return draw, bg, ink, second


def t_punch(frame, spec, local):
    headline, tone = spec
    bg, ink, second = palette(tone)
    draw = ImageDraw.Draw(frame)
    draw.rectangle([0, 0, W, H], fill=bg)
    px = ease(min(1.0, local / 0.45))
    size = int(150 * (0.55 + 0.45 * ease_out_back(px)))
    fnt = font(FB, size)
    lines = wrap(draw, headline, fnt, W - 150)
    while len(lines) > 4 and size > 70:
        size -= 12
        fnt = font(FB, size)
        lines = wrap(draw, headline, fnt, W - 150)
    centered(draw, lines, fnt, ink, 760)
    return draw, bg, ink, second


def t_bars(frame, spec, local):
    title, bars, tone = spec
    bg, ink, second = palette(tone)
    draw = ImageDraw.Draw(frame)
    draw.rectangle([0, 0, W, H], fill=bg)

    tf = font(FR, 44)
    tlines = wrap(draw, title, tf, W - 200)
    y = 480
    for line in tlines:
        width = draw.textlength(line, font=tf)
        draw.text(((W - width) / 2, y), line, font=tf, fill=second)
        y += 58

    base_y = 1400
    max_val = max(v for _, v, _ in bars) or 1
    bar_w = 190
    gap = (W - 200 - bar_w * len(bars)) // (len(bars) + 1)
    for i, (label, value, colour) in enumerate(bars):
        grow = ease(min(1.0, max(0.0, (local - 0.35 - i * 0.25) / 1.1)))
        height = int((base_y - 760) * (value / max_val) * grow)
        x = 100 + gap + i * (bar_w + gap)
        draw.rectangle([x, base_y - height, x + bar_w, base_y], fill=colour)
        fnt_val = font(FB, 46)
        vtext = f"{value:.2f}%" if value < 100 else indian(int(value))
        vw = draw.textlength(vtext, font=fnt_val)
        if grow > 0.15:
            draw.text((x + bar_w / 2 - vw / 2, base_y - height - 70), vtext, font=fnt_val, fill=ink)
        fnt_lab = font(FUN, 30)
        lw = draw.textlength(label, font=fnt_lab)
        draw.text((x + bar_w / 2 - lw / 2, base_y + 26), label, font=fnt_lab, fill=second)
    return draw, bg, ink, second


def t_words(frame, spec, local):
    words, tone = spec
    bg, ink, second = palette(tone)
    draw = ImageDraw.Draw(frame)
    draw.rectangle([0, 0, W, H], fill=bg)
    per = 1.15
    y = 700
    for i, word in enumerate(words):
        start = 0.2 + i * per
        a = ease(min(1.0, max(0.0, (local - start) / 0.5)))
        if a <= 0:
            continue
        size = 96 if len(word) < 16 else 64
        fnt = font(FB, size)
        tint = tuple(int(bg[j] + (ink[j] - bg[j]) * a) for j in range(3))
        draw.text((100 + int((1 - a) * 40), y), word, font=fnt, fill=tint)
        y += size * 1.25
    return draw, bg, ink, second


def t_manifesto(frame, spec, local):
    lines, tone = spec
    bg, ink, second = palette(tone)
    draw = ImageDraw.Draw(frame)
    draw.rectangle([0, 0, W, H], fill=bg)
    y = 620
    for i, line in enumerate(lines):
        a = ease(min(1.0, max(0.0, (local - 0.25 - i * 0.55) / 0.6)))
        if a <= 0:
            continue
        size = 62 if i < len(lines) - 1 else 78
        fnt = font(FB if i == len(lines) - 1 else FR, size)
        tint = tuple(int(bg[j] + (ink[j] - bg[j]) * a) for j in range(3))
        wrapped = wrap(draw, line, fnt, W - 200)
        for piece in wrapped:
            draw.text((100, y + int((1 - a) * 24)), piece, font=fnt, fill=tint)
            y += size * 1.2
        y += 26
    return draw, bg, ink, second


TEMPLATES = {"big": t_big, "punch": t_punch, "bars": t_bars, "words": t_words, "manifesto": t_manifesto}


# ---------------------------------------------------------------- the ten ads

ADS = [
    {"key": "01", "file": "01-rate-without-a-date.mp4", "scenes": [
        ("big", ("8.20%", "Sukanya Samriddhi, today", "paper", 8.20, "", "%")),
        ("punch", ("But since when?", "deep")),
        ("words", (["Most sites", "quote the number.", "Never the date."], "paper")),
        ("big", ("Dated.", "every figure, every page", "green", None, "", "")),
        ("manifesto", (["Rates change.", "We tell you when.", "paisaclear.co.in"], "deep")),
    ]},
    {"key": "02", "file": "02-ssy-lakh-to-crore.mp4", "scenes": [
        ("big", ("₹1,50,000", "a year, for 15 years", "paper", 150000, "₹", "")),
        ("big", ("₹71,82,119", "at maturity, year 21", "green", 7182119, "₹", "")),
        ("bars", ("Deposit vs growth", [("You put in", 2250000, INK), ("Interest", 4932119, AMBER)], "paper")),
        ("punch", ("See the working.", "deep")),
        ("manifesto", (["Free calculator.", "Year by year.", "paisaclear.co.in/plans"], "paper")),
    ]},
    {"key": "03", "file": "03-fd-vs-ppf.mp4", "scenes": [
        ("big", ("7.10%", "the rate you see", "paper", 7.10, "", "%")),
        ("bars", ("What you actually keep", [("Fixed deposit", 5.04, RED), ("PPF", 7.10, GREEN)], "paper")),
        ("punch", ("Same rate. Different money.", "deep")),
        ("words", (["The tax", "decides it."], "paper")),
        ("manifesto", (["Work out your own", "after-tax return.", "paisaclear.co.in"], "green")),
    ]},
    {"key": "04", "file": "04-nobody-reads-the-brochure.mp4", "scenes": [
        ("words", (["Nobody reads", "the brochure."], "deep")),
        ("punch", ("The claim is decided here.", "paper")),
        ("words", (["Waiting period.", "Room rent limit.", "Co-payment."], "green")),
        ("manifesto", (["Health cover is not", "a premium comparison.", "It is a wording comparison."], "paper")),
        ("manifesto", (["Read what decides", "your claim.", "paisaclear.co.in"], "deep")),
    ]},
    {"key": "05", "file": "05-the-message.mp4", "scenes": [
        ("punch", ("Your account will be blocked in 24 hours.", "deep")),
        ("big", ("It is a scam.", "no bank turns off an account by SMS", "paper", None, "", "")),
        ("words", (["OTP request.", "Fake deadline.", "Lookalike link."], "green")),
        ("manifesto", (["Paste it.", "See the flags.", "Free. Nothing stored."], "paper")),
        ("manifesto", (["Check a message", "before you reply.", "paisaclear.co.in/check"], "deep")),
    ]},
    {"key": "06", "file": "06-bank-pays-3.mp4", "scenes": [
        ("big", ("3%", "what your savings account pays", "paper", 3, "", "%")),
        ("big", ("5%", "what prices do", "red", 5, "", "%")),
        ("punch", ("You are moving backwards.", "deep")),
        ("words", (["Real return", "is what matters."], "paper")),
        ("manifesto", (["Understand the product", "before the money goes in.", "paisaclear.co.in"], "green")),
    ]},
    {"key": "07", "file": "07-two-funds.mp4", "scenes": [
        ("words", (["Two funds.", "Same category.", "Different outcomes."], "deep")),
        ("bars", ("Three-year return", [("Fund A", 13.7, GREEN), ("Fund B", 3.6, RED)], "paper")),
        ("punch", ("The category name tells you nothing.", "deep")),
        ("manifesto", (["Look at the record,", "the cost and the risk.", "Not the label."], "paper")),
        ("manifesto", (["Compare before", "you commit.", "paisaclear.co.in"], "green")),
    ]},
    {"key": "08", "file": "08-300-products.mp4", "scenes": [
        ("big", ("300", "products, one place", "paper", 300, "", "")),
        ("words", (["Schemes.", "Deposits.", "Funds. Bonds. Insurance."], "green")),
        ("punch", ("Compare them side by side.", "deep")),
        ("manifesto", (["No advice.", "No sign up.", "No payments."], "paper")),
        ("manifesto", (["Every figure dated.", "Every figure sourced.", "paisaclear.co.in"], "deep")),
    ]},
    {"key": "09", "file": "09-the-date.mp4", "scenes": [
        ("punch", ("A rate without a date is a guess.", "paper")),
        ("words", (["Ten days old.", "Ten weeks old.", "Ten months old."], "deep")),
        ("big", ("Every figure", "carries the date it applied", "green", None, "", "")),
        ("manifesto", (["And the link", "to where it came from."], "paper")),
        ("manifesto", (["Dated. Sourced.", "paisaclear.co.in"], "deep")),
    ]},
    {"key": "10", "file": "10-before-you-invest.mp4", "scenes": [
        ("manifesto", (["Most people", "find out what a product is", "after they buy it."], "deep")),
        ("punch", ("Not you.", "paper")),
        ("words", (["Understand it.", "Compare it.", "Then decide."], "green")),
        ("manifesto", (["Free. No accounts.", "No products sold."], "paper")),
        ("manifesto", (["PaisaClear", "understand the product first"], "deep")),
    ]},
]


def draw_frame(ad, index, local, total_scenes, key):
    template, spec = ad["scenes"][index]
    frame = Image.new("RGB", (W, H), PAPER)
    draw, bg, ink, second = TEMPLATES[template](frame, spec, local)
    brand(draw, second, index + 1, total_scenes)
    progress(draw, (index + max(0.0, min(1.0, local / (SECONDS / total_scenes)))) / total_scenes, bg, second)
    return frame


def render(ad: dict, ffmpeg: str) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / ad["file"]
    scene_len = SECONDS / len(ad["scenes"])
    cmd = [ffmpeg, "-y", "-loglevel", "error",
           "-f", "rawvideo", "-vcodec", "rawvideo", "-s", f"{W}x{H}",
           "-pix_fmt", "rgb24", "-r", str(FPS), "-i", "-",
           "-an", "-vcodec", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    scenes = len(ad["scenes"])
    for n in range(TOTAL):
        t = n / FPS
        idx = min(scenes - 1, int(t // scene_len))
        local = t - idx * scene_len
        frame = draw_frame(ad, idx, local, scenes, ad["key"])
        if local < 0.32 and idx > 0:
            prev = draw_frame(ad, idx - 1, scene_len - 0.01, scenes, ad["key"])
            frame = Image.blend(prev, frame, ease(local / 0.32))
        proc.stdin.write(frame.tobytes())

    proc.stdin.close()
    proc.wait()
    return out


def find_ffmpeg():
    found = shutil.which("ffmpeg")
    if found:
        return found
    for base in (Path.home() / "AppData/Local/Microsoft/WinGet/Packages", Path("C:/ffmpeg")):
        if base.exists():
            for candidate in base.rglob("ffmpeg.exe"):
                return str(candidate)
    return None


def main() -> int:
    ffmpeg = find_ffmpeg()
    if not ffmpeg:
        print("ffmpeg not found. Install with: winget install --id Gyan.FFmpeg -e")
        return 1
    print("ffmpeg:", ffmpeg)
    wanted = sys.argv[1] if len(sys.argv) > 1 else None
    for ad in ADS:
        if wanted and not ad["key"].startswith(wanted):
            continue
        print(f"  {ad['file']} ...", flush=True)
        path = render(ad, ffmpeg)
        print(f"    {path.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
