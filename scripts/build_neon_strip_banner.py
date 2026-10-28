"""Build 04 / Neon Strip Studio artwork from *real* web editor screenshots.

Source is running GitHub code in offline DEMO mode, captured with Chromium.
The decorative multicolor streaks are only typography/background atmosphere;
real editor pixels are preserved inside the browser/device frames.
"""

import math
import random
from pathlib import Path

import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter
from PIL import ImageFont
from PIL import ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "media/design_sources/neon-strip-studio"
TARGET = ROOT / "media/design_exports/04-neon-strip-studio-banner-v1.webp"
W, H = 1600, 900
REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(n, bold=False):
    return ImageFont.truetype(BOLD if bold else REGULAR, n)


def browser_mockup(back, x, y, w, h, source):
    shot = Image.open(source).convert("RGB")
    display = ImageOps.fit(
        shot, (w - 18, h - 59), Image.Resampling.LANCZOS, centering=(0.5, 0.3)
    )
    under = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(under)
    d.rounded_rectangle(
        (x + 16, y + 22, x + w + 20, y + h + 31), radius=28, fill=(0, 0, 0, 190)
    )
    back.alpha_composite(under.filter(ImageFilter.GaussianBlur(30)))
    frame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pen = ImageDraw.Draw(frame)
    pen.rounded_rectangle(
        (x, y, x + w, y + h),
        radius=22,
        fill=(13, 18, 31, 255),
        outline=(101, 100, 151, 255),
        width=2,
    )
    pen.rounded_rectangle(
        (x + 2, y + 2, x + w - 2, y + 53), radius=20, fill=(25, 29, 43, 255)
    )
    pen.rectangle((x + 3, y + 34, x + w - 3, y + 54), fill=(25, 29, 43, 255))
    pen.line(
        (x + 5, y + 54, x + w - 5, y + 54), fill=(98, 108, 141, 145), width=1
    )
    for k, color in enumerate(
        ((255, 109, 138), (255, 195, 98), (94, 218, 187))
    ):
        xx = x + 24 + k * 24
        pen.ellipse((xx - 6, y + 20, xx + 6, y + 32), fill=(*color, 255))
    pen.text(
        (x + 116, y + 16),
        "NEON STRIP STUDIO  /  SHAPE EDITOR",
        font=font(15),
        fill=(181, 195, 220, 255),
    )
    frame.paste(display, (x + 9, y + 56))
    pen = ImageDraw.Draw(frame)
    pen.rounded_rectangle(
        (x, y, x + w, y + h), radius=22, outline=(113, 148, 181, 175), width=2
    )
    back.alpha_composite(frame)


def phone_mockup(back, x, y, w, source):
    shot = Image.open(source).convert("RGB")
    h = round(w * (shot.height / shot.width))
    screen = ImageOps.fit(shot, (w - 14, h - 16), Image.Resampling.LANCZOS)
    mask = Image.new("L", screen.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, screen.width - 1, screen.height - 1),
        radius=round(w * 0.09),
        fill=255,
    )
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(
        (x + 9, y + 22, x + w + 16, y + h + 24),
        radius=round(w * 0.12),
        fill=(0, 0, 0, 180),
    )
    back.alpha_composite(layer.filter(ImageFilter.GaussianBlur(18)))
    device = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(device)
    d.rounded_rectangle(
        (x, y, x + w, y + h),
        radius=round(w * 0.11),
        fill=(4, 8, 14, 255),
        outline=(114, 126, 164, 245),
        width=3,
    )
    device.paste(screen.convert("RGBA"), (x + 7, y + 8), mask)
    d = ImageDraw.Draw(device)
    d.rounded_rectangle(
        (x, y, x + w, y + h),
        radius=round(w * 0.11),
        outline=(133, 143, 182, 185),
        width=3,
    )
    d.rounded_rectangle(
        (x + w * 0.37, y + 9, x + w * 0.63, y + 16),
        radius=4,
        fill=(3, 6, 13, 255),
    )
    back.alpha_composite(device)


def main():
    desktop = SOURCE / "neon-real-desktop-edit-shape-20261029.png"
    mobile = SOURCE / "neon-real-mobile-edit-shape-20261029.png"
    if not desktop.exists() or not mobile.exists():
        raise FileNotFoundError("Actual app screenshots missing")
    yy, xx = np.mgrid[0:H, 0:W]
    bg = np.zeros((H, W, 3), dtype=np.float32)
    bg[:] = (8, 9, 22)
    bg += (xx / W)[..., None] * np.array((6, 5, 15), dtype=np.float32)
    pools = [
        (1240, 330, 720, 470, (105, 42, 169), 0.63),
        (1430, 770, 500, 440, (12, 174, 194), 0.35),
        (370, 810, 590, 460, (84, 29, 117), 0.28),
    ]
    for cx, cy, rx, ry, hue, power in pools:
        radial = (
            np.exp(-(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2) * 2.3)
            * power
        )
        bg += radial[..., None] * np.array(hue, dtype=np.float32)
    bg += np.random.default_rng(4).normal(0, 0.65, (H, W, 1))
    art = Image.fromarray(np.uint8(np.clip(bg, 0, 255)), "RGB").convert("RGBA")
    pattern = Image.new("RGBA", (W, H))
    p = ImageDraw.Draw(pattern)
    rng = random.Random(402)
    for x in range(30, W, 74):
        p.line((x, 0, x, H), fill=(139, 140, 193, 10))
    for y in range(30, H, 74):
        p.line((0, y, W, y), fill=(139, 140, 193, 10))
    for _ in range(38):
        x = rng.randrange(65, W - 50)
        y = rng.randrange(20, H - 70)
        p.ellipse((x - 1, y - 1, x + 1, y + 1), fill=(172, 135, 243, 110))
    art.alpha_composite(pattern)
    # Neon stream ribbons; intentionally abstract, not simulated WLED measurements.
    glows = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(glows)
    for j, color in enumerate(((243, 65, 164), (164, 94, 249), (48, 209, 235))):
        path = []
        for step in range(75):
            x = 630 + step * 15
            y = (
                100
                + 25 * j
                + math.sin(step * 0.115 + j * 0.7) * 41
                + math.sin(step * 0.041 + j) * 27
            )
            path.append((x, y))
        d.line(path, fill=(*color, 100), width=11, joint="curve")
    art.alpha_composite(glows.filter(ImageFilter.GaussianBlur(23)))
    art.alpha_composite(glows)
    browser_mockup(art, 755, 225, 795, 485, desktop)
    phone_mockup(art, 1230, 456, 174, mobile)
    d = ImageDraw.Draw(art)
    d.text(
        (88, 82),
        "LOTFINITY   /   SELECTED PROJECTS",
        font=font(17, True),
        fill=(177, 174, 220, 255),
    )
    d.line((90, 132, 640, 132), fill=(147, 103, 194, 125), width=2)
    d.text((80, 197), "04", font=font(108, True), fill=(137, 78, 185, 255))
    d.text((88, 328), "NEON", font=font(91, True), fill=(250, 247, 255, 255))
    d.text(
        (89, 431),
        "STRIP STUDIO",
        font=font(54, True),
        fill=(229, 177, 255, 255),
    )
    d.rounded_rectangle(
        (91, 510, 184, 517), radius=4, fill=(218, 102, 240, 255)
    )
    d.text(
        (90, 549),
        "DESIGN LIGHT",
        font=font(37, True),
        fill=(181, 239, 247, 255),
    )
    d.text(
        (91, 607),
        "ONE CONTINUOUS STRIP",
        font=font(18),
        fill=(201, 195, 227, 255),
    )
    labels = ["150 LED GROUPS", "WLED PREVIEW", "CROSS-PLATFORM"]
    px = 89
    for label in labels:
        f = font(13, True)
        bbox = d.textbbox((0, 0), label, font=f)
        width = bbox[2] + 30
        d.rounded_rectangle(
            (px, 699, px + width, 736),
            radius=17,
            fill=(38, 23, 58, 230),
            outline=(139, 91, 181, 150),
            width=1,
        )
        d.text((px + 15, 709), label, font=f, fill=(204, 175, 244, 255))
        px += width + 9
    d.line((90, 812, 1510, 812), fill=(124, 91, 174, 139), width=2)
    d.text(
        (90, 835),
        "REAL WEB EDITOR  ·  OFFLINE DEMO  ·  EDITABLE WLED-STYLE LAYOUT",
        font=font(15),
        fill=(159, 155, 204, 255),
    )
    d.text((1477, 830), "↗", font=font(24, True), fill=(174, 231, 249, 255))
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    art.convert("RGB").save(TARGET, format="WEBP", quality=89, method=6)
    print(
        "Banner:", TARGET, "size:", TARGET.stat().st_size, "dimensions:", (W, H)
    )


if __name__ == "__main__":
    main()
