"""The numbered project banners never replace authentic UI screenshots."""
from io import BytesIO

from django.core.files.base import ContentFile
from django.test import TestCase
from PIL import Image
from wagtail.images import get_image_model
from wagtail.models import Site

from website.models import AppPage
from website.models import AppsIndexPage


class ProjectBannerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        root = Site.objects.get(is_default_site=True).root_page
        cls.index = root.add_child(instance=AppsIndexPage(title='Projects', slug='projects'))
        cls.index.save_revision().publish()
        cls.app = cls.index.add_child(instance=AppPage(
            title='Circuit Builder', slug='circuit-builder',
            description='Real circuit assembly workspace',
            show_on_homepage=True, display_order=10,
        ))
        cls.app.save_revision().publish()

    def new_image(self, name, color):
        data = BytesIO()
        Image.new('RGB', (720, 450), color).save(data, format='PNG')
        return get_image_model().objects.create(
            title=name, file=ContentFile(data.getvalue(), name=name + '.png'),
        )

    def test_banner_used_in_index_and_homepage_but_not_as_mockup(self):
        screenshot = self.new_image('Original interface', '#c0dfeb')
        banner = self.new_image('Editorial cover', '#11234b')
        self.app.mockup_design = screenshot
        self.app.banner_image = banner
        self.app.save_revision().publish()
        index = self.client.get('/en/projects/')
        self.assertEqual(index.status_code, 200)
        self.assertContains(index, 'Designed banner for Circuit Builder')
        self.assertContains(index, '01 <span>/ 01</span>')
        home = self.client.get('/en/')
        self.assertContains(home, 'Circuit Builder')
        self.assertIn('Editorial', banner.title)
        detail = self.client.get('/en/projects/circuit-builder/')
        self.assertContains(detail, 'Project visual')
        self.assertContains(detail, 'Circuit Builder project visual')
        self.assertNotContains(detail, 'Designed banner for Circuit Builder')
        self.app.refresh_from_db()
        self.assertEqual(self.app.mockup_design_id, screenshot.pk)
        self.assertEqual(self.app.banner_image_id, banner.pk)

    def test_banner_import_is_idempotent_and_preserves_ui_source(self):
        from pathlib import Path
        from tempfile import TemporaryDirectory

        from django.core.management import call_command

        screenshot = self.new_image('True application screen', '#7799aa')
        self.app.mockup_design = screenshot
        self.app.save_revision().publish()
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / 'artwork.png'
            Image.new('RGB', (800, 450), '#0f2a4a').save(path, 'PNG')
            call_command('apply_project_banner', slug=self.app.slug,
                         file=str(path), desktop_from_mockup=True, verbosity=0)
            self.app.refresh_from_db()
            first_banner = self.app.banner_image_id
            self.assertTrue(first_banner)
            self.assertEqual(self.app.device_desktop_image_id, screenshot.pk)
            self.assertEqual(self.app.mockup_design_id, screenshot.pk)
            call_command('apply_project_banner', slug=self.app.slug,
                         file=str(path), verbosity=0)
            self.app.refresh_from_db()
            self.assertEqual(self.app.banner_image_id, first_banner)

    def test_featured_numbering_excludes_archived_pages(self):
        archive = self.index.add_child(instance=AppPage(
            title='Archived entry', slug='archived-entry',
            display_order=0, show_on_homepage=False,
        ))
        archive.save_revision().publish()
        second = self.index.add_child(instance=AppPage(
            title='Second featured', slug='second-featured',
            display_order=20, show_on_homepage=True,
        ))
        second.save_revision().publish()
        response = self.client.get('/en/projects/')
        self.assertContains(response, '01 <span>/ 02</span>')
        self.assertContains(response, '02 <span>/ 02</span>')
        self.assertContains(response, 'Archived entry')
