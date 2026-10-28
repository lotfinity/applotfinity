"""Produce banner 05 from owner-supplied IstanbulPropTech desktop/mobile UI images.

The background uses abstract cartographic geometry, not invented map or property
statistics. Screenshots are retained, with no synthetic UI controls added.
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
ORIGINAL = ROOT / "media/original_images"
DEST = ROOT / "media/design_exports/05-istanbulproptech-banner-v1.webp"
SIZE = W, H = 1600, 900
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
TEAL = (56, 231, 180)


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, size)


def browser_mockup(image, source):
    x, y, w, h = 683, 202, 855, 513
    shadow = Image.new("RGBA", SIZE)
    s = ImageDraw.Draw(shadow)
    s.rounded_rectangle(
        (x + 18, y + 30, x + w + 18, y + h + 30), radius=24, fill=(0, 0, 0, 210)
    )
    image.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(36)))

    layer = Image.new("RGBA", SIZE)
    draw = ImageDraw.Draw(layer)
    draw.rounded_rectangle(
        (x, y, x + w, y + h),
        radius=25,
        fill=(9, 29, 32, 255),
        outline=(133, 213, 185, 170),
        width=3,
    )
    draw.rounded_rectangle(
        (x + 3, y + 3, x + w - 3, y + 47), radius=23, fill=(18, 47, 49, 255)
    )
    draw.rectangle((x + 4, y + 32, x + w - 4, y + 50), fill=(18, 47, 49, 255))
    for i, color in enumerate(
        ((248, 114, 117), (245, 190, 102), (102, 223, 169))
    ):
        px = x + 29 + i * 24
        draw.ellipse((px - 6, y + 20, px + 6, y + 32), fill=(*color, 255))
    draw.text(
        (x + 123, y + 15),
        "ISTANBULPROPTECH  /  PROPERTY MAP",
        font=font(17),
        fill=(186, 228, 219, 255),
    )

    screen = Image.open(source).convert("RGB")
    inner = (w - 18, h - 59)
    # Fit within the window without cropping the original map/sidebar interface.
    contained = ImageOps.contain(screen, inner, method=Image.Resampling.LANCZOS)
    screen_layer = Image.new("RGB", inner, (222, 237, 230))
    screen_layer.paste(
        contained,
        ((inner[0] - contained.width) // 2, (inner[1] - contained.height) // 2),
    )
    layer.paste(screen_layer, (x + 9, y + 52))
    ImageDraw.Draw(layer).rounded_rectangle(
        (x, y, x + w, y + h), radius=25, outline=(125, 218, 184, 190), width=2
    )
    image.alpha_composite(layer)


def phone_mockup(image, source):
    x, y, w = 1295, 438, 196
    source_image = Image.open(source).convert("RGB")
    h = round(w * source_image.height / source_image.width)
    layer = Image.new("RGBA", SIZE)
    draw = ImageDraw.Draw(layer)
    draw.rounded_rectangle(
        (x + 12, y + 16, x + w + 24, y + h + 28), radius=34, fill=(0, 0, 0, 210)
    )
    image.alpha_composite(layer.filter(ImageFilter.GaussianBlur(28)))
    frame = Image.new("RGBA", SIZE)
    draw = ImageDraw.Draw(frame)
    draw.rounded_rectangle(
        (x, y, x + w, y + h),
        radius=32,
        fill=(5, 25, 25, 255),
        outline=(75, 184, 155, 255),
        width=3,
    )
    inner_w, inner_h = w - 14, h - 16
    photo = ImageOps.contain(
        source_image, (inner_w, inner_h), Image.Resampling.LANCZOS
    )
    inner = Image.new("RGB", (inner_w, inner_h), (233, 247, 240))
    inner.paste(
        photo, ((inner_w - photo.width) // 2, (inner_h - photo.height) // 2)
    )
    mask = Image.new("L", inner.size)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, inner_w - 1, inner_h - 1), radius=25, fill=255
    )
    frame.paste(inner, (x + 7, y + 8), mask)
    draw = ImageDraw.Draw(frame)
    draw.rounded_rectangle(
        (x, y, x + w, y + h), radius=32, outline=(123, 229, 197, 200), width=2
    )
    draw.rounded_rectangle(
        (x + 70, y + 8, x + 127, y + 14), radius=5, fill=(9, 21, 22, 255)
    )
    image.alpha_composite(frame)


def main():
    desktop = ORIGINAL / "istanbulproptech-desktop.webp"
    mobile = ORIGINAL / "istanbulproptech-mobile.webp"
    for file in (desktop, mobile):
        if not file.is_file():
            raise FileNotFoundError(
                f"Missing existing CMS source image: {file}"
            )

    yy, xx = np.mgrid[0:H, 0:W]
    rgb = np.zeros((H, W, 3), dtype=np.float32)
    rgb[:] = (5, 21, 25)
    rgb += (xx / W)[..., None] * np.array((5, 17, 16), dtype=np.float32)
    for cx, cy, rx, ry, color, scale in (
        (1170, 355, 740, 520, (11, 127, 104), 0.55),
        (1500, 780, 630, 410, (22, 94, 128), 0.35),
        (250, 890, 650, 580, (16, 81, 68), 0.38),
    ):
        falloff = (
            np.exp(-(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2) * 2.1)
            * scale
        )
        rgb += falloff[..., None] * np.array(color, dtype=np.float32)
    rgb += np.random.default_rng(503).normal(0, 0.65, (H, W, 1))
    image = Image.fromarray(np.uint8(np.clip(rgb, 0, 255)), "RGB").convert(
        "RGBA"
    )

    overlay = Image.new("RGBA", SIZE)
    d = ImageDraw.Draw(overlay)
    rng = random.Random(503)
    for x in range(34, W + 70, 64):
        d.line((x, 0, x, H), fill=(111, 172, 150, 11), width=1)
    for y in range(19, H + 50, 64):
        d.line((0, y, W, y), fill=(111, 172, 150, 11), width=1)
    # Abstract transit/map paths. They are visual motifs, not actual city routes.
    for k in range(18):
        x = rng.randrange(60, 1620)
        y = rng.randrange(60, 890)
        vertices = [(x, y)]
        for step in range(5):
            x += rng.choice((-1, 1)) * rng.randrange(28, 100)
            y += rng.choice((-1, 1)) * rng.randrange(15, 57)
            vertices.append((x, y))
        d.line(vertices, fill=(84, 209, 182, rng.randint(22, 65)), width=1)
        d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(120, 242, 205, 115))
    # Three schematic map markers outside the original screenshots.
    for x, y in ((118, 761), (663, 143), (1531, 116)):
        d.ellipse(
            (x - 13, y - 13, x + 13, y + 13),
            outline=(69, 208, 164, 70),
            width=2,
        )
        d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(128, 239, 201, 160))
    image.alpha_composite(overlay)
    haze = Image.new("RGBA", SIZE)
    ImageDraw.Draw(haze).ellipse((820, 70, 1550, 780), fill=(49, 228, 180, 40))
    image.alpha_composite(haze.filter(ImageFilter.GaussianBlur(105)))

    browser_mockup(image, desktop)
    phone_mockup(image, mobile)
    d = ImageDraw.Draw(image)
    d.text(
        (87, 80),
        "LOTFINITY   /   SELECTED PROJECTS",
        font=font(18, True),
        fill=(151, 211, 190, 255),
    )
    d.line((91, 133, 639, 133), fill=(94, 172, 143, 120), width=2)
    d.text((78, 193), "05", font=font(112, True), fill=(53, 146, 112, 255))
    d.text(
        (88, 334), "ISTANBUL", font=font(71, True), fill=(246, 255, 251, 255)
    )
    d.text(
        (88, 426), "PROPTECH", font=font(76, True), fill=(145, 241, 199, 255)
    )
    d.rounded_rectangle((92, 525, 183, 533), radius=4, fill=(*TEAL, 255))
    d.text(
        (88, 569),
        "PROPERTY INTELLIGENCE",
        font=font(30, True),
        fill=(216, 246, 231, 255),
    )
    d.text(
        (91, 621),
        "EXPLORE  /  FILTER  /  COMPARE",
        font=font(18),
        fill=(167, 205, 188, 255),
    )

    x = 91
    for label in ("PROPERTY MAPS", "AREA CONTEXT", "LOCATION FILTERS"):
        f = font(14, True)
        bounds = d.textbbox((0, 0), label, font=f)
        width = bounds[2] - bounds[0] + 32
        d.rounded_rectangle(
            (x, 696, x + width, 736),
            radius=17,
            fill=(9, 60, 52, 220),
            outline=(54, 163, 128, 155),
        )
        d.text((x + 16, 709), label, font=f, fill=(167, 229, 206, 255))
        x += width + 11
    d.line((90, 812, 1510, 812), fill=(95, 183, 148, 118), width=2)
    d.text(
        (90, 835),
        "OWNER-SUPPLIED DESKTOP + MOBILE UI REFERENCES  ·  ISTANBUL MAPPING",
        font=font(15),
        fill=(123, 184, 155, 255),
    )
    d.text((1485, 828), "↗", font=font(25, True), fill=(*TEAL, 255))
    DEST.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(DEST, format="WEBP", quality=89, method=6)
    print(
        f"Banner created: {DEST} size={DEST.stat().st_size:,} bytes dimensions={W}x{H}"
    )


if __name__ == "__main__":
    main()
