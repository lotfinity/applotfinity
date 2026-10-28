"""Import authentic, archival PriceBridge screenshots into Wagtail device fields.

This is an explicit one-off assistant-reviewed preview asset import. Never
replace owner-selected graphics and never confuse illustrations with screenshots.
"""
from __future__ import annotations

import os
import sys
from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings.preview')

import django  # noqa: E402


django.setup()

from wagtail.images import get_image_model  # noqa: E402

from website.models import AppPage  # noqa: E402


SOURCES = Path('/home/lofa/DEV/portfolio-previews/pricebridge-deploy/screenshots')
CAPTURES = (
    ('device_desktop_image', 'pricebridge-desktop-card-scroll180-20261029.png',
     'PriceBridge genuine desktop UI — historical evidence from 18 July 2026'),
    ('device_mobile_image', 'pricebridge-mobile-card-scroll370-20261029.png',
     'PriceBridge genuine mobile UI — historical evidence from 18 July 2026'),
)
project = AppPage.objects.get(slug='pricebridge')
image_model = get_image_model()
modified = False
for field, source, title in CAPTURES:
    if getattr(project, field + '_id'):
        print('Preserved existing screenshot:', field)
        continue
    src = SOURCES / source
    if not src.is_file():
        raise FileNotFoundError(src)
    image = image_model.objects.filter(title=title).first()
    if image is None:
        im = Image.open(src).convert('RGB')
        target = BytesIO()
        im.save(target, format='WEBP', quality=84, method=5)
        image = image_model.objects.create(
            title=title,
            file=ContentFile(target.getvalue(), name=source.replace('.png', '.webp')),
        )
    setattr(project, field, image)
    print('Created Wagtail image:', field, 'id', image.pk, 'url', image.file.url)
    modified = True
if modified:
    project.save_revision().publish()
    print('Published updated PriceBridge case study:', project.url)
else:
    print('Already imported; no changes.')
