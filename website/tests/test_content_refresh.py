"""The actual public portfolio should remain honest, editable and reproducible."""
from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from wagtail.models import Site

from website.homepage_settings import HomepageSettings
from website.models import AppPage
from website.models import AppsIndexPage


class CuratedPortfolioTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        out = StringIO()
        call_command("seed_portfolio", stdout=out)
        call_command("seed_homepage", stdout=out)
        call_command("curate_portfolio", apply=True, stdout=out)

    def test_six_real_public_projects_in_editor_order(self):
        featured = list(
            AppPage.objects.live().filter(show_on_homepage=True).order_by("display_order")
        )
        self.assertEqual(len(featured), 6)
        self.assertEqual(featured[0].slug, "ohmlet")
        self.assertEqual(featured[0].external_url, "https://byd.whatsynaptic.com/")
        self.assertEqual(featured[1].slug, "pricebridge")
        self.assertEqual(featured[-1].slug, "beyond-website")
        for project in featured:
            self.assertTrue(project.source_url.startswith("https://github.com/lotfinity/"))
            self.assertTrue(project.focus_area)
            if project.slug != "ohmlet":
                self.assertFalse(project.external_url)
        self.assertEqual(
            AppPage.objects.filter(show_on_homepage=False).count(), 4,
        )

    def test_honest_stage_labels_and_source_attribution(self):
        self.assertEqual(AppPage.objects.get(slug="neon-strip-studio").project_stage, "test_release")
        self.assertEqual(AppPage.objects.get(slug="pricebridge").project_stage, "prototype")
        self.assertIn("AndrOBD", AppPage.objects.get(slug="lotot").key_features)
        self.assertIn("not yet verified", AppPage.objects.get(slug="neon-strip-studio").key_features)
        self.assertTrue(AppPage.objects.get(slug="ohmlet").mockup_design)

    def test_homepage_and_index_are_real_work_not_old_sales_copy(self):
        home = self.client.get("/en/")
        self.assertContains(home, "Connect")
        self.assertContains(home, "The interesting work starts")
        self.assertContains(home, "Ohmlet")
        self.assertContains(home, 'href="https://byd.whatsynaptic.com/"')
        self.assertContains(home, "Launch live app")
        self.assertContains(home, "PriceBridge")
        self.assertNotContains(home, "self-thinking, self-optimizing")
        self.assertNotContains(home, "synaptic-remote-gateway")
        index = AppsIndexPage.objects.get(slug="projects")
        response = self.client.get(index.url)
        self.assertContains(response, "Selected builds")
        self.assertContains(response, "Earlier website work")
        self.assertContains(response, "Public source")
        self.assertContains(response, "Launch live app")

    def test_rerun_does_not_overwrite_editor_edits_or_create_duplicates(self):
        site = Site.objects.get(is_default_site=True)
        home = HomepageSettings.for_site(site)
        home.web_heading = "My custom editor headline"
        home.save()
        project = AppPage.objects.get(slug="pricebridge")
        project.description = "Edited project description"
        project.save_revision().publish()
        legacy = AppPage.objects.get(slug="dentidelil-international")
        legacy.show_on_homepage = True
        legacy.save_revision().publish()
        call_command("curate_portfolio", apply=True, stdout=StringIO())
        legacy.refresh_from_db()
        self.assertTrue(legacy.show_on_homepage)
        home.refresh_from_db()
        project.refresh_from_db()
        self.assertEqual(home.web_heading, "My custom editor headline")
        self.assertEqual(project.description, "Edited project description")
        self.assertEqual(AppPage.objects.filter(show_on_homepage=True).count(), 7)
        self.assertEqual(home.skills.count(), 8)
        self.assertEqual(home.services.count(), 8)
