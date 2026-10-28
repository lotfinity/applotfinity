"""Foundation regression tests for the Lotusfinity public website."""
from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase


class PublicSiteSecurityTests(TestCase):
    """HTTP requests must not mutate global settings or bypass CSRF."""

    def test_homepage_section_hierarchy(self):
        """Portfolio markup must not close the scroll wrapper too early."""
        response = self.client.get("/en/")
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, "html.parser")
        app = soup.select_one("#app")
        self.assertIsNotNone(app)
        self.assertIsNotNone(app.select_one("#studio"))
        self.assertIsNotNone(app.select_one("#studio .studio__section__trusted"))
        work = app.select_one("#web .web__section__content")
        self.assertIsNotNone(work)
        self.assertIsNotNone(work.select_one(".web__section__cta"))
        self.assertIsNotNone(work.select_one(".swiper-container .swiper-wrapper"))
        self.assertEqual(len(work.select(".web__section__legende")), 2)

    def test_homepage_works_without_changing_debug(self):
        original_debug = settings.DEBUG
        response = self.client.get("/en/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lotfinity")
        self.assertEqual(settings.DEBUG, original_debug)

    def test_superuser_request_does_not_enable_debug_globally(self):
        original_debug = settings.DEBUG
        admin = get_user_model().objects.create_superuser(
            username="preview-test-admin",
            email="test-admin@example.test",
            password="not-a-real-login-secret",
        )
        self.client.force_login(admin)
        response = self.client.get("/en/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(settings.DEBUG, original_debug)

    def test_csrf_is_enforced_on_admin_login(self):
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.post(
            "/django-admin/login/", {"username": "irrelevant", "password": "no"}
        )
        self.assertEqual(response.status_code, 403)

    def test_debug_toolbar_is_not_enabled_in_preview(self):
        self.assertNotIn("debug_toolbar", settings.INSTALLED_APPS)
        self.assertFalse(
            any("debug_toolbar" in middleware for middleware in settings.MIDDLEWARE)
        )

    def test_no_request_middleware_changes_debug_setting(self):
        self.assertFalse(
            any("SuperuserDebugMiddleware" in item for item in settings.MIDDLEWARE)
        )
