#!/usr/bin/env python3
"""
make_icon.py — generates Flint.icns
Draws a stylized rainbow F on a dark background,
converts it to a proper macOS .icns file.
"""
from PIL import Image, ImageDraw
import subprocess, shutil, os

OUT_ICNS = os.path.join(os.path.dirname(__file__), "Flint.icns")

def make_base(size=1024):
    img = Image.new("RGBA", (size, size), (13, 17, 23, 255))
    draw = ImageDraw.Draw(img)

    s = size
    p = int(s * 0.12)       # padding
    bh = int(s * 0.13)      # bar height
    vw = int(s * 0.13)      # vertical bar width
    mw = int((s - 2*p) * 0.65)  # middle bar width

    rainbow = ["#ff4444", "#ff7700", "#ffcc00", "#44dd55", "#3399ff", "#bb44ff"]

    # rounded rectangle helper
    def rr(box, color, r=None):
        if r is None:
            r = bh // 4
        draw.rounded_rectangle(box, radius=r, fill=color)

    # ── vertical left bar (gradient by drawing horizontal slices) ──
    grad_colors = [
        (0xff, 0x44, 0x44),
        (0xff, 0x77, 0x00),
        (0xff, 0xcc, 0x00),
        (0x44, 0xdd, 0x55),
        (0x33, 0x99, 0xff),
        (0xbb, 0x44, 0xff),
    ]
    vert_h = s - 2 * p
    for row in range(vert_h):
        t = row / vert_h
        seg = t * (len(grad_colors) - 1)
        lo  = int(seg)
        hi  = min(lo + 1, len(grad_colors) - 1)
        frac = seg - lo
        c = tuple(int(grad_colors[lo][i] + (grad_colors[hi][i] - grad_colors[lo][i]) * frac)
                  for i in range(3))
        y = p + row
        draw.rectangle([p, y, p + vw, y], fill=c)

    # ── top horizontal bar ──
    rr([p, p, s - p, p + bh], rainbow[0])

    # ── middle horizontal bar ──
    mid_y = s // 2 - bh // 2
    rr([p, mid_y, p + mw, mid_y + bh], rainbow[2])

    # ── spark dots (top right corner) ──
    sparks = [
        (s - p - int(s*0.07),  p + int(s*0.04),  int(s*0.035)),
        (s - p - int(s*0.03),  p + int(s*0.10),  int(s*0.022)),
        (s - p - int(s*0.12),  p + int(s*0.07),  int(s*0.028)),
        (s - p - int(s*0.06),  p + int(s*0.18),  int(s*0.018)),
    ]
    sc = [rainbow[3], rainbow[4], rainbow[5], rainbow[1]]
    for (x, y, r), color in zip(sparks, sc):
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color)

    return img


def make_icns(out_path):
    iconset = out_path.replace(".icns", ".iconset")
    os.makedirs(iconset, exist_ok=True)

    sizes = [16, 32, 64, 128, 256, 512, 1024]
    base = make_base(1024)

    for sz in sizes:
        resized = base.resize((sz, sz), Image.LANCZOS)
        if sz <= 512:
            resized.save(f"{iconset}/icon_{sz}x{sz}.png")
        if sz >= 32:
            half = sz // 2
            resized.save(f"{iconset}/icon_{half}x{half}@2x.png")

    subprocess.run(["iconutil", "-c", "icns", iconset, "-o", out_path], check=True)
    shutil.rmtree(iconset)
    print(f"  ✓  Created {os.path.basename(out_path)}")


if __name__ == "__main__":
    make_icns(OUT_ICNS)
