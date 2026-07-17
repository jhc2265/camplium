import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "camp-lium-original.png"
OUT = ROOT / "assets" / "elements"
OUT.mkdir(parents=True, exist_ok=True)


def save_crop(img: Image.Image, name: str, box: tuple[int, int, int, int]) -> None:
    crop = img.crop(box)
    crop.save(OUT / name, "PNG")


def save_paper_texture() -> None:
    random.seed(17)
    w, h = 900, 900
    base = Image.new("RGB", (w, h), "#f3eedf")
    pix = base.load()
    for y in range(h):
      for x in range(w):
        n = random.randint(-7, 7)
        r, g, b = pix[x, y]
        pix[x, y] = (
            max(0, min(255, r + n)),
            max(0, min(255, g + n)),
            max(0, min(255, b + n)),
        )
    draw = ImageDraw.Draw(base, "RGBA")
    for _ in range(1300):
        x = random.randrange(w)
        y = random.randrange(h)
        draw.point((x, y), fill=(105, 92, 70, random.randrange(10, 22)))
    for _ in range(34):
        x = random.randrange(-140, w)
        y = random.randrange(-140, h)
        draw.arc((x, y, x + random.randrange(140, 320), y + random.randrange(120, 300)), 10, 330, fill=(120, 108, 80, 12), width=1)
    base.filter(ImageFilter.GaussianBlur(.15)).save(OUT / "paper-texture.png", "PNG")


def main() -> None:
    img = Image.open(SRC).convert("RGBA")
    save_paper_texture()

    crops = {
        "brand.png": (245, 118, 965, 320),
        "hero-placeholder.png": (2008, 450, 3905, 1925),
        "hero-camp-left.png": (0, 1665, 1900, 2235),
        "hero-camp-right.png": (2380, 1665, 4165, 2235),
        "torn-hero-about.png": (0, 2085, 4165, 2350),
        "about-placeholder-main.png": (2195, 2475, 3130, 3355),
        "about-placeholder-small-top.png": (3180, 2475, 3715, 2945),
        "about-placeholder-small-bottom.png": (3180, 3000, 3715, 3355),
        "about-tape.png": (2110, 2410, 2375, 2550),
        "about-plant.png": (3790, 3020, 4040, 3415),
        "style-thumb.png": (360, 3915, 1135, 4330),
        "style-car.png": (980, 4420, 1165, 4545),
        "style-tent.png": (1830, 4405, 2060, 4555),
        "style-bag.png": (2750, 4385, 2925, 4560),
        "style-tree.png": (3700, 4320, 3960, 4565),
        "activities-map.png": (1030, 4890, 4005, 6325),
        "torn-style-activities.png": (0, 4680, 4165, 4985),
        "guide-bus.png": (380, 6610, 610, 6835),
        "guide-clock.png": (1290, 6610, 1525, 6845),
        "guide-wallet.png": (2190, 6610, 2425, 6845),
        "guide-phone.png": (3080, 6610, 3320, 6845),
        "news-thumb.png": (350, 7300, 735, 7688),
        "news-side-art.png": (3300, 7080, 4165, 7855),
        "footer-bg-art.png": (0, 7720, 4165, 8522),
    }

    for name, box in crops.items():
        save_crop(img, name, box)


if __name__ == "__main__":
    main()
