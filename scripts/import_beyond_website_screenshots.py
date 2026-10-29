"""Import actual archived BeyondClinic screenshot assets to Beyond Website CMS.

Screens originate in the public beyond-website-v5 repository. The source files
are not captures from a currently verified live application. Preserve any
editor-selected Wagtail screenshots; re-running is idempotent.
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
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings.preview")

import django  # noqa: E402


django.setup()

from wagtail.images import get_image_model  # noqa: E402

from website.models import AppPage  # noqa: E402


SOURCES = ROOT / "media/design_sources/beyond-website"
CAPTURES = (
    (
        "device_desktop_image",
        "beyondclinic-desktop-source.png",
        "BeyondClinic — archived source-repository desktop dashboard screenshot",
    ),
    (
        "device_mobile_image",
        "beyondclinic-mobile-source.png",
        "BeyondClinic — archived source-repository mobile dashboard screenshot",
    ),
)
project = AppPage.objects.get(slug="beyond-website")
images = get_image_model()
changed = False
for field, filename, title in CAPTURES:
    if getattr(project, field + "_id"):
        print("Preserved existing editor screenshot:", field)
        continue
    path = SOURCES / filename
    if not path.is_file():
        raise FileNotFoundError(path)
    image = images.objects.filter(title=title).first()
    if image is None:
        source = Image.open(path).convert("RGB")
        encoded = BytesIO()
        source.save(encoded, format="WEBP", quality=88, method=6)
        image = images.objects.create(
            title=title,
            file=ContentFile(
                encoded.getvalue(), name=filename.replace(".png", ".webp")
            ),
        )
    setattr(project, field, image)
    changed = True
    print(
        "Imported", field, image.pk, image.width, image.height, image.file.url
    )
if changed:
    # Do not overwrite the separate promotional banner or claim this is live.
    project.save_revision().publish()
    print("Published archived Beyond Website screenshot mockups")
else:
    print("Screenshots already populated; no update")
