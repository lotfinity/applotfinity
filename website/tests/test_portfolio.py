"""CMS portfolio ordering, publication, editing and HTML regression tests."""
from django.contrib.auth import get_user_model
from django.test import TestCase
from wagtail.models import Site

from website.models import AppPage
from website.models import AppsIndexPage


class PortfolioIntegrationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        site = Site.objects.get(is_default_site=True)
        cls.index = site.root_page.add_child(
            instance=AppsIndexPage(title="Projects", slug="projects")
        )
        cls.index.save_revision().publish()
        cls.second = cls.make_page(
            "Second demo", "second-demo", "Second description", 20,
            "https://example.org/second",
        )
        cls.first = cls.make_page(
            "First demo", "first-demo", "First description", 10,
            "https://example.org/first",
        )

    @classmethod
    def make_page(cls, title, slug, description, order, url):
        project = cls.index.add_child(instance=AppPage(
            title=title, slug=slug, description=description,
            display_order=order, external_url=url,
            key_features="Feature alpha\nFeature beta\n\n",
            show_on_homepage=True,
        ))
        project.save_revision().publish()
        return project

    def test_published_projects_appear_in_editor_defined_order(self):
        response = self.client.get("/en/")
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertLess(html.index('class="app-name">First demo'),
                        html.index('class="app-name">Second demo'))
        self.assertContains(response, "First description")
        self.assertContains(response, "Feature alpha")
        self.assertContains(response, "https://example.org/first")

    def test_editing_cms_record_changes_homepage(self):
        project = AppPage.objects.get(pk=self.first.pk)
        project.description = "Updated through Wagtail"
        project.save_revision().publish()
        response = self.client.get("/en/")
        self.assertContains(response, "Updated through Wagtail")
        self.assertNotContains(response, "First description")

    def test_unfeatured_and_unpublished_pages_are_hidden(self):
        self.second.show_on_homepage = False
        self.second.save_revision().publish()
        draft = self.index.add_child(instance=AppPage(
            title="Draft only", slug="draft-only", live=False,
            display_order=1, show_on_homepage=True,
        ))
        self.assertFalse(draft.live)
        response = self.client.get("/en/")
        self.assertContains(response, "First demo")
        self.assertNotContains(response, "Second demo")
        self.assertNotContains(response, "Draft only")

    def test_project_index_and_detail_pages(self):
        index_page = self.client.get("/en/projects/")
        detail = self.client.get("/en/projects/first-demo/")
        self.assertEqual(index_page.status_code, 200)
        self.assertEqual(detail.status_code, 200)
        self.assertContains(detail, "Feature beta")
        self.assertContains(detail, "Visit project")

    def test_editor_can_open_wagtail_project_form(self):
        editor = get_user_model().objects.create_superuser(
            username="portfolio-editor-test", email="editor@example.test",
            password="not-a-real-login-secret"
        )
        self.client.force_login(editor)
        response = self.client.get(f"/admin/pages/{self.first.pk}/edit/")
        self.assertEqual(response.status_code, 200)
        for name in ("external_url", "key_features", "show_on_homepage", "display_order"):
            self.assertContains(response, name)
