"""Prevent an accidental return of always-on WebGL or duplicate animation runtimes."""
from pathlib import Path

from django.conf import settings
from django.test import TestCase


class HomepageEnergyRegressionTests(TestCase):
    def test_webgl_renderer_has_a_frame_budget_and_idles(self):
        bundle = (
            Path(settings.BASE_DIR) / "website" / "static" / "js" / "main.js"
        ).read_text()
        self.assertIn("t-this._lastDraw>=(e?22:16)", bundle)
        self.assertIn("t-this._lastInput>6500", bundle)
        self.assertIn("new xd(1,\"ontouchstart\"in document.documentElement?12:16)", bundle)
        self.assertIn("antialias:!0", bundle)
        self.assertIn("document.hidden", bundle)
        self.assertIn("setTimeout(this._tick,800)", bundle)
        self.assertIn("prefers-reduced-motion", bundle)
        self.assertNotIn("requestAnimationFrame(this.animate.bind(this))", bundle)

    def test_homepage_does_not_load_second_gsap_runtime(self):
        page = self.client.get("/en/")
        self.assertEqual(page.status_code, 200)
        html = page.content.decode()
        self.assertNotIn("cdnjs.cloudflare.com/ajax/libs/gsap/3.11.3", html)
        self.assertIn("new IntersectionObserver", html)
        self.assertIn("main.js?v=smooth-1", html)
