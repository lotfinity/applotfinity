"""Register real Neon Strip Studio *web editor* captures in Wagtail.

These are screenshots of the running browser preview, not screenshots of
installed GNOME, Windows or Android packages. Never replace editor selections.
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


SOURCES = ROOT / "media/design_sources/neon-strip-studio"
CAPTURES = (
    (
        "device_desktop_image",
        "neon-real-desktop-edit-shape-20261029.png",
        "Neon Strip Studio real desktop web editor — offline demo, edit mode",
    ),
    (
        "device_mobile_image",
        "neon-real-mobile-edit-shape-20261029.png",
        "Neon Strip Studio real mobile browser editor — offline demo, edit mode",
    ),
)
project = AppPage.objects.get(slug="neon-strip-studio")
image_model = get_image_model()
modified = False
for field, source, title in CAPTURES:
    if getattr(project, field + "_id"):
        print("Preserving existing project screenshot:", field)
        continue
    path = SOURCES / source
    if not path.is_file():
        raise FileNotFoundError(path)
    image = image_model.objects.filter(title=title).first()
    if image is None:
        original = Image.open(path).convert("RGB")
        target = BytesIO()
        original.save(target, format="WEBP", quality=88, method=6)
        image = image_model.objects.create(
            title=title,
            file=ContentFile(
                target.getvalue(), name=source.replace(".png", ".webp")
            ),
        )
    setattr(project, field, image)
    modified = True
    print(
        "Wagtail image:",
        field,
        image.pk,
        image.width,
        image.height,
        image.file.url,
    )
if modified:
    if not project.mockup_design_id:
        project.mockup_design = project.device_desktop_image
    project.save_revision().publish()
    print("Published", project.title)
else:
    print("Screenshots already present; nothing overwritten.")
