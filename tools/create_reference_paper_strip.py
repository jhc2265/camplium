from __future__ import annotations

from pathlib import Path

import random
import math

from PIL import Image, ImageChops, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = Path(r"C:\Users\Administrator\Downloads\ChatGPT Image 2026년 7월 6일 오후 03_45_04.png")
OUT = ROOT / "assets" / "elements"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    random.seed(706)
    src = Image.open(REFERENCE).convert("RGBA")
    target_w, target_h = 2600, 260
    strip = src.resize((target_w, target_h), Image.Resampling.LANCZOS)
    rgb = strip.convert("RGB")

    white_bg = Image.new("RGB", strip.size, (255, 255, 255))
    diff = ImageChops.difference(rgb, white_bg).convert("L")

    alpha = Image.new("L", (target_w, target_h), 0)
    alpha_px = alpha.load()
    diff_px = diff.load()
    for x in range(target_w):
        ys = [y for y in range(target_h) if diff_px[x, y] > 24]
        if not ys:
            continue
        ref_bottom = max(ys)
        wave = (
            math.sin((x - 120) / 128) * 22
            + math.sin((x + 340) / 55) * 9
            + math.sin((x - 760) / 300) * 28
        )
        art_dips = (
            44 * math.exp(-((x - 460) / 190) ** 2)
            - 20 * math.exp(-((x - 700) / 80) ** 2)
            + 30 * math.exp(-((x - 1180) / 260) ** 2)
            + 42 * math.exp(-((x - 1770) / 150) ** 2)
            + 34 * math.exp(-((x - 2190) / 190) ** 2)
        )
        ref_texture = (ref_bottom - 238) * 0.35
        bottom = int(198 + wave + art_dips + ref_texture + random.randint(-2, 2))
        bottom = max(170, min(target_h - 4, bottom))
        for y in range(0, bottom + 1):
            alpha_px[x, y] = 255
    alpha = alpha.filter(ImageFilter.GaussianBlur(1.15))

    base = Image.new("RGB", (target_w, target_h), "#f3eedf")
    draw = ImageDraw.Draw(base, "RGBA")

    # Only tiny paper speckles and broad soft wash. No curves, no fiber lines.
    for _ in range(6500):
        x = random.randrange(target_w)
        y = random.randrange(target_h)
        shade = random.choice([(116, 105, 78, 9), (255, 252, 238, 10), (132, 123, 96, 5)])
        draw.point((x, y), fill=shade)

    for _ in range(28):
        x = random.randint(-300, target_w)
        y = random.randint(24, target_h - 24)
        rx = random.randint(240, 720)
        ry = random.randint(18, 58)
        col = random.choice([(235, 229, 207, 18), (255, 252, 238, 18), (222, 218, 198, 12)])
        draw.ellipse((x - rx, y - ry, x + rx, y + ry), fill=col)

    edge_shadow = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    edge_draw = ImageDraw.Draw(edge_shadow, "RGBA")
    for x in range(0, target_w, 4):
        ys = [y for y in range(target_h) if alpha_px[x, y] > 128]
        if not ys:
            continue
        bottom = max(ys)
        edge_draw.line((x, bottom - 1, x + 3, bottom - 1), fill=(104, 94, 72, 16), width=1)
    edge_shadow = edge_shadow.filter(ImageFilter.GaussianBlur(0.7))

    out = base.convert("RGBA")
    out.alpha_composite(edge_shadow)
    out.putalpha(alpha)
    out.save(OUT / "hero-paper-transition.png", "PNG")

    preview = Image.new("RGBA", (target_w, 360), "#dfe8d8")
    preview.paste(Image.new("RGBA", (target_w, 220), "#f3eedf"), (0, 0))
    preview.alpha_composite(out, (0, 78))
    preview.convert("RGB").save(ROOT / "hero-paper-transition-preview.png", "PNG")


if __name__ == "__main__":
    main()
