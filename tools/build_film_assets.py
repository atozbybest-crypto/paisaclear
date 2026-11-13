#!/usr/bin/env python3
"""Build the film's typographic assets at 1080x1920.

  1. Date supers      — transparent PNGs, overlay on your own paper footage
  2. Screen insert    — the rates page with a dated figure and a source link
  3. End card         — 4s MP4 plus a still PNG

    python tools/build_film_assets.py
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "ads" / "film-assets"
W, H = 1080, 1920
FPS = 30

PAPER = (247, 244, 236)
INK = (20, 35, 28)
GREEN = (15, 81, 50)
MUTED = (107, 116, 110)
AMBER = (214, 158, 46)
LINE = (216, 210, 196)

FB = "C:/Windows/Fonts/georgiab.ttf"
FR = "C:/Windows/Fonts/georgia.ttf"
FU = "C:/Windows/Fonts/segoeuib.ttf"
FUN = "C:/Windows/Fonts/segoeui.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def tracking(draw, x, y, text, fnt, fill, space=3):
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + space


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


# --------------------------------------------------------------- 1. date supers

DATES = [
    ("dates-as-on-01-04-2021.png", "01.04.2021"),
    ("dates-as-on-2022.png", "2022"),
    ("dates-as-on-2023.png", "2023"),
]


def build_date_super(path: Path, value: str):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    fnt = font(FU, 34)
    label = "AS PRINTED"
    # bottom-left, clear of a 9:16 safe area
    x, y = 88, H - 320
    draw.line([x, y - 26, x + 96, y - 26], fill=INK + (160,), width=3)
    tracking(draw, x, y, label, font(FU, 22), MUTED + (255,), space=4)
    size = 78 if len(value) > 4 else 96
    draw.text((x, y + 40), value, font=font(FB, size), fill=INK + (255,))
    img.save(path)
    return path


# --------------------------------------------------------------- 2. screen insert

def screen_frame(local: float) -> Image.Image:
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # browser chrome, so it reads as a screen not a poster
    draw.rectangle([0, 0, W, 150], fill=(236, 232, 221))
    for i, colour in enumerate([(226, 106, 94), (231, 187, 90), (140, 190, 130)]):
        draw.ellipse([40 + i * 44, 58, 66 + i * 44, 84], fill=colour)
    draw.rounded_rectangle([230, 46, W - 60, 100], radius=26, fill=(248, 246, 240), outline=LINE, width=2)
    draw.text((258, 60), "paisaclear.co.in/rates", font=font(FUN, 26), fill=MUTED)

    draw.text((88, 230), "PAISACLEAR", font=font(FU, 28), fill=MUTED)

    # the rate card
    top = 380
    draw.rounded_rectangle([72, top, W - 72, top + 520], radius=26, fill=(255, 255, 255), outline=LINE, width=2)
    draw.text((116, top + 46), "Sukanya Samriddhi Yojana", font=font(FB, 40), fill=INK)
    draw.text((116, top + 120), "8.20%", font=font(FB, 128), fill=GREEN)

    appear = ease(min(1.0, max(0.0, (local - 0.9) / 0.8)))
    if appear > 0:
        tint = tuple(int(PAPER[i] + (MUTED[i] - PAPER[i]) * appear) for i in range(3))
        line_y = top + 300
        draw.line([116, line_y - 18, W - 116, line_y - 18], fill=LINE, width=2)
        draw.text((116, line_y), "as of 1 October 2026", font=font(FR, 34), fill=tint)
        link = "Source: nsiindia.gov.in  \u2197"
        draw.text((116, line_y + 62), link, font=font(FUN, 30), fill=(15, 81, 50) if appear > 0.6 else tint)

    draw.text((116, top + 430), "Notified quarterly · dated on every page", font=font(FUN, 26), fill=MUTED)

    zoom = 1.0 + 0.04 * (local / 6.0)
    w2, h2 = int(W * zoom), int(H * zoom)
    return img.resize((w2, h2), Image.LANCZOS).crop(((w2 - W) // 2, (h2 - H) // 2, (w2 - W) // 2 + W, (h2 - H) // 2 + H))


# --------------------------------------------------------------- 3. end card

def endcard_frame(local: float, total: float = 4.0) -> Image.Image:
    img = Image.new("RGB", (W, H), GREEN)
    draw = ImageDraw.Draw(img)
    a = ease(min(1.0, local / 0.9))

    def tint(colour):
        return tuple(int(GREEN[i] + (colour[i] - GREEN[i]) * a) for i in range(3))

    brand = font(FB, 104)
    bw = draw.textlength("PaisaClear", font=brand)
    draw.text(((W - bw) / 2, 720), "PaisaClear", font=brand, fill=tint(PAPER))

    tag = font(FR, 38)
    for i, line in enumerate(["Understand the product", "before you put money in it."]):
        tw = draw.textlength(line, font=tag)
        draw.text(((W - tw) / 2, 880 + i * 52), line, font=tag, fill=tint((201, 216, 207)))

    url = font(FU, 46)
    uw = draw.textlength("paisaclear.co.in", font=url)
    draw.text(((W - uw) / 2, 1080), "paisaclear.co.in", font=url, fill=tint(PAPER))

    small = font(FUN, 26)
    sw = draw.textlength("Free · No sign-up · No advice", font=small)
    draw.text(((W - sw) / 2, 1170), "Free · No sign-up · No advice", font=small, fill=tint((160, 186, 168)))

    # hairline that draws itself
    line_w = int(((W - 400) / 2) * ease(min(1.0, local / 1.2)))
    if line_w > 0:
        draw.line([W / 2 - line_w, 1250, W / 2 + line_w, 1250], fill=tint((214, 158, 46)), width=3)
    return img


def find_ffmpeg():
    found = shutil.which("ffmpeg")
    if found:
        return found
    base = Path.home() / "AppData/Local/Microsoft/WinGet/Packages"
    if base.exists():
        for candidate in base.rglob("ffmpeg.exe"):
            return str(candidate)
    return None


def render_video(ffmpeg: str, out: Path, seconds: float, frame_fn):
    cmd = [ffmpeg, "-y", "-loglevel", "error",
           "-f", "rawvideo", "-vcodec", "rawvideo", "-s", f"{W}x{H}",
           "-pix_fmt", "rgb24", "-r", str(FPS), "-i", "-",
           "-an", "-vcodec", "libx264", "-preset", "medium", "-crf", "18",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    total = int(seconds * FPS)
    for n in range(total):
        proc.stdin.write(frame_fn(n / FPS).tobytes())
    proc.stdin.close()
    proc.wait()
    print(f"  {out.name:<28} {out.stat().st_size // 1024} KB")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    for name, value in DATES:
        build_date_super(OUT / name, value)
        print(f"  {name:<28} super")

    ffmpeg = find_ffmpeg()
    if not ffmpeg:
        print("ffmpeg missing — install with: winget install --id Gyan.FFmpeg -e")
        return 1

    render_video(ffmpeg, OUT / "insert-laptop-screen.mp4", 6.0, screen_frame)
    render_video(ffmpeg, OUT / "endcard.mp4", 4.0, endcard_frame)
    endcard_frame(3.0).save(OUT / "endcard-still.png")
    print(f"  {'endcard-still.png':<28} still")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
