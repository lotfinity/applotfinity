"""Keep the React Bits-inspired gallery treatment isolated and power-conscious."""
from pathlib import Path

from django.conf import settings
from django.test import TestCase
from wagtail.models import Site

from website.models import AppPage
from website.models import AppsIndexPage


class GalleryLetterGlitchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        site = Site.objects.get(is_default_site=True)
        index = site.root_page.add_child(
            instance=AppsIndexPage(title='Projects', slug='projects')
        )
        index.save_revision().publish()
        project = index.add_child(
            instance=AppPage(title='Visual check', slug='visual-check',
                             description='A genuine engineering project')
        )
        project.save_revision().publish()

    def test_only_numbered_gallery_has_letter_glitch(self):
        response = self.client.get('/en/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="gallery-page"')
        self.assertContains(response, 'data-letter-glitch aria-hidden="true"')
        self.assertContains(response, 'gallery-letter-glitch.js')
        self.assertContains(response, 'Visual check')
        detail = self.client.get('/en/projects/visual-check/')
        self.assertEqual(detail.status_code, 200)
        self.assertNotContains(detail, 'data-letter-glitch')
        self.assertNotContains(detail, 'gallery-letter-glitch.js')
        self.assertContains(detail, 'data-project-network')
        home = self.client.get('/en/')
        self.assertNotContains(home, 'gallery-letter-glitch.js')

    def test_canvas_2d_effect_has_frame_and_accessibility_budgets(self):
        source = (Path(settings.BASE_DIR) / 'website/static/js/gallery-letter-glitch.js').read_text()
        self.assertIn("getContext('2d'", source)
        self.assertNotIn('requestAnimationFrame(', source)
        self.assertNotIn('WebGLRenderer', source)
        self.assertIn('mobile ? 6 : 10', source)
        self.assertIn('mobile ? 15 : 24', source)
        self.assertIn('maxPixels', source)
        self.assertIn('document.hidden', source)
        self.assertIn('prefers-reduced-motion: reduce', source)
        self.assertIn('navigator.connection?.saveData', source)
        self.assertIn('pointermove', source)
        self.assertIn('pointerdown', source)

    def test_canvas_background_not_interactive(self):
        css = (Path(settings.BASE_DIR) / 'website/static/css/project-pages.css').read_text()
        self.assertIn('.gallery-letter-glitch {', css)
        self.assertIn('pointer-events: none;', css)
        self.assertIn('.gallery-page > .page-wrap', css)

    def test_gallery_editor_can_set_custom_phrases_without_script_injection(self):
        import json
        import re

        index = AppsIndexPage.objects.get(slug='projects')
        editor_value = 'RESEARCH / BUILD\nCONNECT EVERY LAYER\n</script><script>alert(1)</script>'
        index.glitch_messages = editor_value
        index.save_revision().publish()
        response = self.client.get('/en/projects/')
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        match = re.search(
            r'<script id="gallery-glitch-messages" type="application/json">(.*?)</script>',
            html,
        )
        self.assertIsNotNone(match)
        self.assertEqual(json.loads(match.group(1)), editor_value)
        self.assertNotIn('</script><script>alert(1)', html)
        self.assertIn(r'\u003C/script\u003E', match.group(1))

    def test_wagtail_editor_has_message_field(self):
        self.assertIn('glitch_messages', [
            getattr(panel, 'field_name', None)
            for panel in AppsIndexPage.content_panels
        ])
