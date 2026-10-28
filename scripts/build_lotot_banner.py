"""Generate project 03: LotoT banner using actual Android screenshots.

No fake OBD readings or invented desktop app. Sources are authentic app screens
captured over ADB from a connected Samsung phone on 2026-10-29.
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


BASE = Path(__file__).resolve().parents[1]
CAPTURES = BASE / 'media/design_sources/lotot'
TARGET = BASE / 'media/design_exports/03-lotot-banner-v1.webp'
W, H = 1600, 900
BG = (7, 11, 15)
LIME = (202, 248, 55)
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'


def font(size, bold=False):
    return ImageFont.truetype(FB if bold else F, size)


def panel(image, x, y, w, source, *, glow=False):
    """Android device frame containing unchanged screenshot pixels."""
    shot = Image.open(source).convert('RGB')
    h = round(w * shot.height / shot.width)
    mask = Image.new('L', (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, w - 1, h - 1), radius=round(w * .115), fill=255)
    screen = ImageOps.fit(shot, (w, h), method=Image.Resampling.LANCZOS)
    sticker = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    sticker.paste(screen.convert('RGBA'), (0, 0), mask)

    under = Image.new('RGBA', image.size)
    sd = ImageDraw.Draw(under)
    sd.rounded_rectangle((x - 8, y - 8, x + w + 8, y + h + 8),
                         radius=round(w * .11), fill=(2, 6, 8, 255),
                         outline=(115, 152, 120, 235) if glow else (54, 73, 74, 235), width=3)
    shadow = Image.new('RGBA', image.size)
    ImageDraw.Draw(shadow).rounded_rectangle((x + 12, y + 30, x + w + 28, y + h + 30),
                                             radius=round(w * .1), fill=(0, 0, 0, 190))
    image.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(27)))
    image.alpha_composite(under)
    image.alpha_composite(sticker, dest=(x, y))
    d = ImageDraw.Draw(image)
    d.rounded_rectangle((x - 8, y - 8, x + w + 8, y + h + 8),
                        radius=round(w * .11), outline=(162, 210, 87, 135) if glow else (77, 101, 103, 255), width=3)
    # Deliberately do not add simulated phone sensors or synthetic diagnostic UI.


def main():
    for filename in ('lotot-cockpit-initial-20261029.png', 'lotot-live-data-20261029.png'):
        if not (CAPTURES / filename).is_file():
            raise FileNotFoundError(CAPTURES / filename)

    y, x = np.mgrid[0:H, 0:W]
    rgb = np.zeros((H, W, 3), dtype=np.float32)
    rgb[:] = BG
    rgb += (x / W)[..., None] * np.array([4, 9, 5], dtype=np.float32)
    radial = np.exp(-(((x - 1240) / 670) ** 2 + ((y - 420) / 590) ** 2) * 1.75)
    rgb += radial[..., None] * np.array([33, 76, 28], dtype=np.float32)
    radial2 = np.exp(-(((x - 500) / 950) ** 2 + ((y - 790) / 490) ** 2) * 2.5)
    rgb += radial2[..., None] * np.array([8, 15, 17], dtype=np.float32)
    grain = np.random.default_rng(16).normal(0, .6, (H, W, 1))
    img = Image.fromarray(np.uint8(np.clip(rgb + grain, 0, 255)), 'RGB').convert('RGBA')
    overlay = Image.new('RGBA', (W, H))
    d = ImageDraw.Draw(overlay)
    rng = random.Random(29)
    for gx in range(35, W, 76):
        d.line((gx, 10, gx, H - 20), fill=(130, 180, 130, 12), width=1)
    for gy in range(40, H, 76):
        d.line((25, gy, W - 15, gy), fill=(130, 180, 130, 11), width=1)

    # Abstract sensor-network traces. These are ornamental, not vehicle data.
    for k in range(18):
        sx = rng.randrange(620, 1650)
        sy = rng.randrange(40, 900)
        points=[(sx,sy)]
        for i in range(4):
            sx += rng.choice((-1,1))*rng.randrange(29,95)
            sy += rng.choice((-1,1))*rng.randrange(12,42)
            points.append((sx,sy))
        d.line(points,fill=(*LIME,rng.randint(24,65)),width=1)
        d.ellipse((sx-2,sy-2,sx+2,sy+2),fill=(*LIME,90))
    for i in range(45):
        xx = rng.randrange(70,1570)
        yy = rng.randrange(45,840)
        d.ellipse((xx-1,yy-1,xx+1,yy+1),fill=(*LIME,55))
    img.alpha_composite(overlay)

    haze = Image.new('RGBA', (W,H))
    hd=ImageDraw.Draw(haze)
    hd.ellipse((900,95,1550,760),fill=(178,240,40,70))
    img.alpha_composite(haze.filter(ImageFilter.GaussianBlur(110)))

    # Real Android screens. Reference device renders from the connected APK.
    panel(img, 824, 120, 332, CAPTURES / 'lotot-cockpit-initial-20261029.png', glow=True)
    panel(img, 1214, 234, 252, CAPTURES / 'lotot-live-data-20261029.png')

    d = ImageDraw.Draw(img)
    d.text((88,82), 'LOTFINITY   /   SELECTED PROJECTS',font=font(17,True),fill=(132,184,156,255))
    d.line((90,131,645,131),fill=(109,163,104,90),width=2)
    d.text((79,189),'03',font=font(115,True),fill=(88,141,60,255))
    d.text((87,327),'LotoT',font=font(111,True),fill=(249,254,247,255))
    d.rounded_rectangle((91,458,184,465),radius=4,fill=(*LIME,255))
    d.text((88,499),'ANDROID OBD-II',font=font(38,True),fill=(*LIME,255))
    d.text((88,551),'DIAGNOSTICS',font=font(38,True),fill=(231,247,235,255))
    d.text((90,636),'CONNECT   /   MONITOR   /   DIAGNOSE',font=font(17),fill=(163,191,170,255))

    labels=['VEHICLE HEALTH','LIVE SENSORS','FAULT CODES']
    px=88
    for label in labels:
        tbox=d.textbbox((0,0),label,font=font(13,True))
        width=tbox[2]-tbox[0]+31
        d.rounded_rectangle((px,699,px+width,735),radius=16,fill=(24,49,30,230),outline=(103,174,75,130),width=1)
        d.text((px+15,710),label,font=font(13,True),fill=(183,232,164,255))
        px += width+10
    d.line((90,812,1511,812),fill=(100,167,84,109),width=2)
    d.text((90,834),'ACTUAL APP UI  ·  UNCONNECTED OBD STATUS  ·  SAMSUNG ANDROID CAPTURE',
           font=font(14),fill=(122,172,139,255))
    d.text((1481,829),'↗',font=font(25,True),fill=(*LIME,255))
    TARGET.parent.mkdir(parents=True,exist_ok=True)
    img.convert('RGB').save(TARGET,'WEBP',quality=88,method=6)
    print('Generated',TARGET,'dimensions',W,H,'bytes',TARGET.stat().st_size)


if __name__=='__main__':
    main()
