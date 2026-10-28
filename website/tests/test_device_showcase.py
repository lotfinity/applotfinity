"""Verify the reusable, screenshot-only CSS device mockups."""
from django.test import TestCase
from wagtail.images import get_image_model
from wagtail.models import Site

from website.models import AppPage
from website.models import AppsIndexPage


class ProjectDeviceShowcaseTests(TestCase):
    def setUp(self):
        root = Site.objects.get(is_default_site=True).root_page
        self.index = root.add_child(instance=AppsIndexPage(title="Showcase", slug="showcase", locale=root.locale))
        self.index.save_revision().publish()
        self.project = self.index.add_child(instance=AppPage(title="Test device demo", slug="test-device-demo", locale=root.locale))
        self.project.save_revision().publish()

    def test_no_device_mockup_without_images(self):
        response = self.client.get(self.project.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'class="device-showcase"')

    def test_device_mockup_only_when_images_present(self):
        from io import BytesIO

        from django.core.files.base import ContentFile
        from PIL import Image
        buf = BytesIO()
        Image.new("RGB", (160, 90), "#ffffff").save(buf, format="PNG")
        image = get_image_model().objects.create(title="Test screenshot", file=ContentFile(buf.getvalue(), name="test.png"))
        self.project.device_desktop_image = image
        self.project.device_mobile_image = image
        self.project.save_revision().publish()
        response = self.client.get(self.project.url)
        self.assertContains(response, 'class="device-showcase"')
        self.assertContains(response, 'class="device-laptop"')
        self.assertContains(response, 'class="device-phone"')
        self.assertContains(response, "Desktop screenshot of Test device demo")
        self.assertContains(response, "Mobile screenshot of Test device demo")
        self.assertNotContains(response, "three.js")
