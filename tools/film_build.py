#!/usr/bin/env python3
"""Assemble the PaisaClear film from stills, the screen insert, the end card
and the ElevenLabs voiceover.

Outputs two files: English and Hindi.

    python tools/film_build.py
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "ads" / "raw"
ASSETS = ROOT / "ads" / "film-assets"
OUT = ROOT / "ads" / "final"
TMP = ROOT / "ads" / ".build"

W, H = 1080, 1920
FPS = 24

FB = "C:/Windows/Fonts/georgiab.ttf"
FU = "C:/Windows/Fonts/segoeuib.ttf"

INK = (20, 35, 28)
MUTED = (150, 143, 128)

# --- chosen stills -----------------------------------------------------------------
PAMPHLET = RAW / "Overhead_close-up_of_a_crumpled_cream-coloured_paper_pamphle (8).jpg"
FLIP = RAW / "Close-up_of_a_single_sheet_of_paper_lying_face_down_on_a_woo (3).jpg"
HER = RAW / "an_Indian_woman_in_her_mid-thirties_medium-brown_skin_dark_h (3).jpg"
LAPTOP = RAW / "Over-shoulder_view_of_a_dark_laptop_on_a_wooden_table_lid_ha (2).jpg"

# --- timing (seconds) --------------------------------------------------------------
P1, P2, P3, P4 = 5.5, 3.5, 3.5, 2.5    # pamphlet, her, flip, laptop
XFADE = 0.6

DATES = [("01.04.2021", 0.0), ("2022", 1.5), ("2023", 3.0)]


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def crop916(path: Path, focus: float = 0.5) -> Image.Image:
    img = Image.open(path).convert("RGB")
    w, h = img.size
    target = int(h * 9 / 16)
    left = int(max(0, min(w - target, w * focus - target / 2)))
    img = img.crop((left, 0, left + target, h))
    return img.resize((W * 2, H * 2), Image.LANCZOS)


def burns(base: Image.Image, progress: float, zoom_in: bool = True) -> Image.Image:
    span = 0.07
    zoom = 1.0 + span * (progress if zoom_in else 1 - progress)
    bw, bh = base.size
    cw, ch = int(bw / zoom), int(bh / zoom)
    left = (bw - cw) // 2
    top = (bh - ch) // 2
    return base.crop((left, top, left + cw, top + ch)).resize((W, H), Image.LANCZOS)


def grade(frame: Image.Image, t: float) -> Image.Image:
    noise = Image.effect_noise((W, H), 8).convert("L")
    grain = Image.merge("RGB", (noise, noise, noise))
    frame = Image.blend(frame, grain, 0.035)

    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse([-W * 0.35, -H * 0.25, W * 1.35, H * 1.25], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(200))
    dark = ImageEnhance.Brightness(frame).enhance(0.62)
    frame = Image.composite(frame, dark, mask)
    return ImageEnhance.Brightness(frame).enhance(1.0 + 0.01 * (t % 2))


def date_super(frame: Image.Image, text: str, alpha: float) -> Image.Image:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = 96, H - 430
    d.line([x, y - 30, x + 110, y - 30], fill=MUTED + (int(180 * alpha),), width=3)
    d.text((x, y), "AS PRINTED", font=font(FU, 24), fill=MUTED + (int(230 * alpha),))
    d.text((x, y + 46), text, font=font(FB, 108), fill=INK + (int(255 * alpha),))
    return Image.alpha_composite(frame.convert("RGBA"), layer).convert("RGB")


def render_part1(ffmpeg: str) -> Path:
    """Pamphlet -> her -> flip (with dates) -> laptop, plus crossfades."""
    out = TMP / "part1.mp4"
    stills = [
        (crop916(PAMPHLET), P1, True),
        (crop916(HER, focus=0.45), P2, True),
        (crop916(FLIP, focus=0.64), P3, False),
        (crop916(LAPTOP, focus=0.5), P4, True),
    ]
    bounds, acc = [], 0.0
    for _, secs, _ in stills:
        acc += secs
        bounds.append(acc)

    total = int(sum(s for _, s, _ in stills) * FPS)
    cmd = [ffmpeg, "-y", "-loglevel", "error", "-f", "rawvideo", "-vcodec", "rawvideo",
           "-s", f"{W}x{H}", "-pix_fmt", "rgb24", "-r", str(FPS), "-i", "-",
           "-an", "-vcodec", "libx264", "-preset", "medium", "-crf", "18",
           "-pix_fmt", "yuv420p", str(out)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    for n in range(total):
        t = n / FPS
        idx = next((i for i, b in enumerate(bounds) if t < b), len(stills) - 1)
        base, secs, zoom_in = stills[idx]
        local = t - (bounds[idx - 1] if idx else 0.0)
        frame = burns(base, min(1.0, local / secs), zoom_in)

        if idx == 2:  # the flip carries the dates
            for value, start_s in DATES:
                span = 1.4
                if start_s <= local < start_s + span:
                    fade = min(1.0, (local - start_s) / 0.3, (start_s + span - local) / 0.3)
                    frame = date_super(frame, value, max(0.0, fade))

        # crossfade into each new still
        if idx > 0 and local < XFADE:
            prev, psecs, pzoom = stills[idx - 1]
            frame = Image.blend(burns(prev, 1.0, pzoom), frame, local / XFADE)

        proc.stdin.write(grade(frame, t).tobytes())

    proc.stdin.close()
    proc.wait()
    return out


def assemble(ffmpeg: str, part1: Path, audio: Path, out: Path) -> None:
    insert = ASSETS / "insert-laptop-screen.mp4"
    endcard = ASSETS / "endcard.mp4"
    stills_len = P1 + P2 + P3 + P4
    insert_len = 3.5
    off1 = stills_len - XFADE
    off2 = stills_len + insert_len - 2 * XFADE
    total = stills_len + insert_len + 4.0 - 2 * XFADE

    graph = (
        f"[0:v]fps={FPS},settb=AVTB,format=yuv420p[p1];"
        f"[1:v]trim=duration={insert_len},setpts=PTS-STARTPTS,fps={FPS},settb=AVTB,format=yuv420p[ins];"
        f"[2:v]fps={FPS},settb=AVTB,format=yuv420p[end];"
        f"[p1][ins]xfade=transition=fade:duration={XFADE}:offset={off1:.2f}[a];"
        f"[a][end]xfade=transition=fade:duration={XFADE}:offset={off2:.2f}[v];"
        f"[3:a]adelay=400|400,apad[aud]"
    )
    cmd = [ffmpeg, "-y", "-loglevel", "error",
           "-i", str(part1), "-i", str(insert), "-i", str(endcard), "-i", str(audio),
           "-filter_complex", graph,
           "-map", "[v]", "-map", "[aud]", "-t", f"{total:.2f}",
           "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=False)


def find_ffmpeg():
    found = shutil.which("ffmpeg")
    if found:
        return found
    for c in (Path.home() / "AppData/Local/Microsoft/WinGet/Packages").rglob("ffmpeg.exe"):
        return str(c)
    return None


def main() -> int:
    ffmpeg = find_ffmpeg()
    if not ffmpeg:
        print("ffmpeg missing")
        return 1
    OUT.mkdir(exist_ok=True)
    TMP.mkdir(exist_ok=True)

    print("  rendering stills ...", flush=True)
    part1 = render_part1(ffmpeg)
    print("  part1 done")

    en = next(RAW.glob("*Vanishree*.mp3"))
    hi = next(RAW.glob("*Jia*.mp3"))
    assemble(ffmpeg, part1, en, OUT / "paisaclear-film-english.mp4")
    print("  english assembled")
    assemble(ffmpeg, part1, hi, OUT / "paisaclear-film-hindi.mp4")
    print("  hindi assembled")

    for f in sorted(OUT.glob("*.mp4")):
        print(f"  {f.name}  {f.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
