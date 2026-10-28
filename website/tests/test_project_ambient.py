"""Project case-study visual treatment and background budget regression tests."""
from pathlib import Path

from django.conf import settings
from django.test import TestCase
from wagtail.models import Site

from website.models import AppPage
from website.models import AppsIndexPage


class ProjectAmbientTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        site = Site.objects.get(is_default_site=True)
        index = site.root_page.add_child(
            instance=AppsIndexPage(title="Projects", slug="projects")
        )
        index.save_revision().publish()
        project = index.add_child(
            instance=AppPage(
                title="Node network test",
                slug="node-network-test",
                description="Canvas 2D circuit backdrop test",
            )
        )
        project.save_revision().publish()

    def test_detail_has_only_decorative_background(self):
        response = self.client.get("/en/projects/node-network-test/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="project-detail"')
        self.assertContains(response, 'data-project-network aria-hidden="true"')
        self.assertContains(response, 'class="project-energy__canvas"')
        self.assertContains(response, "js/project-network.js")
        self.assertContains(response, "Node network test")
        self.assertContains(response, "← All projects")

    def test_index_does_not_run_detail_animation(self):
        response = self.client.get("/en/projects/")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "data-project-network")
        self.assertNotContains(response, "project-network.js")

    def test_renderer_has_no_webgl_and_has_energy_budget(self):
        source = (
            Path(settings.BASE_DIR) / "website" / "static" / "js"
            / "project-network.js"
        ).read_text()
        self.assertIn("getContext('2d'", source)
        self.assertNotIn("WebGLRenderer", source)
        self.assertNotIn("requestAnimationFrame(", source)
        self.assertIn("document.hidden", source)
        self.assertIn("prefers-reduced-motion: reduce", source)
        self.assertIn("navigator.connection.saveData", source)
        self.assertIn("mobile ? 23", source)
        self.assertIn("mobile ? 41 : 90", source)
        self.assertIn("1000 / 7", source)
        self.assertIn("1600000", source)
        self.assertIn("430000", source)
