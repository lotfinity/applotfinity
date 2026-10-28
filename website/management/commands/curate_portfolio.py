"""One-time, evidence-based Lotfinity content refresh from public project repos.

Source: the owner's October 2026 portfolio review, cross-checked against
public GitHub README/repository metadata. Nothing is claimed production-ready
without evidence. Private Synaptic repositories are deliberately omitted.

Explicit execution: `manage.py curate_portfolio --apply` after DB/media backup.
Preserves projects and editor changes on subsequent runs.
"""
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.db import transaction
from django.utils.text import slugify
from wagtail.images import get_image_model
from wagtail.models import Site

from website.homepage_settings import HomepageService
from website.homepage_settings import HomepageSettings
from website.homepage_settings import HomepageSkill
from website.models import AppPage
from website.models import AppsIndexPage
from website.models import TechStack


LEGACY_TITLE = "Lotfinity | Creative Web Studio"

HOMEPAGE_COPY = {
    "site_title": "Lotfinity — Connected Systems & Digital Product Engineering",
    "seo_description": (
        "Real-world software and systems engineering: Django platforms, Android integration, "
        "AI workflows, IoT, 3D electronics, geospatial tools and cross-platform prototypes."
    ),
    "byline_verb": "Connecting",
    "byline_description": "Ideas, Devices & Systems",
    "hero_prefix": "Connect",
    "hero_emphasis": "The",
    "hero_suffix": "Unconnected.",
    "web_marker": "Systems & Product Engineering",
    "web_kicker": "Software, hardware, AI — one connected problem space.",
    "web_heading": "The interesting work starts where existing systems stop.",
    "web_intro_before": (
        "I work at the boundaries between software, hardware and automation. When an "
        "application, device or workflow reaches a limit, I investigate the protocols, "
        "interfaces and underlying data rather than accepting that limit as final. At "
    ),
    "web_intro_after": (
        ", I build the missing bridges: practical applications, Android companions, "
        "market-intelligence pipelines, diagnostic dashboards and experiments with "
        "physical devices. The work ranges from built software to research prototypes — "
        "and each project is presented with its actual scope and limitations."
    ),
    "projects_heading": "Selected Builds",
    "projects_subheading": "Real repositories. Working ideas. Honest stages of development.",
    "web_secondary_kicker": "A philosophy of connection, not reinvention.",
    "web_secondary_heading": "When systems do not connect, build the bridge.",
    "web_secondary_lead_before": "The projects behind ",
    "web_secondary_lead_after": (
        " follow a common pattern: understand an existing system, reuse what already "
        "works and change what is missing. A phone can become a sensor node. An open-source "
        "OBD engine can power a new automotive interface. Raw listings can become useful "
        "market intelligence — but only after the evidence and product identities are checked."
    ),
    "web_automation": (
        "I usually begin with one concrete limitation. I test the smallest useful solution, "
        "then turn it into reusable components, clearer interfaces or a platform where that "
        "actually helps. The goal is not to call every experiment a product; it is to "
        "show what was built, what was verified and what still needs work."
    ),
    "contact_label": "Discuss a project",
    "github_url": "https://github.com/lotfinity",
    "studio_title": "Studio",
    "studio_subtitle": "Curiosity, integration & engineering",
    "studio_bio": "LOTFI KANOUNI — Systems-Oriented Product Builder",
    "hosted_services_label": "Explore the source on GitHub",
    "hosted_services_url": "https://github.com/lotfinity",
    "studio_manifesto": (
        "Inspect the internals. Keep what works. Connect what does not. "
        "Test on real devices. Be explicit about the limits."
    ),
    "expertise_title": "Areas I build in:",
    "expertise_description": (
        "Django and business systems · Python and data pipelines · Android and Linux · "
        "React interfaces · MCP and AI-agent tooling · ESP32, WLED and sensors · "
        "Telemetry, mapping and commercial intelligence."
    ),
}

SERVICES = (
    "Start from a real constraint — not a buzzword",
    "Investigate how existing APIs, devices and protocols actually work",
    "Reuse proven engines and libraries where they make sense",
    "Build a working bridge between otherwise separate components",
    "Keep raw evidence separate from verified facts",
    "Design controls and interfaces for people, not just developers",
    "Test on real devices, with rollback and repeatable setup",
    "Document what works, what is experimental and what comes next",
)

# Indicators preserve the original visual ring concept; they are editorial,
# illustrative focus weights rather than standardized proficiency scores.
SKILLS = (
    ("Django", "Business platforms & CMS", 90, "django.webp"),
    ("Python", "Backend logic & integration", 90, "python.webp"),
    ("Android", "Device tools & native bridges", 83, None),
    ("React", "Interactive cross-platform UI", 84, "react.webp"),
    ("Linux", "Systems & remote access", 85, None),
    ("ESP32 / WLED", "Physical computing & light", 78, None),
    ("AI & MCP", "Agents, APIs & orchestration", 86, "openai.webp"),
    ("Data Systems", "Telemetry, maps & provenance", 82, "postgresql.webp"),
)

# Only public repositories. This is not a list of proven production deployments.
PROJECTS = (
    {
        "title": "Ohmlet — 3D Circuit Workbench",
        "category": "Hardware Simulation",
        "stage": "active",
        "repo": "https://github.com/lotfinity/ohmlet",
        "demo": "https://byd.whatsynaptic.com/",
        "description": (
            "A browser-based 3D breadboard workbench combining visual circuit assembly "
            "with analog and digital simulation. Hardware experimentation, without needing "
            "every component on the desk."
        ),
        "features": (
            "Three.js breadboards, wiring, instruments and live component previews",
            "Hybrid analog solver and behavioral digital IC models",
            "AI-assisted circuit creation with simulator-based validation",
        ),
        "tech": ("React", "TypeScript", "Three.js", "Electronics Simulation"),
        "image": "ohmlet-portfolio.webp",
    },
    {
        "title": "PriceBridge — Market Intelligence",
        "category": "Data & Commerce",
        "stage": "prototype",
        "repo": "https://github.com/lotfinity/pricebridge-clean",
        "description": (
            "A Django-based system for comparing mobile-phone listings across markets, "
            "designed around a strict boundary between collected evidence and trusted product matches."
        ),
        "features": (
            "Canonical model and storage-variant matching — no automatic catalog pollution",
            "Raw listing preservation, structured extraction and review states",
            "Evidence-gated opportunity comparisons using stored exchange-rate data",
        ),
        "tech": ("Django", "Python", "Data Pipelines"),
    },
    {
        "title": "LotoT — Android Vehicle Diagnostics",
        "category": "Android & Telematics",
        "stage": "active",
        "repo": "https://github.com/lotfinity/lotot-android",
        "description": (
            "An Android vehicle-health companion built around AndrOBD's existing diagnostic "
            "engine, with a custom React cockpit and connections to live phone and vehicle data."
        ),
        "features": (
            "OBD-II / ELM327 diagnostics using the AndrOBD open-source engine",
            "Custom React/WebView cockpit with GPS and phone sensor context",
            "JavaScript/native bridging and MQTT telemetry publishing",
        ),
        "tech": ("Android", "React", "MQTT"),
    },
    {
        "title": "Neon Strip Studio",
        "category": "IoT & Visual Tools",
        "stage": "test_release",
        "repo": "https://github.com/lotfinity/neon-strip-studio",
        "description": (
            "A visual editor and screensaver player for a continuous WLED neon-strip design, "
            "with shared JSON designs across Windows, GNOME Linux and Android."
        ),
        "features": (
            "Editable LED layout and colors with real-time previews",
            "Cross-platform playback and transferable design/recording data",
            "Personal test release; physical WLED and some target devices not yet verified",
        ),
        "tech": ("JavaScript", "WLED", "Android"),
    },
    {
        "title": "IstanbulPropTech",
        "category": "Property & Maps",
        "stage": "prototype",
        "repo": "https://github.com/lotfinity/IstanbulPropTech",
        "description": (
            "Geospatial property exploration tools that turn map layers, neighborhood context "
            "and listing data into information that can be searched and compared."
        ),
        "features": (
            "Interactive map layers and property/area exploration",
            "Hierarchical geographic and listing filters",
            "Caching and location-based service context",
        ),
        "tech": ("Python", "Maps & GIS", "Data Pipelines"),
    },
    {
        "title": "Beyond Website — Business Workflows",
        "category": "Healthcare & Operations",
        "stage": "case_study",
        "repo": "https://github.com/lotfinity/beyond-website-v5",
        "description": (
            "An exploration of more complete Django-powered business workflows: "
            "public-facing interfaces, staff administration, dashboards and service integrations."
        ),
        "features": (
            "Business UI alongside administrative and staff workflows",
            "Django-based authentication and application structure",
            "Webhook and external-system integration patterns",
        ),
        "tech": ("Django", "Python", "Business Systems"),
    },
)


class Command(BaseCommand):
    help = "Curate the portfolio with real public work, and update the homepage philosophy."

    def add_arguments(self, parser):
        parser.add_argument("--apply", action="store_true", help="Apply the one-time content update")

    @transaction.atomic
    def handle(self, *args, **options):
        if not options["apply"]:
            self.stdout.write("Dry-run: homepage philosophy, 8 services, 8 focus areas, 6 public projects; no changes.")
            return
        site = Site.objects.get(is_default_site=True)
        home = HomepageSettings.for_site(site)
        first_curation = home.site_title == LEGACY_TITLE
        if not first_curation:
            self.stdout.write(self.style.WARNING(
                "Homepage already customized — preserving all settings and ordered child content."
            ))
        else:
            for field, text in HOMEPAGE_COPY.items():
                setattr(home, field, text)
            home.save()
            home.services.all().delete()
            home.skills.all().delete()
            for index, service in enumerate(SERVICES):
                HomepageService.objects.create(homepage=home, sort_order=index, text=service)
            for index, (name, detail, weight, image_name) in enumerate(SKILLS):
                icon = None
                if image_name:
                    title = f"Lotfinity focus - {name}"
                    icon = get_image_model().objects.filter(title=title).first()
                    if icon is None:
                        path = Path(settings.BASE_DIR) / "website" / "static" / "img" / image_name
                        if path.exists():
                            with path.open("rb") as f:
                                icon = get_image_model().objects.create(
                                    title=title, file=File(f, name=f"focus-{image_name}")
                                )
                HomepageSkill.objects.create(
                    homepage=home, sort_order=index, name=name,
                    description=detail, percentage=weight, icon=icon,
                )
            self.stdout.write(self.style.SUCCESS("Updated homepage narrative and focus areas"))
        root = site.root_page
        index = AppsIndexPage.objects.child_of(root).filter(slug="projects").first()
        if index is None:
            raise CommandError("Projects index is missing; run seed_portfolio first")
        if index.introduction == "Selected projects and applications":
            index.introduction = (
                "A curated selection of public engineering work. Prototypes, test releases and "
                "case studies are labeled honestly; source repositories are linked where available."
            )
            index.save_revision().publish()
        if first_curation:
            for old in AppPage.objects.child_of(index).filter(source_url=""):
                if (
                    old.slug in {
                        "dentidelil-international", "dentidelil-app",
                        "dental-management-app", "salon-nassnor",
                    }
                    and old.show_on_homepage
                ):
                    old.show_on_homepage = False
                    old.save_revision().publish()
        added = 0
        for order, data in enumerate(PROJECTS, 1):
            slug = slugify(data["title"].split(" — ")[0])
            if AppPage.objects.child_of(index).filter(slug=slug).exists():
                self.stdout.write(f"Preserved existing {slug}")
                continue
            icon = None
            if data.get("image"):
                title = "Portfolio - " + data["title"]
                icon = get_image_model().objects.filter(title=title).first()
                if icon is None:
                    path = Path(settings.BASE_DIR) / "website" / "static" / "img" / data["image"]
                    if not path.exists():
                        raise CommandError(f"Missing approved public screenshot {path}")
                    with path.open("rb") as f:
                        icon = get_image_model().objects.create(
                            title=title, file=File(f, name=data["image"]),
                        )
            project = index.add_child(instance=AppPage(
                title=data["title"], slug=slug, locale=index.locale,
                description=data["description"],
                source_url=data["repo"], external_url=data.get("demo", ""),
                project_stage=data["stage"], focus_area=data["category"],
                key_features="\n".join(data["features"]),
                display_order=order * 10, mockup_design=icon,
                show_on_homepage=True,
            ))
            snippets = []
            for name in data["tech"]:
                tech, _ = TechStack.objects.get_or_create(name=name)
                snippets.append(tech)
            project.tech_stack.set(snippets)
            project.save_revision().publish()
            added += 1
            self.stdout.write(self.style.SUCCESS(f"Published {project.title}"))
        self.stdout.write(self.style.SUCCESS(f"Added {added} projects; featured {AppPage.objects.filter(show_on_homepage=True).count()}."))
