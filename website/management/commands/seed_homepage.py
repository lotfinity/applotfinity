"""Populate a new site homepage's editable services and skills once.

Does not replace existing content or delete already-edited records.
"""
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction
from wagtail.images import get_image_model
from wagtail.models import Site

from website.homepage_settings import HomepageService
from website.homepage_settings import HomepageSettings
from website.homepage_settings import HomepageSkill


SERVICES = (
    "In-Depth Research & Insightful Strategy",
    "Tailored Digital Concepts & Strategic Vision",
    "User-Centric UI & UX Design",
    "Content Management",
    "Frontend Development",
    "Animations & Interactions",
    "Admin System & Backend",
    "Support & Maintaining",
)

SKILLS = (
    ("Django", "Python web framework", 90, "django.webp"),
    ("Wagtail", "CMS built on Django", 85, "wagtail.webp"),
    ("PostgreSQL", "Relational database", 80, "postgresql.webp"),
    ("OpenAI", "AI solutions", 75, "openai.webp"),
    ("HTML/CSS", "Front-end design", 90, "htmlcss.webp"),
    ("JavaScript", "Interactive features", 80, "js.webp"),
    ("GSAP", "Animation library", 70, "gsap.webp"),
    ("Python", "Core programming language", 95, "python.webp"),
)


class Command(BaseCommand):
    help = "Seed original homepage services and skills as editable Wagtail settings."

    @transaction.atomic
    def handle(self, *args, **options):
        site = Site.objects.get(is_default_site=True)
        homepage = HomepageSettings.for_site(site)
        if not homepage.services.exists():
            for i, label in enumerate(SERVICES):
                HomepageService.objects.create(homepage=homepage, sort_order=i, text=label)
            self.stdout.write(self.style.SUCCESS("Seeded 8 editable services"))
        else:
            self.stdout.write("Existing services: untouched")

        if not homepage.skills.exists():
            image_model = get_image_model()
            for i, (name, description, percentage, filename) in enumerate(SKILLS):
                title = f"Homepage skill - {name}"
                icon = image_model.objects.filter(title=title).first()
                if icon is None:
                    path = Path(settings.BASE_DIR) / "website" / "static" / "img" / filename
                    if path.is_file():
                        with path.open("rb") as handle:
                            icon = image_model.objects.create(
                                title=title, file=File(handle, name=filename)
                            )
                HomepageSkill.objects.create(
                    homepage=homepage, sort_order=i, name=name,
                    description=description, percentage=percentage, icon=icon,
                )
            self.stdout.write(self.style.SUCCESS("Seeded 8 editable skills"))
        else:
            self.stdout.write("Existing skills: untouched")
        self.stdout.write(self.style.SUCCESS(
            f"Homepage: {homepage.pk}; services={homepage.services.count()}; "
            f"skills={homepage.skills.count()}"
        ))
