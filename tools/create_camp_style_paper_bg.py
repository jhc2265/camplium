from __future__ import annotations

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "elements"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    random.seed(707)
    w, h = 2600, 760
    base = Image.new("RGB", (w, h), "#f2eedf")
    draw = ImageDraw.Draw(base, "RGBA")

    # Quiet paper surface only. No blobs, curves, strokes, or visible fibers.
    for _ in range(12000):
        x = random.randrange(w)
        y = random.randrange(h)
        color = random.choice([
            (128, 114, 86, 5),
            (255, 252, 238, 7),
            (188, 174, 132, 3),
        ])
        draw.point((x, y), fill=color)

    # Very faint top/bottom depth without visible blotches.
    edge = Image.new("L", (w, h), 0)
    ed = ImageDraw.Draw(edge)
    ed.rectangle((0, 0, w, 40), fill=10)
    ed.rectangle((0, h - 64, w, h), fill=8)
    edge = edge.filter(ImageFilter.GaussianBlur(42))
    shade = Image.new("RGBA", (w, h), (120, 105, 78, 0))
    shade.putalpha(edge)
    out = base.convert("RGBA")
    out.alpha_composite(shade)
    out.save(OUT / "camp-style-paper-bg.png", "PNG")


if __name__ == "__main__":
    main()
