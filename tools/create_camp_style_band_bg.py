from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "elements"
OUT.mkdir(parents=True, exist_ok=True)


def make_edge(width: int, base: int, amp: int, step: int, seed_shift: int = 0) -> list[tuple[int, int]]:
    points: list[tuple[int, int]] = []
    for x in range(-step, width + step * 2, step):
        y = int(
            base
            + math.sin((x + seed_shift) / 71) * amp
            + math.sin((x + seed_shift) / 31) * (amp * 0.45)
            + random.randint(-amp // 2, amp // 2)
        )
        points.append((x, y))
    return points


def main() -> None:
    random.seed(129)
    w, h = 2600, 780
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img, "RGBA")

    top = make_edge(w, 34, 12, 24, 0)
    bottom = make_edge(w, h - 34, 14, 24, 480)

    band_poly = top + list(reversed(bottom))
    d.polygon(band_poly, fill="#e2e4d5")

    # Soft watercolor wash, clipped visually by drawing translucent blobs inside the band.
    for _ in range(180):
        x = random.randint(-160, w)
        y = random.randint(45, h - 45)
        rx = random.randint(120, 520)
        ry = random.randint(45, 210)
        col = random.choice([
            (203, 209, 190, 24),
            (231, 228, 208, 30),
            (190, 201, 181, 20),
            (246, 242, 224, 22),
        ])
        d.ellipse((x - rx, y - ry, x + rx, y + ry), fill=col)

    # Paper grain and vertical watercolor fibers.
    for _ in range(4800):
        x = random.randrange(w)
        y = random.randrange(h)
        if 34 < y < h - 34:
            d.point((x, y), fill=(103, 100, 78, random.randrange(5, 18)))

    for _ in range(360):
        x = random.randrange(w)
        y1 = random.randrange(55, h - 150)
        length = random.randrange(80, 360)
        d.line((x, y1, x + random.randint(-10, 10), min(h - 55, y1 + length)), fill=(110, 112, 90, random.randrange(4, 11)), width=1)

    # Feathered torn edges.
    for x, y in top:
        d.ellipse((x - 22, y - 9, x + 22, y + 8), fill=(255, 255, 246, 32))
    for x, y in bottom:
        d.ellipse((x - 24, y - 8, x + 24, y + 10), fill=(255, 255, 246, 36))

    img = img.filter(ImageFilter.GaussianBlur(0.25))
    img.save(OUT / "camp-style-band-bg.png", "PNG")


if __name__ == "__main__":
    main()
