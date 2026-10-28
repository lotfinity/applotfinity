"""Store two authentic installed LotoT Android screenshots in Wagtail.

This intentionally does not invent an Android desktop interface. Re-running
preserves any screenshot or mockup already chosen by a content editor.
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


SOURCES = ROOT / 'media/design_sources/lotot'
CAPTURES = (
    ('device_mobile_image', 'lotot-cockpit-initial-20261029.png',
     'LotoT original Android cockpit — no OBD adapter connected'),
    ('device_mobile_secondary_image', 'lotot-live-data-20261029.png',
     'LotoT real Android live phone sensor graphs — no OBD adapter'),
)
project = AppPage.objects.get(slug='lotot')
image_model = get_image_model()
modified = False
for field, source, title in CAPTURES:
    if getattr(project, field + '_id'):
        print('Existing screenshot preserved:', field)
        continue
    src = SOURCES / source
    if not src.is_file():
        raise FileNotFoundError(src)
    artwork = image_model.objects.filter(title=title).first()
    if artwork is None:
        screenshot = Image.open(src).convert('RGB')
        encoded = BytesIO()
        screenshot.save(encoded, format='WEBP', quality=87, method=6)
        artwork = image_model.objects.create(
            title=title,
            file=ContentFile(encoded.getvalue(), name=source.replace('.png', '.webp')),
        )
    setattr(project, field, artwork)
    print('Screenshot', field, 'id', artwork.pk, artwork.width, artwork.height)
    modified = True
if modified:
    if not project.mockup_design_id:
        project.mockup_design = project.device_mobile_image
    project.save_revision().publish()
    print('Published project:', project.title)
else:
    print('Already populated; left unchanged.')
