"""Enrich only the LotoT Wagtail record from verified upstream Git history.

Source: https://github.com/lotfinity/lotot-android (main, b4911b2,
2026-08-14). This is an idempotent one-time content migration, not an app build.
Keeps original captured screenshots/banner and respects later human editing.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings.preview")

import django  # noqa: E402


django.setup()

from website.models import AppPage  # noqa: E402
from website.models import TechStack  # noqa: E402


SOURCE_COMMIT = "b4911b26fe6e3518831595dab759746178dd4cdb"
REPO = "https://github.com/lotfinity/lotot-android"

DESCRIPTION = (
    "An Android vehicle-health companion combining AndrOBD diagnostics, a React "
    "cockpit, GPS and phone sensors, resilient MQTT telemetry and LoToTi—an "
    "evidence-first AI copilot. Vehicle-health conclusions require actual ECU data."
)
FEATURES = [
    "Native ELM327/OBD-II diagnostics: live PIDs, fault codes, freeze frames and vehicle information",
    "React/WebView cockpit with low-latency charts, multilingual UI and light/dark appearance",
    "Built-in GPS and motion sensors with explicit provenance separate from ECU signals",
    "Foreground MQTT gateway: device UID topics, secure credentials, durable queue and reconnect handling",
    "LoToTi diagnostic copilot: local DTC database, streamed AI explanations and evidence-first rules",
    "Configurable LiteLLM, Codex and StepFun model fallback with additional provider options",
    "Standalone branding, onboarding, Bluetooth connection flow and access to AndrOBD advanced tools",
]

# Wagtail RichText content is HTML fragments. All markup below is our own
# reviewed, static editorial text, never taken from arbitrary source files.
BODY = [
    ("heading", "<h2>Built by connecting diagnostic layers</h2>"),
    (
        "paragraph",
        "<p><strong>Native underneath, modern at the surface.</strong> "
        'LotoT builds on the GPL-3.0 <a href="https://github.com/fr3ts0n/AndrOBD">AndrOBD</a> '
        "engine rather than replacing its OBD protocol handling. A Java-to-JavaScript bridge "
        "supplies data to the React/Vite cockpit, retaining advanced native tools for "
        "inspection when a compatible adapter is available.</p>",
    ),
    (
        "paragraph",
        "<p><strong>Two different categories of evidence.</strong> "
        "Bluetooth/USB/Wi-Fi ELM327 sessions can yield ECU measurements and trouble-code "
        "reports. The phone supplies its own GPS and accelerometer context. The UI and "
        "assistant distinguish these signals: an unconnected phone cannot establish "
        "engine, suspension or transmission health.</p>",
    ),
    ("heading", "<h2>The latest engineering milestones</h2>"),
    (
        "paragraph",
        "<p><strong>14 August — AI fallback routing.</strong> "
        '<a href="https://github.com/lotfinity/lotot-android/commit/b4911b26fe6e3518831595dab759746178dd4cdb">'
        "Commit b4911b2</a> adds a LiteLLM fallback chain to the LoToTi prototype. "
        "Configured providers can be tried in order, including Codex-oriented and "
        "StepFun-oriented LiteLLM routes and other supported endpoints. "
        "External model availability depends on separately configured services.</p>",
    ),
    (
        "paragraph",
        "<p><strong>12 August — LoToTi &amp; onboarding.</strong> "
        '<a href="https://github.com/lotfinity/lotot-android/commit/eb7c186df969547e39ad3110f5c43c4ca0f22ae2">'
        "Commit eb7c186</a> introduces an AI diagnostic conversation, a bundled "
        "DTC-description database, and a more polished onboarding experience. "
        "Descriptions explain possible meanings of codes; they do not assert that "
        "any particular fault occurred on a connected vehicle.</p>",
    ),
    (
        "paragraph",
        "<p><strong>31 July — reliable telemetry.</strong> "
        '<a href="https://github.com/lotfinity/lotot-android/commit/7681d1c19904fceb9d23107ff6a34a4b442af1fd">'
        "Commit 7681d1c</a> brings the MQTT publishing stack into a foreground "
        "gateway with queued snapshots and secure credential storage. "
        "Earlier changes route data by the Django platform's device UID and "
        "combine built-in GPS and motion data with labeled OBD readings.</p>",
    ),
    (
        "paragraph",
        "<p><strong>28 July — diagnostic cockpit.</strong> "
        '<a href="https://github.com/lotfinity/lotot-android/commit/d8e42ed9eae9c262bcf8830cdfdc3dafd48ac990">'
        "Commit d8e42ed</a> adds the full live-OBD dashboard; the development "
        "series also improves speedometer responsiveness and Bluetooth connection "
        "state handling. Later UI work adds light/dark themes, language resources "
        "and a standalone LotoT identity.</p>",
    ),
    ("heading", "<h2>Intelligence without invented diagnoses</h2>"),
    (
        "paragraph",
        "<p><strong>Observed → interpreted → next check.</strong> "
        "The LoToTi system prompt calls out session state, source labels and "
        "missing measurements before interpreting them. It must not treat a "
        "missing trouble-code report as a clean scan, or demo readings as live "
        "vehicle evidence. When observations are insufficient, it asks for "
        "the relevant ECU connection or scan.</p>",
    ),
    (
        "paragraph",
        "<p><strong>Project scope.</strong> The public repo shows "
        "working source-level integration for an Android/React cockpit, native "
        "OBD workflows, MQTT and an AI-provider prototype. "
        "It does not establish production readiness, cloud-service uptime, "
        "vehicle compatibility or diagnostic accuracy. The device mockups on "
        "this page were captured from an installed Android app with no OBD adapter "
        "connected.</p>",
    ),
    ("heading", "<h2>Open-source foundations &amp; what comes next</h2>"),
    (
        "paragraph",
        "<p>The project retains <strong>AndrOBD attribution and GPL-3.0 "
        "licensing</strong>. Source, integration notes and build instructions are available "
        'in the <a href="https://github.com/lotfinity/lotot-android">LotoT Android repository</a>. '
        "The companion Django vehicle-health platform is maintained separately. "
        "Future verification should focus on repeatable on-vehicle sessions, "
        "secure AI credential distribution and end-to-end MQTT delivery.</p>",
    ),
]


def main():
    project = AppPage.objects.get(slug="lotot")
    if not project.source_url.startswith(REPO):
        raise RuntimeError("Unexpected source URL: refusing to modify project")
    body = project.body.raw_data
    if body and not any(
        "Built by connecting diagnostic layers" in str(part) for part in body
    ):
        raise RuntimeError(
            "Project body has independent editorial content; refusing to overwrite it"
        )
    if body and project.title == "LotoT — Diagnostics & AI Copilot":
        print("Already enriched; preserving existing Wagtail edits")
        return

    original_media = [
        getattr(project, field + "_id")
        for field in (
            "banner_image",
            "device_mobile_image",
            "device_mobile_secondary_image",
            "mockup_design",
        )
    ]
    if not all(original_media):
        raise RuntimeError("Existing captured LotoT media incomplete; aborting")

    project.title = "LotoT — Diagnostics & AI Copilot"
    project.description = DESCRIPTION
    project.focus_area = "Android / Telematics / AI"
    project.key_features = "\n".join(FEATURES)
    project.body = BODY
    for name in ("Java", "Vite", "WebView", "LiteLLM", "OBD-II / ELM327"):
        item, _created = TechStack.objects.get_or_create(name=name)
        project.tech_stack.add(item)
    project.save_revision().publish()
    assert original_media == [
        getattr(project, field + "_id")
        for field in (
            "banner_image",
            "device_mobile_image",
            "device_mobile_secondary_image",
            "mockup_design",
        )
    ]
    print(
        "Published",
        project.title,
        "page ID",
        project.pk,
        "with",
        len(FEATURES),
        "feature lines and",
        len(BODY),
        "story blocks",
    )
    print("Latest source commit:", SOURCE_COMMIT)


if __name__ == "__main__":
    main()
