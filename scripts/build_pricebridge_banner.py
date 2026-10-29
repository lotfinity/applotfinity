"""Make 02 / PriceBridge from the *real* historical app screenshots.

Source: Wagtail's existing browser captures of the locally built private
PriceBridge preview, containing July 18, 2026 historical market evidence.
The graphics outside the screens are purely decorative. No fictional products,
exchange rates, buyer promises or live market figures are generated.
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
SOURCE = ROOT / "media/original_images"
DEST = ROOT / "media/design_exports/02-pricebridge-banner-v1.webp"
W, H = 1600, 900
SIZE = W, H
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MINT = (98, 236, 183)


def ft(n, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, n)


def desktop_mockup(bg, screenshot):
    x, y, w, h = 765, 207, 784, 503
    shadow = Image.new("RGBA", SIZE)
    ImageDraw.Draw(shadow).rounded_rectangle(
        (x + 15, y + 24, x + w + 15, y + h + 28),
        radius=25,
        fill=(0, 2, 13, 224),
    )
    bg.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(28)))
    panel = Image.new("RGBA", SIZE)
    d = ImageDraw.Draw(panel)
    d.rounded_rectangle(
        (x, y, x + w, y + h),
        radius=24,
        fill=(13, 35, 47, 255),
        outline=(107, 184, 168, 200),
        width=2,
    )
    d.rounded_rectangle(
        (x + 3, y + 3, x + w - 3, y + 49), radius=21, fill=(18, 45, 55, 255)
    )
    d.rectangle((x + 4, y + 32, x + w - 4, y + 50), fill=(18, 45, 55, 255))
    for i, c in enumerate(((249, 113, 112), (250, 190, 94), (86, 222, 151))):
        cx = x + 28 + i * 23
        d.ellipse((cx - 6, y + 22, cx + 6, y + 34), fill=c + (255,))
    d.text(
        (x + 123, y + 16),
        "PRICEBRIDGE  /  MARKET COMPARISON",
        font=ft(16),
        fill=(175, 222, 210, 255),
    )

    src = Image.open(screenshot).convert("RGB")
    inner = (w - 16, h - 60)
    fitted = ImageOps.contain(src, inner, method=Image.Resampling.LANCZOS)
    layer = Image.new("RGB", inner, (245, 248, 247))
    layer.paste(
        fitted,
        ((inner[0] - fitted.width) // 2, (inner[1] - fitted.height) // 2),
    )
    panel.paste(layer, (x + 8, y + 54))
    ImageDraw.Draw(panel).rounded_rectangle(
        (x, y, x + w, y + h), radius=24, outline=(120, 214, 178, 205), width=2
    )
    bg.alpha_composite(panel)


def mobile_mockup(bg, screenshot):
    x, y, w = 1300, 442, 199
    src = Image.open(screenshot).convert("RGB")
    h = round(w * src.height / src.width)
    blur = Image.new("RGBA", SIZE)
    ImageDraw.Draw(blur).rounded_rectangle(
        (x + 14, y + 24, x + w + 22, y + h + 25),
        radius=34,
        fill=(0, 3, 14, 227),
    )
    bg.alpha_composite(blur.filter(ImageFilter.GaussianBlur(24)))

    phone = Image.new("RGBA", SIZE)
    d = ImageDraw.Draw(phone)
    d.rounded_rectangle(
        (x, y, x + w, y + h),
        radius=31,
        fill=(5, 17, 25, 255),
        outline=(125, 213, 180, 230),
        width=3,
    )
    inner = (w - 14, h - 16)
    src = ImageOps.contain(src, inner, method=Image.Resampling.LANCZOS)
    padded = Image.new("RGB", inner, (247, 248, 247))
    padded.paste(
        src, ((inner[0] - src.width) // 2, (inner[1] - src.height) // 2)
    )
    mask = Image.new("L", inner)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, inner[0] - 1, inner[1] - 1), radius=24, fill=255
    )
    phone.paste(padded, (x + 7, y + 8), mask)
    d = ImageDraw.Draw(phone)
    d.rounded_rectangle(
        (x, y, x + w, y + h), radius=31, outline=(145, 231, 196, 225), width=2
    )
    d.rounded_rectangle(
        (x + 73, y + 8, x + 127, y + 14), radius=5, fill=(9, 18, 23, 255)
    )
    bg.alpha_composite(phone)


def main():
    desktop = SOURCE / "pricebridge-desktop-card-scroll180-20261029.webp"
    mobile = SOURCE / "pricebridge-mobile-card-scroll370-20261029.webp"
    for path in (desktop, mobile):
        if not path.is_file():
            raise FileNotFoundError(path)

    yy, xx = np.mgrid[0:H, 0:W]
    rgb = np.zeros((H, W, 3), dtype=np.float32)
    rgb[:] = (7, 20, 36)
    rgb += (xx / W)[..., None] * np.array((5, 20, 25), dtype=np.float32)
    for cx, cy, rx, ry, col, scale in (
        (1260, 341, 640, 535, (20, 125, 137), 0.54),
        (350, 840, 670, 540, (14, 63, 121), 0.44),
        (1600, 770, 460, 460, (29, 148, 112), 0.26),
    ):
        g = (
            np.exp(-(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2) * 2.25)
            * scale
        )
        rgb += g[..., None] * np.array(col, dtype=np.float32)
    rgb += np.random.default_rng(202).normal(0, 0.6, (H, W, 1))
    bg = Image.fromarray(np.uint8(np.clip(rgb, 0, 255)), "RGB").convert("RGBA")
    overlay = Image.new("RGBA", SIZE)
    d = ImageDraw.Draw(overlay)
    for x in range(30, W + 50, 72):
        d.line((x, 0, x, H), fill=(90, 170, 180, 12), width=1)
    for y in range(24, H + 50, 72):
        d.line((0, y, W, y), fill=(90, 170, 180, 12), width=1)
    rng = random.Random(2026)
    # Abstract connections: evidence -> normalized variant -> market comparison.
    # Neither the lines nor the nodes imply additional real market records.
    for i in range(21):
        x = rng.randrange(630, 1600)
        y = rng.randrange(50, H - 40)
        points = [(x, y)]
        for j in range(3):
            x += rng.choice((-1, 1)) * rng.randrange(45, 125)
            y += rng.choice((-1, 1)) * rng.randrange(18, 60)
            points.append((x, y))
        d.line(points, fill=(85, 202, 177, rng.randrange(23, 67)), width=1)
        d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(123, 237, 192, 127))
    for i in range(30):
        x, y = rng.randrange(64, W - 40), rng.randrange(30, H - 36)
        d.ellipse((x - 1, y - 1, x + 1, y + 1), fill=(155, 212, 206, 93))
    bg.alpha_composite(overlay)
    glow = Image.new("RGBA", SIZE)
    ImageDraw.Draw(glow).ellipse((850, 95, 1570, 770), fill=(53, 204, 172, 42))
    bg.alpha_composite(glow.filter(ImageFilter.GaussianBlur(95)))

    desktop_mockup(bg, desktop)
    mobile_mockup(bg, mobile)
    d = ImageDraw.Draw(bg)
    d.text(
        (88, 80),
        "LOTFINITY   /   SELECTED PROJECTS",
        font=ft(18, True),
        fill=(152, 211, 212, 255),
    )
    d.line((91, 134, 652, 134), fill=(95, 178, 177, 116), width=2)
    d.text((77, 197), "02", font=ft(113, True), fill=(44, 139, 138, 255))
    d.text((87, 326), "PRICE", font=ft(94, True), fill=(249, 252, 255, 255))
    d.text((88, 435), "BRIDGE", font=ft(94, True), fill=(154, 239, 210, 255))
    d.rounded_rectangle((93, 540, 185, 548), radius=4, fill=(*MINT, 255))
    d.text((90, 579), "MARKET", font=ft(34, True), fill=(220, 245, 244, 255))
    d.text(
        (90, 622), "INTELLIGENCE", font=ft(34, True), fill=(220, 245, 244, 255)
    )
    x = 90
    for item in ("LISTING EVIDENCE", "VARIANT MATCHING", "COMPARISON"):
        f = ft(13, True)
        width = d.textbbox((0, 0), item, font=f)[2] + 27
        d.rounded_rectangle(
            (x, 705, x + width, 741),
            radius=16,
            fill=(13, 54, 65, 230),
            outline=(71, 178, 156, 140),
        )
        d.text((x + 14, 715), item, font=f, fill=(171, 227, 211, 255))
        x += width + 9
    d.line((90, 813, 1512, 813), fill=(86, 165, 161, 125), width=2)
    d.text(
        (90, 837),
        "ACTUAL APPLICATION UI  ·  HISTORICAL JULY 2026 DATA  ·  NOT LIVE OFFERS",
        font=ft(15),
        fill=(134, 194, 190, 255),
    )
    d.text((1486, 830), "↗", font=ft(25, True), fill=(*MINT, 255))

    DEST.parent.mkdir(parents=True, exist_ok=True)
    bg.convert("RGB").save(DEST, format="WEBP", quality=89, method=6)
    print("Generated", DEST, "size", DEST.stat().st_size, "dimensions", SIZE)


if __name__ == "__main__":
    main()
