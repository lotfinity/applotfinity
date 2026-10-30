"""Project-specific, source-verified LotoT story stays isolated and editable."""
from pathlib import Path

from django.conf import settings
from django.test import TestCase
from wagtail.models import Site

from website.models import AppPage
from website.models import AppsIndexPage


class LotoTStoryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        site = Site.objects.get(is_default_site=True)
        index = site.root_page.add_child(instance=AppsIndexPage(title='Projects', slug='projects'))
        index.save_revision().publish()
        cls.lotot = index.add_child(instance=AppPage(
            title='LotoT — Diagnostics & AI Copilot', slug='lotot',
            description='Evidence-first diagnostic assistant',
            source_url='https://github.com/lotfinity/lotot-android',
            key_features='Native diagnostic engine\nMQTT gateway\nAI copilot',
            body=[
                ('heading', '<h2>Source-verified deep dive</h2>'),
                ('paragraph', '<p>GPS data is separate from ECU signals.</p>'),
            ],
        ))
        cls.lotot.save_revision().publish()
        normal = index.add_child(instance=AppPage(title='Other project', slug='other', description='Other record'))
        normal.save_revision().publish()

    def test_story_renders_verified_source_commits_and_architecture(self):
        response = self.client.get('/en/projects/lotot/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'project-detail--lotot')
        self.assertContains(response, 'class="lotot-story__spotlight"', count=4)
        self.assertContains(response, 'lotot-story__flow')
        self.assertContains(response, 'lotot-story__milestones')
        self.assertContains(response, 'b4911b26fe6e3518831595dab759746178dd4cdb')
        self.assertContains(response, '2026-08-14')
        self.assertContains(response, 'external AI-provider availability')
        self.assertContains(response, 'Source-verified deep dive')
        self.assertContains(response, 'GPS data is separate from ECU signals')
        self.assertContains(response, 'Explore public source')

    def test_other_pages_unaffected(self):
        response = self.client.get('/en/projects/other/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'class="lotot-story"')
        self.assertNotContains(response, 'project-detail--lotot')
        index_response = self.client.get('/en/projects/')
        self.assertNotContains(index_response, 'lotot-story__flow')

    def test_mobile_and_reduced_motion_styles_exist_without_new_renderer(self):
        css = (Path(settings.BASE_DIR) / 'website/static/css/project-pages.css').read_text()
        self.assertIn('.project-detail--lotot .lotot-story', css)
        self.assertIn('.lotot-story__flow', css)
        self.assertIn('@media(max-width:700px)', css)
        self.assertIn('@media(prefers-reduced-motion:reduce)', css)
        template = (Path(settings.BASE_DIR) / 'website/templates/website/partials/lotot_engineering.html').read_text()
        self.assertNotIn('<script', template)
        self.assertNotIn('<canvas', template)
        self.assertIn('https://github.com/lotfinity/lotot-android/commit/b4911b', template)
