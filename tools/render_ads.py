#!/usr/bin/env python3
"""Render the five PaisaClear ads as MP4 motion graphics.

Every frame is drawn here — no footage, no stock images, no people. Numbers
count up, text eases in, the progress bar tracks the spot. Frames are piped
straight into ffmpeg.

    python tools/render_ads.py              # all five
    python tools/render_ads.py 02           # just the SSY ad

Needs ffmpeg on PATH, or at %LOCALAPPDATA%\\Microsoft\\WinGet\\Packages\\...
"""

from __future__ import annotations

import math
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ADS_DIR = ROOT / "ads"
W, H = 1080, 1920
FPS = 30
SECONDS = 20.0
TOTAL = int(FPS * SECONDS)

PAPER = (247, 244, 236)
INK = (20, 35, 28)
GREEN = (15, 81, 50)
MUTED = (107, 116, 110)
SOFT = (201, 216, 207)
AMBER = (183, 121, 31)

FONT_BOLD = "C:/Windows/Fonts/georgiab.ttf"
FONT_REG = "C:/Windows/Fonts/georgia.ttf"
FONT_UI = "C:/Windows/Fonts/segoeuib.ttf"


def font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


# scene: (headline, sub, tone, count_to_or_None, prefix, suffix)
ADS = [
    {
        "key": "01",
        "file": "01-rate-without-a-date.mp4",
        "scenes": [
            ("8.20%", "Sukanya Samriddhi", "paper", 8.20, "", "%"),
            ("But since when?", "a rate means nothing without a date", "green", None, "", ""),
            ("Most sites never say.", "they quote the number, not the date", "paper", None, "", ""),
            ("PaisaClear dates every rate.", "and links the source", "green", None, "", ""),
            ("Dated. Sourced.", "paisaclear.co.in", "paper", None, "", ""),
        ],
    },
    {
        "key": "02",
        "file": "02-ssy-calculator.mp4",
        "scenes": [
            ("₹1,50,000", "a year, for 15 years", "paper", 150000, "₹", ""),
            ("15 years", "then it keeps growing", "green", 15, "", ""),
            ("₹71,82,119", "at maturity, year 21", "paper", 7182119, "₹", ""),
            ("Every rupee accounted for.", "year by year, not a headline", "green", None, "", ""),
            ("Change the rate.", "see what a revision costs", "paper", None, "", ""),
        ],
    },
    {
        "key": "03",
        "file": "03-fd-vs-ppf-tax.mp4",
        "scenes": [
            ("7.10%", "the rate you see", "paper", 7.10, "", "%"),
            ("5.04%", "what a fixed deposit leaves you", "red", 5.04, "", "%"),
            ("7.10%", "what PPF leaves you", "green", 7.10, "", "%"),
            ("Same number.", "different money", "paper", None, "", ""),
            ("The gap, every year.", "paisaclear.co.in", "green", None, "", ""),
        ],
    },
    {
        "key": "04",
        "file": "04-scam-checker.mp4",
        "scenes": [
            ("Your account will be blocked in 24 hours.", "you have seen this message", "green", None, "", ""),
            ("It is a scam.", "no bank switches off an account by SMS", "paper", None, "", ""),
            ("OTP request.", "flag one", "green", 1, "", ""),
            ("Fake deadline.", "flag two", "green", 2, "", ""),
            ("Lookalike link.", "flag three — paisaclear.co.in/check", "paper", 3, "", ""),
        ],
    },
    {
        "key": "05",
        "file": "05-compare.mp4",
        "scenes": [
            ("300 products.", "one place", "paper", 300, "", ""),
            ("Schemes. Deposits. Funds. Bonds.", "insurance too", "green", None, "", ""),
            ("Side by side.", "rates, lock-ins, tax, risk", "paper", None, "", ""),
            ("No advice. No sign up.", "no payments", "green", None, "", ""),
            ("Every figure dated.", "paisaclear.co.in", "paper", None, "", ""),
        ],
    },
]


def indian(n: int) -> str:
    """Group digits the Indian way: 71,82,119 not 7,182,119."""
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
    """Cubic ease-out on a 0..1 progress value."""
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def wrap(draw, text, fnt, max_width):
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


def palette(tone: str):
    if tone == "green":
        return GREEN, PAPER, SOFT
    if tone == "red":
        return (122, 35, 24), PAPER, (240, 200, 194)
    return PAPER, INK, MUTED


def draw_scene(frame: Image.Image, scene, local: float, index: int, total: int, ad_key: str):
    headline, sub, tone, count_to, prefix, suffix = scene
    bg, ink, second = palette(tone)
    draw = ImageDraw.Draw(frame)
    draw.rectangle([0, 0, W, H], fill=bg)

    # brand line
    draw.text((72, 92), "PAISACLEAR", font=font(FONT_UI, 30), fill=second)

    # scene counter, top right
    draw.text((W - 132, 92), f"{index + 1}/{total}", font=font(FONT_UI, 26), fill=second)

    # counting number
    text = headline
    if count_to is not None:
        progress = ease(min(1.0, local / 1.6))
        value = count_to * progress
        if count_to >= 1000:
            text = f"{prefix}{indian(int(round(value)))}{suffix}"
        elif count_to < 20 and ("." in f"{count_to}" or suffix == "%"):
            text = f"{prefix}{value:.2f}{suffix}"
        else:
            text = f"{prefix}{int(round(value))}{suffix}"

    size = 108
    fnt = font(FONT_BOLD, size)
    lines = wrap(draw, text, fnt, W - 160)
    while len(lines) > 3 and size > 54:
        size -= 8
        fnt = font(FONT_BOLD, size)
        lines = wrap(draw, text, fnt, W - 160)

    slide = int((1 - ease(min(1.0, local / 0.7))) * 46)
    y = 640 + slide
    for line in lines:
        width = draw.textlength(line, font=fnt)
        draw.text(((W - width) / 2, y), line, font=fnt, fill=ink)
        y += size * 1.14

    # sub line
    if sub:
        alpha = ease(min(1.0, max(0.0, (local - 0.45) / 0.8)))
        if alpha > 0:
            sub_fnt = font(FONT_REG, 40)
            sub_lines = wrap(draw, sub, sub_fnt, W - 220)
            sy = y + 40 + int((1 - alpha) * 26)
            tint = tuple(int(bg[i] + (second[i] - bg[i]) * alpha) for i in range(3))
            for line in sub_lines:
                width = draw.textlength(line, font=sub_fnt)
                draw.text(((W - width) / 2, sy), line, font=sub_fnt, fill=tint)
                sy += 56

    # footer
    draw.text((72, H - 132), "paisaclear.co.in", font=font(FONT_UI, 30), fill=second)

    # progress bar
    bar_y = H - 72
    draw.rectangle([72, bar_y, W - 72, bar_y + 6], fill=tuple(int((bg[i] + second[i]) / 2) for i in range(3)))
    overall = (index + max(0.0, min(1.0, local / 4.0))) / total
    draw.rectangle([72, bar_y, 72 + (W - 144) * overall, bar_y + 6], fill=AMBER)


def render(ad: dict, ffmpeg: str) -> Path:
    out = ADS_DIR / ad["file"]
    scene_len = SECONDS / len(ad["scenes"])
    cmd = [
        ffmpeg, "-y", "-loglevel", "error",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{W}x{H}", "-pix_fmt", "rgb24", "-r", str(FPS), "-i", "-",
        "-an", "-vcodec", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    for n in range(TOTAL):
        t = n / FPS
        index = min(len(ad["scenes"]) - 1, int(t // scene_len))
        local = t - index * scene_len
        frame = Image.new("RGB", (W, H), PAPER)
        draw_scene(frame, ad["scenes"][index], local, index, len(ad["scenes"]), ad["key"])

        # crossfade between scenes
        if local < 0.35 and index > 0:
            prev = Image.new("RGB", (W, H), PAPER)
            draw_scene(prev, ad["scenes"][index - 1], scene_len - 0.01, index - 1, len(ad["scenes"]), ad["key"])
            frame = Image.blend(prev, frame, ease(local / 0.35))

        proc.stdin.write(frame.tobytes())

    proc.stdin.close()
    proc.wait()
    return out


def find_ffmpeg() -> str | None:
    found = shutil.which("ffmpeg")
    if found:
        return found
    local = Path.home() / "AppData/Local/Microsoft/WinGet/Packages"
    if local.exists():
        for candidate in local.rglob("ffmpeg.exe"):
            return str(candidate)
    return None


def main() -> int:
    ffmpeg = find_ffmpeg()
    if not ffmpeg:
        print("ffmpeg not found.\nInstall it with:  winget install --id Gyan.FFmpeg -e")
        return 1
    print("ffmpeg:", ffmpeg)

    wanted = sys.argv[1] if len(sys.argv) > 1 else None
    ADS_DIR.mkdir(exist_ok=True)
    for ad in ADS:
        if wanted and not ad["key"].startswith(wanted):
            continue
        print(f"  rendering {ad['file']} ...", flush=True)
        path = render(ad, ffmpeg)
        print(f"  done  {path.name}  {path.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
