from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "elements"
OUT.mkdir(parents=True, exist_ok=True)
random.seed(31)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    names = [
        r"C:\Windows\Fonts\malgunbd.ttf" if bold else r"C:\Windows\Fonts\malgun.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for name in names:
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default()


def textured(size: tuple[int, int], color: str, alpha: int = 255) -> Image.Image:
    img = Image.new("RGBA", size, color)
    if alpha < 255:
        img.putalpha(alpha)
    px = img.load()
    for y in range(size[1]):
        for x in range(size[0]):
            r, g, b, a = px[x, y]
            n = random.randint(-8, 8)
            px[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n)), max(0, min(255, b + n)), a)
    return img.filter(ImageFilter.GaussianBlur(.12))


def save(img: Image.Image, name: str) -> None:
    img.save(OUT / name, "PNG")


def draw_tree(d: ImageDraw.ImageDraw, x: int, y: int, s: float, dark: str = "#35563d") -> None:
    d.rectangle((x - 5*s, y - 60*s, x + 5*s, y + 8*s), fill="#76623e")
    for i, (w, h, c) in enumerate([(58, 78, dark), (48, 62, "#496b4b"), (37, 49, "#62794f")]):
        yy = y - i * 34 * s
        d.polygon([(x, yy - h*s), (x - w*s, yy), (x + w*s, yy)], fill=c)
        d.line((x - w*.72*s, yy - 6*s, x + w*.65*s, yy - 5*s), fill=(255, 255, 230, 28), width=max(1, int(2*s)))


def draw_tent(d: ImageDraw.ImageDraw, x: int, y: int, s: float) -> None:
    d.polygon([(x, y - 150*s), (x - 150*s, y), (x + 170*s, y)], fill="#d8ad5b")
    d.polygon([(x - 5*s, y - 145*s), (x - 58*s, y), (x + 48*s, y)], fill="#76593a")
    d.polygon([(x + 45*s, y - 132*s), (x + 78*s, y), (x + 145*s, y)], fill="#efd68e")
    d.line((x, y - 150*s, x + 170*s, y), fill="#7c663b", width=max(2, int(5*s)))
    d.line((x - 150*s, y, x + 170*s, y), fill="#907246", width=max(2, int(3*s)))


def draw_fire(d: ImageDraw.ImageDraw, x: int, y: int, s: float) -> None:
    d.line((x - 70*s, y, x + 72*s, y - 28*s), fill="#765436", width=max(3, int(8*s)))
    d.line((x - 58*s, y - 28*s, x + 62*s, y + 2*s), fill="#6f4e32", width=max(3, int(8*s)))
    d.polygon([(x, y - 110*s), (x - 45*s, y - 12*s), (x + 44*s, y - 14*s)], fill="#cf6a39")
    d.polygon([(x + 10*s, y - 84*s), (x - 14*s, y - 12*s), (x + 25*s, y - 18*s)], fill="#f5bd5d")


def draw_car(d: ImageDraw.ImageDraw, x: int, y: int, s: float) -> None:
    d.rounded_rectangle((x - 130*s, y - 68*s, x + 135*s, y + 35*s), radius=int(22*s), fill="#6d918d", outline="#3e5852", width=max(2, int(4*s)))
    d.polygon([(x - 70*s, y - 68*s), (x - 32*s, y - 132*s), (x + 65*s, y - 132*s), (x + 110*s, y - 68*s)], fill="#e9ece2", outline="#53675d")
    d.rectangle((x - 18*s, y - 120*s, x + 33*s, y - 76*s), fill="#f7f5e8")
    d.rectangle((x + 44*s, y - 120*s, x + 88*s, y - 76*s), fill="#f7f5e8")
    d.rectangle((x - 50*s, y - 158*s, x + 80*s, y - 136*s), fill="#7a5737")
    for dx in (-76, 76):
        d.ellipse((x + dx*s - 26*s, y + 8*s, x + dx*s + 26*s, y + 60*s), fill="#28302e")
        d.ellipse((x + dx*s - 11*s, y + 23*s, x + dx*s + 11*s, y + 45*s), fill="#cbd0c8")


def paper_texture() -> None:
    img = textured((900, 900), "#f4efdf")
    d = ImageDraw.Draw(img, "RGBA")
    for _ in range(1200):
        x, y = random.randrange(900), random.randrange(900)
        d.point((x, y), fill=(112, 98, 72, random.randrange(8, 24)))
    for _ in range(34):
        x, y = random.randrange(-120, 900), random.randrange(-120, 900)
        d.arc((x, y, x + random.randrange(140, 360), y + random.randrange(120, 320)), 0, 310, fill=(120, 105, 77, 13), width=1)
    save(img, "paper-texture.png")


def placeholder(name: str, size: tuple[int, int], text: str = "이미지", radius: int = 40) -> None:
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle((0, 0, size[0]-1, size[1]-1), radius=radius, fill="#d9dad9", outline=(255, 255, 255, 150), width=4)
    cx, cy = size[0] // 2, int(size[1] * .45)
    d.polygon([(cx-55, cy+25), (cx-15, cy-38), (cx+25, cy+25)], fill="#bfc1bf")
    d.polygon([(cx+8, cy+25), (cx+42, cy-20), (cx+92, cy+25)], fill="#c7c9c7")
    f = font(max(22, min(size)//12), True)
    box = d.textbbox((0, 0), text, font=f)
    d.text((cx - (box[2]-box[0])/2, cy + 58), text, fill="#a6a7a6", font=f)
    save(img, name)


def brand() -> None:
    img = Image.new("RGBA", (720, 210), (0, 0, 0, 0))
    d = ImageDraw.Draw(img, "RGBA")
    draw_tent(d, 95, 135, .45)
    draw_tree(d, 170, 145, .42)
    draw_tree(d, 42, 152, .32)
    d.text((220, 35), "Camp Lium", font=font(52, True), fill="#314634")
    d.text((224, 103), "자연 속, 우리만의 시간", font=font(22), fill="#69735e")
    save(img, "brand.png")


def torn(name: str, color: str) -> None:
    w, h = 1800, 150
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img, "RGBA")
    pts = []
    for x in range(0, w + 35, 35):
        y = int(72 + math.sin(x / 53) * 15 + math.sin(x / 29) * 9 + random.randint(-8, 8))
        pts.append((x, y))
    d.polygon([(0, h), (0, pts[0][1]), *pts, (w, h)], fill=color)
    for x, y in pts:
        d.ellipse((x-18, y-7, x+20, y+8), fill=(255,255,255,38))
    save(img, name)


def band_texture(name: str, color: str, size: tuple[int, int] = (900, 900)) -> None:
    img = textured(size, color)
    d = ImageDraw.Draw(img, "RGBA")
    for _ in range(850):
        x, y = random.randrange(size[0]), random.randrange(size[1])
        d.point((x, y), fill=(48, 72, 76, random.randrange(8, 20)))
    save(img, name)


def torn_top(name: str, top_color: str, bottom_color: str) -> None:
    w, h = 2200, 180
    img = textured((w, h), bottom_color)
    d = ImageDraw.Draw(img, "RGBA")
    pts = []
    for x in range(0, w + 28, 28):
        y = int(78 + math.sin(x / 67) * 13 + math.sin(x / 31) * 8 + random.randint(-7, 7))
        pts.append((x, y))
    d.polygon([(0, 0), *pts, (w, 0)], fill=top_color)
    for x, y in pts:
        d.ellipse((x - 18, y - 8, x + 18, y + 8), fill=(255, 255, 255, 34))
    save(img, name)


def hero_left() -> None:
    img = Image.new("RGBA", (1900, 570), (0, 0, 0, 0))
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse((150, 315, 1230, 545), fill="#d5ceb5")
    for x, s in [(80, .9), (145, .7), (250, .55), (760, .42), (1120, .65), (1185, .5)]:
        draw_tree(d, x, 390, s)
    draw_tent(d, 530, 455, .78)
    d.line((1030, 430, 1070, 350, 1110, 430), fill="#536357", width=9)
    d.line((1040, 430, 1125, 430), fill="#536357", width=7)
    d.rectangle((1110, 368, 1188, 378), fill="#536357")
    draw_fire(d, 880, 470, .55)
    save(img, "hero-camp-left.png")


def hero_right() -> None:
    img = Image.new("RGBA", (1785, 570), (0, 0, 0, 0))
    d = ImageDraw.Draw(img, "RGBA")
    d.polygon([(0, 420), (340, 250), (680, 315), (985, 205), (1380, 320), (1785, 278), (1785, 570), (0, 570)], fill="#9bad74")
    d.polygon([(0, 465), (420, 310), (860, 335), (1240, 285), (1785, 355), (1785, 570), (0, 570)], fill="#c9c09b")
    for x, s in [(1180, .75), (1260, 1), (1370, .82), (1490, 1.06), (1600, .8), (1700, .65)]:
        draw_tree(d, x, 410, s)
    draw_car(d, 1080, 430, .78)
    save(img, "hero-camp-right.png")


def about_assets() -> None:
    placeholder("about-placeholder-main.png", (935, 880), radius=34)
    placeholder("about-placeholder-small-top.png", (535, 470), radius=30)
    placeholder("about-placeholder-small-bottom.png", (535, 355), radius=28)
    tape = Image.new("RGBA", (265, 140), (0, 0, 0, 0))
    d = ImageDraw.Draw(tape, "RGBA")
    d.polygon([(20, 42), (225, 8), (250, 92), (45, 128)], fill=(219, 176, 107, 145))
    save(tape, "about-tape.png")
    plant = Image.new("RGBA", (250, 390), (0, 0, 0, 0))
    d = ImageDraw.Draw(plant, "RGBA")
    d.line((120, 350, 145, 90), fill="#637655", width=7)
    for y in [120, 165, 210, 255, 300]:
        d.ellipse((90, y, 135, y+36), fill="#7f936b")
        d.ellipse((135, y-18, 185, y+20), fill="#596d50")
    save(plant, "about-plant.png")


def style_assets() -> None:
    placeholder("style-thumb.png", (775, 415), radius=22)
    for name, kind in [("style-car.png","car"),("style-tent.png","tent"),("style-bag.png","bag"),("style-tree.png","tree")]:
        img = Image.new("RGBA", (240, 180), (0,0,0,0))
        d = ImageDraw.Draw(img, "RGBA")
        if kind == "car":
            draw_car(d, 120, 105, .42)
        elif kind == "tent":
            draw_tent(d, 120, 140, .42)
        elif kind == "tree":
            draw_tree(d, 115, 145, .62)
        else:
            d.rounded_rectangle((78, 32, 158, 160), radius=18, fill="#b88a4b", outline="#5d5f42", width=5)
            d.rectangle((92, 92, 144, 136), fill="#8a6a42")
            d.line((92, 32, 70, 90), fill="#5d5f42", width=5)
            d.line((142, 32, 165, 90), fill="#5d5f42", width=5)
        save(img, name)


def activity_map() -> None:
    img = Image.new("RGBA", (2975, 1435), (0,0,0,0))
    d = ImageDraw.Draw(img, "RGBA")
    d.line([(120,720),(430,590),(650,810),(960,390),(1370,550),(1740,270),(2210,620),(2760,420)], fill=(255,255,255,180), width=8)
    for i in range(0, 2500, 55):
        y = int(700 + math.sin(i/150)*155)
        d.ellipse((120+i, y, 132+i, y+12), fill=(255,255,255,220))
    d.polygon([(1220, 365), (1360, 100), (1500, 365)], fill="#4a665d")
    d.polygon([(1430, 365), (1580, 150), (1750, 365)], fill="#6f8977")
    d.ellipse((180, 620, 370, 720), fill="#6b99a0")
    d.polygon([(255, 628), (320, 590), (295, 675)], fill="#fbf5df")
    draw_tent(d, 1120, 785, .36)
    for x in [2050, 2120, 2200]:
        draw_tree(d, x, 860, .35)
    for x,y,title,body in [
        (100,170,"카약 & 보트","호수 위에서 즐기는\n시원한 액티비티"),
        (1140,720,"캠프파이어","별빛 아래\n따뜻한 모닥불"),
        (2260,150,"하이킹 코스","숲길을 따라 걷는\n힐링 트레킹"),
        (520,1050,"별보기 명소","도심을 벗어난\n밤의 시간"),
        (2020,1050,"자연가 사이딩","자연 속 생태\n체험 코스"),
    ]:
        d.rounded_rectangle((x,y,x+520,y+190), radius=22, fill=(248,248,235,235))
        placeholder_box = (x+20,y+25,x+155,y+160)
        d.rounded_rectangle(placeholder_box, radius=14, fill="#d8d9d8")
        d.text((x+180,y+38), title, font=font(31, True), fill="#2f352d")
        d.text((x+180,y+88), body, font=font(24, True), fill="#5f665a", spacing=5)
    save(img, "activities-map.png")


def guide_news_assets() -> None:
    for name, kind in [("guide-bus.png","bus"),("guide-clock.png","clock"),("guide-wallet.png","wallet"),("guide-phone.png","phone")]:
        img = Image.new("RGBA", (230, 230), (0,0,0,0))
        d = ImageDraw.Draw(img, "RGBA")
        if kind == "bus":
            d.rounded_rectangle((55,35,175,180), radius=18, fill="#718569")
            d.rectangle((75,58,155,112), fill="#eef0e6")
            d.ellipse((72,170,100,198), fill="#454d43"); d.ellipse((130,170,158,198), fill="#454d43")
        elif kind == "clock":
            d.ellipse((38,30,190,182), fill="#f4f0dc", outline="#738260", width=10)
            d.line((114,106,114,55), fill="#766640", width=8); d.line((114,106,150,132), fill="#c28b45", width=8)
        elif kind == "wallet":
            d.rounded_rectangle((45,75,182,164), radius=15, fill="#738160")
            d.polygon([(48,75),(145,38),(172,76)], fill="#b99b55")
            d.rounded_rectangle((110,95,194,145), radius=14, fill="#60714f")
        else:
            d.arc((40,35,115,115), 130, 225, fill="#71815f", width=24)
            d.arc((95,95,185,185), -45, 42, fill="#71815f", width=24)
            d.arc((125,45,190,110), -35, 40, fill="#71815f", width=8)
        save(img, name)
    placeholder("news-thumb.png", (385, 388), radius=18)
    img = Image.new("RGBA", (865, 775), (0,0,0,0))
    d = ImageDraw.Draw(img, "RGBA")
    d.polygon([(120,480),(380,360),(700,420),(865,500),(865,775),(0,775),(0,560)], fill="#9cb177")
    for x,s in [(460,.8),(550,1),(650,.75)]:
        draw_tree(d, x, 570, s)
    draw_tent(d, 300, 620, .42)
    save(img, "news-side-art.png")


def main() -> None:
    paper_texture()
    band_texture("activities-bg.png", "#8cafb5")
    brand()
    placeholder("hero-placeholder.png", (1897, 1475), text="메인 비주얼 이미지", radius=55)
    torn("torn-hero-about.png", "#dfe8d8")
    torn_top("torn-style-activities.png", "#f4efdf", "#8cafb5")
    hero_left()
    hero_right()
    about_assets()
    style_assets()
    activity_map()
    guide_news_assets()


if __name__ == "__main__":
    main()
