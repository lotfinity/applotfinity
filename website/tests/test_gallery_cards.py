"""Numbered portfolio cards animate independently without adding GPU runtimes."""
from pathlib import Path

from django.conf import settings
from django.test import TestCase
from wagtail.models import Site

from website.models import AppPage
from website.models import AppsIndexPage


class GalleryCardsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        root = Site.objects.get(is_default_site=True).root_page
        index = root.add_child(instance=AppsIndexPage(title='Projects', slug='projects'))
        index.save_revision().publish()
        for n in range(6):
            entry = index.add_child(instance=AppPage(
                title=f'System {n+1}', slug=f'system-{n+1}',
                description=f'Verifiable engineering work {n+1}',
                display_order=n, show_on_homepage=True,
            ))
            entry.save_revision().publish()

    def test_exactly_six_numbered_cards_have_scoped_animation_hooks(self):
        response = self.client.get('/en/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.count(b'data-project-card'), 6)
        self.assertEqual(response.content.count(b'case-tile__signal'), 6)
        self.assertContains(response, 'gallery-cards.js')
        self.assertContains(response, 'gallery-letter-glitch.js')
        self.assertContains(response, 'Read System 1')
        self.assertContains(response, 'Read System 6')
        self.assertNotContains(response, 'webgl')

    def test_card_engine_is_scoped_and_power_conscious(self):
        script = (Path(settings.BASE_DIR) / 'website/static/js/gallery-cards.js').read_text()
        self.assertIn('IntersectionObserver', script)
        self.assertIn('rootMargin', script)
        self.assertIn('document.hidden', script)
        self.assertIn('prefers-reduced-motion: reduce', script)
        self.assertIn('navigator.connection?.saveData', script)
        self.assertIn('requestAnimationFrame(paint)', script)
        self.assertNotIn('setInterval(', script)
        self.assertNotIn('THREE', script)
        self.assertNotIn('WebGL', script)
        self.assertIn('pointerleave', script)

    def test_hover_layers_are_inert_and_reduced_motion_is_off(self):
        css = (Path(settings.BASE_DIR) / 'website/static/css/project-pages.css').read_text()
        self.assertIn('.gallery-page .case-tile > .case-tile__signal', css)
        self.assertIn('pointer-events: none;', css)
        self.assertIn('gallery-card-track', css)
        self.assertIn('gallery-card-scan', css)
        self.assertIn('gallery-number-signal', css)
        self.assertIn('gallery-card-breathe', css)
        self.assertIn('gallery-cards--still', css)
        self.assertIn('@media (prefers-reduced-motion: reduce)', css)
        self.assertNotIn('gallery-card-edge', css)

    def test_project_detail_and_home_do_not_load_card_engine(self):
        detail = self.client.get('/en/projects/system-1/')
        self.assertEqual(detail.status_code, 200)
        self.assertNotContains(detail, 'gallery-cards.js')
        self.assertNotContains(detail, 'data-project-card')
        home = self.client.get('/en/')
        self.assertEqual(home.status_code, 200)
        self.assertNotContains(home, 'gallery-cards.js')
