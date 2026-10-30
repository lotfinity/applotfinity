"""Safely publish one reviewed GitHub project at a time to Wagtail.

Usage: python scripts/update_source_case_study.py ohmlet
The curated source metadata is in website/project_source_stories.py.
"""

from __future__ import annotations

import os
import sys
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings.preview")

import django  # noqa: E402


django.setup()

from website.models import AppPage  # noqa: E402
from website.models import TechStack  # noqa: E402
from website.project_source_stories import STORIES  # noqa: E402


TAGS = {
    "ohmlet": [
        "React",
        "TypeScript",
        "Three.js",
        "ESP32",
        "MCP",
        "WebAssembly",
    ],
    "pricebridge": [
        "Django",
        "Python",
        "Data Engineering",
        "Market Intelligence",
    ],
    "neon-strip-studio": ["WebGL", "Canvas", "WLED", "Electron", "Android"],
    "istanbulproptech": ["Django", "JavaScript", "Geospatial", "Mapping"],
    "beyond-website": [
        "Django",
        "Python",
        "Healthcare Operations",
        "Bootstrap",
    ],
}


def run(slug: str):
    if slug not in STORIES:
        raise ValueError(f"Unrecognized reviewed project: {slug}")
    story = STORIES[slug]
    p = AppPage.objects.get(slug=slug)
    expected_repo = "https://github.com/lotfinity/" + (
        "IstanbulPropTech"
        if slug == "istanbulproptech"
        else "beyond-website-v5"
        if slug == "beyond-website"
        else "pricebridge-clean"
        if slug == "pricebridge"
        else "neon-strip-studio"
        if slug == "neon-strip-studio"
        else "ohmlet"
    )
    if p.source_url.rstrip("/") != expected_repo:
        raise RuntimeError("Source repo mismatch: not modifying project")
    blocks = p.body.raw_data
    if blocks:
        if p.title == story["title"] and any(
            "Source-reviewed engineering narrative" in str(b) for b in blocks
        ):
            print("ALREADY_UPDATED", slug, p.pk)
            return
        raise RuntimeError(
            "Found existing editorial body; preserving it instead of replacing"
        )
    media_ids_before = {
        name: getattr(p, name + "_id")
        for name in (
            "banner_image",
            "mockup_design",
            "device_desktop_image",
            "device_mobile_image",
            "device_mobile_secondary_image",
        )
    }
    if not media_ids_before["banner_image"] or not any(
        media_ids_before[k]
        for k in ("device_desktop_image", "device_mobile_image")
    ):
        raise RuntimeError("Images not populated; refusing update")
    p.title = story["title"]
    p.description = story["description"]
    p.focus_area = story["focus"]
    p.key_features = "\n".join(story["features"])
    body = [("heading", "<h2>Source-reviewed engineering narrative</h2>")]
    for title, paragraph in story["body"]:
        body.append(("heading", "<h3>" + escape(title) + "</h3>"))
        body.append(("paragraph", "<p>" + escape(paragraph) + "</p>"))
    body += [
        ("heading", "<h2>Verification and source</h2>"),
        (
            "paragraph",
            "<p>The latest <strong>public main-branch commit</strong> reviewed for this case study is "
            '<a href="'
            + escape(p.source_url)
            + "/commit/"
            + escape(story["sha"])
            + '">'
            + escape(story["sha"][:9])
            + "</a> "
            "("
            + escape(story["verified"])
            + "). The project status and claims are limited by the caveats above; "
            "no production service or new hardware test was independently demonstrated.</p>",
        ),
    ]
    p.body = body
    for tag in TAGS[slug]:
        tech, _ = TechStack.objects.get_or_create(name=tag)
        p.tech_stack.add(tech)
    p.save_revision().publish()
    media_ids_after = {
        name: getattr(p, name + "_id") for name in media_ids_before
    }
    assert (
        media_ids_after == media_ids_before
    ), "Image fields unexpectedly changed"
    print(
        "UPDATED",
        slug,
        "page",
        p.pk,
        "blocks",
        len(p.body),
        "features",
        len(p.feature_items),
        "commit",
        story["sha"][:9],
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Pass one project slug at a time")
    run(sys.argv[1])
