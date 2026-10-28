"""Render editorial project banners using verified screenshots, not invented UIs.

The first approved concept is Ohmlet. Other projects will be added one at a time
using project-specific palette, composition and source imagery.
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
EXPORTS = ROOT / 'media' / 'design_exports'
W, H = 1600, 900
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'


def font(size: int, bold: bool = False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def rounded(layer, box, fill, radius=20, outline=None, width=1):
    ImageDraw.Draw(layer).rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def build_ohmlet():
    rng = random.Random(1208)
    yy, xx = np.mgrid[0:H, 0:W]
    base = np.zeros((H, W, 3), dtype=np.float32)
    base[:] = (5, 12, 26)
    right = np.clip(xx / W, 0, 1)
    for j, color in enumerate((3, 11, 17)):
        base[:, :, j] += color * right
    for cx, cy, rx, ry, hue, intensity in [
        (1190, 350, 580, 470, (23, 145, 219), 0.35),
        (370, 800, 640, 580, (22, 85, 153), 0.23),
        (1590, 40, 520, 380, (0, 190, 221), 0.22),
    ]:
        radial = np.exp(-(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2) * 2.2) * intensity
        for j, color in enumerate(hue):
            base[:, :, j] += radial * color
    noise = np.random.default_rng(1108).normal(0, 0.8, (H, W, 1))
    base += noise
    image = Image.fromarray(np.uint8(np.clip(base, 0, 255)), 'RGB').convert('RGBA')

    ambient = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    pen = ImageDraw.Draw(ambient)
    # Faint technical grid and finely dotted PCB-node field.
    for x in range(50, W + 80, 64):
        pen.line((x, 0, x, H), fill=(72, 131, 176, 9), width=1)
    for y in range(32, H + 70, 64):
        pen.line((0, y, W, y), fill=(72, 131, 176, 9), width=1)
    for i in range(55):
        x = rng.randrange(70, W - 40)
        y = rng.randrange(40, H - 40)
        pen.ellipse((x - 1, y - 1, x + 1, y + 1), fill=(69, 201, 241, rng.randint(80, 170)))

    # Real circuit-trace motifs instead of misleading functional dashboards.
    for i in range(26):
        x0 = rng.randrange(620, W + 80)
        y0 = rng.randrange(50, H + 40)
        dx = rng.randint(55, 235) * (-1 if rng.random() < 0.5 else 1)
        dy = rng.randint(30, 125) * (-1 if rng.random() < 0.5 else 1)
        points = [(x0, y0), (x0 + dx * 0.56, y0), (x0 + dx, y0 + dy * 0.55), (x0 + dx * 1.34, y0 + dy * 0.55)]
        alpha = rng.randint(25, 75)
        pen.line(points, fill=(62, 192, 227, alpha), width=1)
        x1, y1 = points[-1]
        pen.ellipse((x1 - 3, y1 - 3, x1 + 3, y1 + 3), fill=(110, 225, 239, min(200, alpha * 2)))
    image = Image.alpha_composite(image, ambient)

    # Diffused cool-blue light where the authentic Ohmlet screenshot is placed.
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    g.rounded_rectangle((756, 175, 1575, 752), 39, fill=(26, 167, 231, 89))
    image = Image.alpha_composite(image, glow.filter(ImageFilter.GaussianBlur(92)))

    # Browser-mockup presentation of actual documented UI, not generated controls.
    x, y, bw, bh = 785, 190, 720, 500
    shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    rounded(shadow, (x + 14, y + 28, x + bw + 14, y + bh + 28), (0, 1, 7, 230), 31)
    image = Image.alpha_composite(image, shadow.filter(ImageFilter.GaussianBlur(26)))
    frame = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    rounded(frame, (x, y, x + bw, y + bh), (12, 25, 44, 255), 26, outline=(83, 168, 205, 180), width=2)
    rounded(frame, (x + 3, y + 4, x + bw - 3, y + 45), (19, 37, 59, 255), 23)
    fp = ImageDraw.Draw(frame)
    fp.rectangle((x + 4, y + 30, x + bw - 4, y + 46), fill=(19, 37, 59, 255))
    for idx, color in enumerate([(252, 99, 102), (246, 190, 84), (63, 207, 161)]):
        cx = x + 30 + idx * 24
        fp.ellipse((cx - 6, y + 20, cx + 6, y + 32), fill=color + (255,))
    fp.text((x + 126, y + 15), 'OHMLET  /  3D WORKSPACE', font=font(18), fill=(186, 213, 228, 255))
    screenshot = Image.open(ROOT / 'media/original_images/ohmlet-portfolio.webp').convert('RGB')
    content = ImageOps.fit(screenshot, (bw - 16, bh - 56), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    frame.paste(content, (x + 8, y + 48))
    fp = ImageDraw.Draw(frame)
    fp.rounded_rectangle((x, y, x + bw, y + bh), radius=26, outline=(91, 186, 231, 170), width=2)
    image = Image.alpha_composite(image, frame)

    # Brand hierarchy, legible at both full size and card thumbnail size.
    d = ImageDraw.Draw(image)
    d.text((94, 94), 'LOTFINITY   /   SELECTED PROJECTS', font=font(18, True), fill=(116, 202, 225, 255), stroke_width=0)
    d.line((94, 139, 640, 139), fill=(64, 138, 176, 105), width=2)
    d.text((86, 202), '01', font=font(103, True), fill=(33, 121, 164, 255))
    d.text((94, 319), 'OHMLET', font=font(94, True), fill=(245, 251, 255, 255), stroke_width=0)
    d.rounded_rectangle((95, 441, 181, 448), radius=3, fill=(68, 208, 238, 255))
    d.text((94, 477), '3D CIRCUIT', font=font(42, True), fill=(135, 235, 253, 255))
    d.text((94, 534), 'WORKBENCH', font=font(42, True), fill=(232, 243, 251, 255))
    d.text((96, 614), 'BUILD  /  WIRE  /  SIMULATE', font=font(21), fill=(181, 206, 218, 255))
    labels = ['3D BREADBOARD', 'ANALOG + DIGITAL', 'AI-ASSISTED']
    px = 94
    for label in labels:
        tw = ImageDraw.Draw(image).textbbox((0, 0), label, font=font(15, True))[2]
        width = tw + 32
        d.rounded_rectangle((px, 699, px + width, 737), radius=16, fill=(10, 42, 60, 229), outline=(58, 149, 178, 130), width=1)
        d.text((px + 16, 709), label, font=font(15, True), fill=(161, 221, 233, 255))
        px += width + 10
    d.line((94, 811, 1510, 811), fill=(75, 142, 176, 110), width=2)
    d.text((94, 835), 'ELECTRONICS  ×  SIMULATION  ×  CREATIVE ENGINEERING', font=font(16), fill=(110, 170, 192, 255))
    d.text((1451, 837), '↗', font=font(24, True), fill=(110, 220, 241, 255))

    EXPORTS.mkdir(parents=True, exist_ok=True)
    out = EXPORTS / '01-ohmlet-banner-v1.webp'
    image.convert('RGB').save(out, format='WEBP', quality=89, method=6)
    print('Banner:', out, f'{out.stat().st_size:,} bytes', image.size)
    return out


if __name__ == '__main__':
    build_ohmlet()
