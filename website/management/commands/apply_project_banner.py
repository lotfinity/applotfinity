"""Attach an approved banner to a project without overwriting real UI captures."""
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.db import transaction
from wagtail.images import get_image_model

from website.models import AppPage


class Command(BaseCommand):
    help = 'Import a reviewed project banner into Wagtail and link it to one case study.'

    def add_arguments(self, parser):
        parser.add_argument('--slug', required=True, help='Existing AppPage slug')
        parser.add_argument('--file', required=True, help='Local WebP/PNG/JPEG artwork path')
        parser.add_argument('--title', help='Title for the Wagtail image record')
        parser.add_argument('--replace', action='store_true', help='Replace existing approved banner')
        parser.add_argument('--desktop-from-mockup', action='store_true',
                            help='Reuse the genuine screenshot for the CSS laptop showcase')

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            project = AppPage.objects.get(slug=options['slug'])
        except (AppPage.DoesNotExist, AppPage.MultipleObjectsReturned) as e:
            raise CommandError(f'No unique project with slug {options["slug"]}') from e
        file_path = Path(options['file']).expanduser().resolve()
        if not file_path.is_file() or file_path.suffix.lower() not in {'.webp', '.png', '.jpg', '.jpeg'}:
            raise CommandError('Provide an existing WebP/PNG/JPEG artwork file')
        if project.banner_image_id and not options['replace']:
            self.stdout.write(f'{project.title}: current banner kept ({project.banner_image_id}).')
            return
        title = options.get('title') or f'Editorial banner / {project.title} / {file_path.stem}'
        image_model = get_image_model()
        artwork = image_model.objects.filter(title=title).first()
        if artwork is None:
            with file_path.open('rb') as source:
                artwork = image_model.objects.create(
                    title=title, file=File(source, name=file_path.name)
                )
        project.banner_image = artwork
        if options['desktop_from_mockup'] and not project.device_desktop_image_id:
            if not project.mockup_design_id:
                self.stdout.write('No real screenshot available; skipped desktop mockup.')
            else:
                project.device_desktop_image = project.mockup_design
        revision = project.save_revision()
        if project.live:
            revision.publish()
        self.stdout.write(self.style.SUCCESS(
            f'{project.title}: banner={artwork.pk} ({artwork.file.name}); '
            f'desktop screenshot={project.device_desktop_image_id or "none"}'
        ))
