"""End-to-end rendered homepage and Wagtail settings regression coverage."""
from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from wagtail.models import Site

from website.homepage_settings import HomepageService
from website.homepage_settings import HomepageSettings
from website.homepage_settings import HomepageSkill


class HomepageSettingsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.site = Site.objects.get(is_default_site=True)
        cls.home = HomepageSettings.for_site(cls.site)
        HomepageService.objects.create(homepage=cls.home, sort_order=0, text="Initial service")
        HomepageSkill.objects.create(
            homepage=cls.home, sort_order=0, name="Django", description="Backend", percentage=90
        )

    def test_homepage_content_can_be_edited_without_template_changes(self):
        self.home.hero_prefix = "Build"
        self.home.web_heading = "Custom AI studio title"
        self.home.contact_label = "Message the studio"
        self.home.site_title = "Editable Lotfinity SEO title"
        self.home.save()
        page = self.client.get("/en/")
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, "Custom AI studio title")
        self.assertContains(page, "Message the studio")
        self.assertContains(page, "Editable Lotfinity SEO title")
        self.assertContains(page, "Build")

    def test_ordered_services_and_skills_appear(self):
        HomepageService.objects.create(
            homepage=self.home, sort_order=1, text="Second service"
        )
        HomepageSkill.objects.create(
            homepage=self.home, sort_order=1, name="Python", percentage=95
        )
        page = self.client.get("/en/")
        text = page.content.decode()
        self.assertLess(text.index("Initial service"), text.index("Second service"))
        self.assertLess(text.index('data-skill-percent="90"'), text.index('data-skill-percent="95"'))
        self.assertContains(page, "Python")

    def test_section_visibility_does_not_break_other_sections(self):
        self.home.show_projects = False
        self.home.show_services = False
        self.home.show_studio = False
        self.home.save()
        page = self.client.get("/en/")
        self.assertEqual(page.status_code, 200)
        soup = BeautifulSoup(page.content, "html.parser")
        self.assertIsNotNone(soup.select_one("#intro"))
        self.assertIsNotNone(soup.select_one("#web"))
        self.assertIsNone(soup.select_one("#web .swiper-container"))
        self.assertIsNone(soup.select_one("#studio"))
        self.assertIsNone(soup.select_one(".anchor-link-studio"))
        self.assertIsNone(soup.select_one("#web .web__section__cta"))

    def test_editable_text_is_escaped(self):
        self.home.web_heading = '<script>alert("test")</script>'
        self.home.save()
        page = self.client.get("/en/")
        self.assertNotContains(page, '<script>alert("test")</script>', html=False)
        self.assertContains(page, '&lt;script&gt;', html=False)

    def test_editor_form_contains_required_panels(self):
        editor = get_user_model().objects.create_superuser(
            username="homepage-editor-test", email="editor@example.test",
            password="local-test-only-secret"
        )
        self.client.force_login(editor)
        url = reverse("wagtailsettings:edit", args=["website", "homepagesettings", self.site.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for name in ("hero_prefix", "web_heading", "show_studio",
                     "contact_email", "skills", "services"):
            self.assertContains(response, name)
