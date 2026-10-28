"""Import the four historical homepage projects into Wagtail exactly once.

Safe to re-run: existing project pages, images, and technology snippets are
reused without overwriting editor-owned content. This is not an auto-migration:
run it explicitly after migrating and on a database where seed content is wanted.
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

from website.models import AppPage
from website.models import AppsIndexPage
from website.models import TechStack


TECHNOLOGIES = {
    "Django": ("Python web framework", "django.webp"),
    "Wagtail": ("CMS built on Django", "wagtail.webp"),
    "PostgreSQL": ("Relational database", "postgresql.webp"),
    "OpenAI": ("AI solutions", "openai.webp"),
    "React": ("Frontend library", "react.webp"),
    "Azure Translator": ("Real-time translation services", "azure.webp"),
}

PROJECTS = (
    {
        "title": "DentiDelil International",
        "image": "denti.webp",
        "url": "https://dentidelil-international.com",
        "description": "A state-of-the-art multilingual CMS-powered website designed to cater to international dental services.",
        "features": [
            "Multilingual Support: Supports 13+ languages.",
            "AI-Powered Enhancements: Integrated OpenAI GPT-4o model and Azure Translator.",
            "Dynamic API Integrations: JotForm, Unsplash, and more.",
        ],
        "stack": ("Django", "Wagtail", "PostgreSQL", "OpenAI"),
    },
    {
        "title": "DentiDelil App",
        "image": "app1.webp",
        "url": "https://app.dentidelil-international.com",
        "description": "A modern, all-in-one dashboard for beauty salon management.",
        "features": [
            "Appointment Scheduling: Interactive calendar with reminders.",
            "Client Management: Profiles and treatment histories.",
            "Real-Time Analytics: Revenue, top services, and productivity tracking.",
        ],
        "stack": ("Django", "React", "PostgreSQL"),
    },
    {
        "title": "Dental Management App",
        "image": "app2.webp",
        "url": "https://app.dentidelil-international.com",
        "description": "A comprehensive dental management solution.",
        "features": [
            "Patient Scheduling: Simplify appointment management for clinics.",
            "Records Management: Secure and accessible patient records.",
            "Financial Tracking: Monitor invoices, payments, and insurance claims.",
            "Multilingual Support: Enable communication with patients from diverse backgrounds.",
        ],
        "stack": ("Django", "Wagtail", "Azure Translator"),
    },
    {
        "title": "Salon Nassnor",
        "image": "snn.webp",
        "url": "https://salonnassnor.com",
        "description": "The pro version of Salon Nassnor, offering enhanced tools for beauty professionals.",
        "features": [
            "Advanced Appointment System: Customizable bookings and reminders.",
            "Inventory Management: Track beauty product availability.",
            "Customer Relationship Management: Tools to engage and retain clients.",
            "Reporting Tools: Visualize revenue and staff productivity.",
        ],
        "stack": ("Django", "Wagtail", "Azure Translator"),
    },
)


class Command(BaseCommand):
    help = "Seed historical portfolio cards as editable Wagtail AppPage records."

    def add_arguments(self, parser):
        parser.add_argument("--site", default=None, help="Existing Wagtail site hostname")

    @staticmethod
    def import_image(name, filename):
        image_model = get_image_model()
        title = f"Portfolio - {name}"
        old = image_model.objects.filter(title=title).first()
        if old:
            return old
        path = Path(settings.BASE_DIR) / "website" / "static" / "img" / filename
        if not path.is_file():
            raise CommandError(f"Missing seed image: {path}")
        with path.open("rb") as stream:
            return image_model.objects.create(title=title, file=File(stream, name=filename))

    @transaction.atomic
    def handle(self, *args, **options):
        if options["site"]:
            site = Site.objects.get(hostname=options["site"])
        else:
            site = Site.objects.get(is_default_site=True)
        root = site.root_page
        index = AppsIndexPage.objects.child_of(root).filter(slug="projects").first()
        if not index:
            index = root.add_child(
                instance=AppsIndexPage(
                    title="Projects", slug="projects",
                    introduction="Selected projects and applications",
                    locale=root.locale,
                )
            )
            index.save_revision().publish()
            self.stdout.write(self.style.SUCCESS(f"Created project index #{index.pk}"))

        stacks = {}
        for name, (description, icon) in TECHNOLOGIES.items():
            tech, created = TechStack.objects.get_or_create(
                name=name, defaults={"description": description}
            )
            if created and not tech.logo:
                tech.logo = self.import_image(name, icon)
                tech.save(update_fields=["logo"])
            stacks[name] = tech

        added = 0
        for order, data in enumerate(PROJECTS, 1):
            slug = slugify(data["title"])
            project = AppPage.objects.child_of(index).filter(slug=slug).first()
            if project:
                self.stdout.write(f"Existing {project.title} (#{project.pk}): untouched")
                continue
            image = self.import_image(data["title"], data["image"])
            project = index.add_child(
                instance=AppPage(
                    title=data["title"], slug=slug,
                    description=data["description"],
                    external_url=data["url"],
                    key_features="\n".join(data["features"]),
                    mockup_design=image, show_on_homepage=True,
                    display_order=order * 10,
                    locale=index.locale,
                )
            )
            project.tech_stack.set([stacks[name] for name in data["stack"]])
            project.save_revision().publish()
            added += 1
            self.stdout.write(self.style.SUCCESS(f"Created {project.title} (#{project.pk})"))
        self.stdout.write(self.style.SUCCESS(f"Added {added}; total project pages: {AppPage.objects.count()}"))
