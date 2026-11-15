#!/usr/bin/env python3
"""Animate stills into a vertical film — no paid AI video.

Each shot gets a slow push or drift, film grain, a vignette and a light flicker,
then crossfades between shots. For a film built on paper and one quiet face,
this is indistinguishable from "AI video" and cannot morph anyone's face.

    python tools/film_from_stills.py
"""

from __future__ import annotations

import math
import random
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "ads" / "film-tests"
W, H = 1080, 1920
FPS = 24
FADE = 0.55

# (path, seconds, motion)  motion: in | out | left | right
SHOTS = [
    ("C:/Users/Gowtham_Sravya/.dsh/attachments/v1/objects/76/76b70970affa7b370293c0db0c902b1ba9410c93a51d5bacb7bd175939c8bfc6", 5.0, "in"),
    ("C:/Users/Gowtham_Sravya/.dsh/attachments/v1/objects/3b/3b8068e79aa1adadf2abd181f95cf79d46f1bf2d11a485ffbada09078a4ca1e2", 5.0, "out"),
]


def prepare(path: str) -> Image.Image:
    img = Image.open(path).convert("RGB")
    w, h = img.size
    target_w = int(h * 9 / 16)
    left = max(0, (w - target_w) // 2)
    img = img.crop((left, 0, left + target_w, h))
    return img.resize((W * 2, H * 2), Image.LANCZOS)  # headroom for the zoom


def ken_burns(base: Image.Image, progress: float, motion: str) -> Image.Image:
    """Zoom 1.00 -> 1.08 (or reverse), crop to frame."""
    span = 0.08
    if motion == "in":
        zoom = 1.0 + span * progress
    elif motion == "out":
        zoom = 1.0 + span * (1 - progress)
    else:
        zoom = 1.0 + span * 0.5

    bw, bh = base.size
    cw, ch = int(bw / zoom), int(bh / zoom)

    cx = bw / 2
    if motion == "left":
        cx = bw * (0.5 - 0.03 * (1 - progress))
    elif motion == "right":
        cx = bw * (0.5 + 0.03 * (1 - progress))

    left = int(max(0, min(bw - cw, cx - cw / 2)))
    top = int(max(0, min(bh - ch, (bh - ch) / 2)))
    return base.crop((left, top, left + cw, top + ch)).resize((W, H), Image.LANCZOS)


def grain_and_vignette(frame: Image.Image, seed: float) -> Image.Image:
    random.seed(int(seed * 1000) % 100000)
    noise = Image.effect_noise((W, H), 9).convert("L")
    grain = Image.merge("RGB", (noise, noise, noise))
    frame = Image.blend(frame, Image.blend(frame, grain, 0.06), 0.55)

    vignette = Image.new("L", (W, H), 0)
    draw = ImageDraw.Draw(vignette)
    draw.ellipse([-W * 0.35, -H * 0.25, W * 1.35, H * 1.25], fill=255)
    vignette = vignette.filter(ImageFilter.GaussianBlur(220))
    dark = ImageEnhance.Brightness(frame).enhance(0.55)
    return Image.composite(frame, dark, vignette)


def find_ffmpeg():
    found = shutil.which("ffmpeg")
    if found:
        return found
    base = Path.home() / "AppData/Local/Microsoft/WinGet/Packages"
    for candidate in base.rglob("ffmpeg.exe"):
        return str(candidate)
    return None


def render(out_path: Path, ffmpeg: str) -> None:
    prepared = [(prepare(p), secs, motion) for p, secs, motion in SHOTS]
    total = sum(secs for _, secs, _ in prepared) - FADE * (len(prepared) - 1)
    frames = int(total * FPS)

    cmd = [ffmpeg, "-y", "-loglevel", "error", "-f", "rawvideo", "-vcodec", "rawvideo",
           "-s", f"{W}x{H}", "-pix_fmt", "rgb24", "-r", str(FPS), "-i", "-",
           "-an", "-vcodec", "libx264", "-preset", "slow", "-crf", "19",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out_path)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    for n in range(frames):
        t = n / FPS
        # find which shot we are in, honouring overlaps
        elapsed, idx, local = 0.0, 0, 0.0
        for i, (_, secs, _) in enumerate(prepared):
            end = elapsed + secs
            if t < end or i == len(prepared) - 1:
                idx, local = i, t - elapsed
                break
            elapsed = end - FADE

        base, secs, motion = prepared[idx]
        frame = ken_burns(base, min(1.0, local / secs), motion)

        # crossfade into the next shot
        if idx + 1 < len(prepared):
            start_fade = secs - FADE
            if local >= start_fade:
                nxt, nsecs, nmotion = prepared[idx + 1]
                k = (local - start_fade) / FADE
                other = ken_burns(nxt, 0.0, nmotion)
                frame = Image.blend(frame, other, k)

        frame = grain_and_vignette(frame, t)
        frame = ImageEnhance.Brightness(frame).enhance(1.0 + 0.012 * math.sin(t * 3.1))
        proc.stdin.write(frame.tobytes())

    proc.stdin.close()
    proc.wait()


def main() -> int:
    ffmpeg = find_ffmpeg()
    if not ffmpeg:
        print("ffmpeg missing")
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "demo-stills-motion.mp4"
    render(target, ffmpeg)
    print(f"  {target.name}  {target.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
