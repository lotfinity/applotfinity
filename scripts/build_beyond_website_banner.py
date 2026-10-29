"""Build project 06 from actual desktop/mobile BeyondClinic screenshots.

Source: lotfinity/beyond-website-v5 commit f77d0fe, repository assets
staticfiles/assets/img/screenshot1.png and screenshot2.png.
These are archived UI-reference screenshots, not live patient data or a verified
running production deployment. No numbers or medical information are invented.
"""

from __future__ import annotations

import random
from pathlib import Path

import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter
from PIL import ImageFont
from PIL import ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "media/design_sources/beyond-website"
DEST = ROOT / "media/design_exports/06-beyond-website-banner-v1.webp"
W, H = 1600, 900
SIZE = (W, H)
BLUE = (100, 120, 244)
MINT = (62, 227, 192)
CORAL = (253, 118, 114)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def ft(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def desktop_frame(base, source):
    x, y, w, h = 751, 223, 793, 502
    sh = Image.new("RGBA", SIZE)
    ImageDraw.Draw(sh).rounded_rectangle(
        (x + 22, y + 33, x + w + 22, y + h + 33),
        radius=25,
        fill=(1, 6, 24, 220),
    )
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(33)))

    frame = Image.new("RGBA", SIZE)
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle(
        (x, y, x + w, y + h),
        radius=24,
        fill=(18, 28, 55, 255),
        outline=(133, 143, 220, 185),
        width=2,
    )
    d.rounded_rectangle(
        (x + 3, y + 3, x + w - 3, y + 51), radius=21, fill=(31, 40, 77, 255)
    )
    d.rectangle((x + 4, y + 33, x + w - 4, y + 54), fill=(31, 40, 77, 255))
    for i, c in enumerate(((248, 111, 129), (247, 185, 97), (88, 219, 162))):
        cx = x + 29 + 23 * i
        d.ellipse((cx - 6, y + 23, cx + 6, y + 35), fill=c + (255,))
    d.text(
        (x + 126, y + 17),
        "BEYONDCLINIC  /  SERVICE DASHBOARD",
        font=ft(16),
        fill=(193, 205, 242, 255),
    )
    screenshot = Image.open(source).convert("RGB")
    target = (w - 16, h - 60)
    fitted = ImageOps.contain(
        screenshot, target, method=Image.Resampling.LANCZOS
    )
    background = Image.new("RGB", target, (234, 239, 251))
    background.paste(
        fitted,
        ((target[0] - fitted.width) // 2, (target[1] - fitted.height) // 2),
    )
    frame.paste(background, (x + 8, y + 55))
    ImageDraw.Draw(frame).rounded_rectangle(
        (x, y, x + w, y + h), radius=24, outline=(157, 163, 238, 200), width=2
    )
    base.alpha_composite(frame)


def phone_frame(base, source):
    x, y, w = 1318, 421, 187
    img = Image.open(source).convert("RGB")
    h = round(w * img.height / img.width)
    sh = Image.new("RGBA", SIZE)
    ImageDraw.Draw(sh).rounded_rectangle(
        (x + 13, y + 21, x + w + 17, y + h + 27),
        radius=31,
        fill=(2, 8, 28, 220),
    )
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(21)))

    layer = Image.new("RGBA", SIZE)
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(
        (x, y, x + w, y + h),
        radius=28,
        fill=(9, 14, 29, 255),
        outline=(156, 163, 224, 240),
        width=2,
    )
    ww, hh = w - 14, h - 16
    contained = ImageOps.contain(img, (ww, hh), method=Image.Resampling.LANCZOS)
    padded = Image.new("RGB", (ww, hh), (244, 246, 253))
    padded.paste(
        contained, ((ww - contained.width) // 2, (hh - contained.height) // 2)
    )
    mask = Image.new("L", (ww, hh))
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, ww - 1, hh - 1), radius=21, fill=255
    )
    layer.paste(padded, (x + 7, y + 8), mask)
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(
        (x, y, x + w, y + h), radius=28, outline=(172, 176, 244, 235), width=2
    )
    d.rounded_rectangle(
        (x + 67, y + 8, x + 123, y + 15), radius=5, fill=(8, 13, 26, 255)
    )
    base.alpha_composite(layer)


def main():
    desktop = SOURCES / "beyondclinic-desktop-source.png"
    mobile = SOURCES / "beyondclinic-mobile-source.png"
    for path in (desktop, mobile):
        if not path.is_file():
            raise FileNotFoundError(path)

    yy, xx = np.mgrid[0:H, 0:W]
    color = np.zeros((H, W, 3), dtype=np.float32)
    color[:] = (9, 14, 34)
    color += (xx / W)[..., None] * np.array((15, 17, 40), dtype=np.float32)
    for cx, cy, rx, ry, hue, power in (
        (1115, 300, 650, 500, (107, 95, 239), 0.60),
        (1510, 760, 530, 400, (52, 172, 196), 0.32),
        (390, 830, 570, 530, (53, 77, 190), 0.31),
    ):
        strength = (
            np.exp(-(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2) * 2.25)
            * power
        )
        color += strength[..., None] * np.array(hue, dtype=np.float32)
    color += np.random.default_rng(6).normal(0, 0.65, (H, W, 1))
    bg = Image.fromarray(np.uint8(np.clip(color, 0, 255)), "RGB").convert(
        "RGBA"
    )

    decoration = Image.new("RGBA", SIZE)
    d = ImageDraw.Draw(decoration)
    rng = random.Random(606)
    for x in range(40, W + 40, 72):
        d.line((x, 0, x, H), fill=(135, 152, 236, 12), width=1)
    for y in range(28, H + 50, 72):
        d.line((0, y, W, y), fill=(135, 152, 236, 12), width=1)
    # Decorative workflow graph, not a claimed working interface.
    for i in range(14):
        x = rng.randrange(680, W)
        y = rng.randrange(75, H - 55)
        segments = [(x, y)]
        for j in range(3):
            x += rng.randrange(-130, 131)
            y += rng.randrange(-70, 71)
            segments.append((x, y))
        d.line(segments, fill=(*BLUE, rng.randint(24, 68)), width=2)
        d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(*MINT, 120))
    for i in range(35):
        x = rng.randrange(72, W - 30)
        y = rng.randrange(30, H - 30)
        d.ellipse((x - 1, y - 1, x + 1, y + 1), fill=(186, 195, 247, 84))
    bg.alpha_composite(decoration)

    haze = Image.new("RGBA", SIZE)
    ImageDraw.Draw(haze).ellipse((875, 65, 1550, 820), fill=(92, 101, 247, 65))
    bg.alpha_composite(haze.filter(ImageFilter.GaussianBlur(90)))
    desktop_frame(bg, desktop)
    phone_frame(bg, mobile)

    d = ImageDraw.Draw(bg)
    d.text(
        (86, 78),
        "LOTFINITY   /   SELECTED PROJECTS",
        font=ft(18, True),
        fill=(166, 182, 236, 255),
    )
    d.line((90, 131, 655, 131), fill=(135, 148, 219, 112), width=2)
    d.text((78, 186), "06", font=ft(113, True), fill=(98, 107, 212, 255))
    d.text((87, 319), "BEYOND", font=ft(85, True), fill=(247, 248, 255, 255))
    d.text((88, 424), "WEBSITE", font=ft(85, True), fill=(181, 191, 255, 255))
    d.rounded_rectangle((91, 522, 186, 530), radius=3, fill=(*MINT, 255))
    d.text((89, 565), "CONNECTED", font=ft(35, True), fill=(214, 239, 249, 255))
    d.text((89, 615), "SERVICES", font=ft(35, True), fill=(214, 239, 249, 255))
    x = 90
    for text, hue in (
        ("PATIENT PORTAL", BLUE),
        ("APPOINTMENTS", CORAL),
        ("OPERATIONS", MINT),
    ):
        f = ft(13, True)
        bounds = d.textbbox((0, 0), text, font=f)
        ww = bounds[2] + 31
        d.rounded_rectangle(
            (x, 697, x + ww, 735),
            radius=17,
            fill=(19, 29, 66, 240),
            outline=(*hue, 140),
            width=1,
        )
        d.text((x + 15, 709), text, font=f, fill=(202, 215, 253, 255))
        x += ww + 9
    d.line((90, 813, 1512, 813), fill=(128, 149, 218, 119), width=2)
    d.text(
        (90, 837),
        "ARCHIVED APPLICATION UI REFERENCES  ·  BEYONDCLINIC / DJANGO",
        font=ft(15),
        fill=(162, 179, 227, 255),
    )
    d.text((1485, 827), "↗", font=ft(25, True), fill=(*MINT, 255))

    DEST.parent.mkdir(parents=True, exist_ok=True)
    bg.convert("RGB").save(DEST, "WEBP", quality=89, method=6)
    print("Generated", DEST, "bytes", DEST.stat().st_size, "dimensions", (W, H))


if __name__ == "__main__":
    main()
