"""The five repository-backed case studies share a scoped presentation."""

from django.test import TestCase
from wagtail.models import Site

from website.models import AppPage
from website.models import AppsIndexPage
from website.project_source_stories import STORIES


class ProjectSourceStoriesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        root = Site.objects.get(is_default_site=True).root_page
        index = root.add_child(
            instance=AppsIndexPage(title="Projects", slug="projects")
        )
        index.save_revision().publish()
        for slug, story in STORIES.items():
            page = index.add_child(
                instance=AppPage(
                    title=story["title"],
                    slug=slug,
                    description=story["description"],
                    source_url="https://github.com/lotfinity/"
                    + (
                        "IstanbulPropTech"
                        if slug == "istanbulproptech"
                        else "beyond-website-v5"
                        if slug == "beyond-website"
                        else "pricebridge-clean"
                        if slug == "pricebridge"
                        else slug
                    ),
                    body=[
                        (
                            "heading",
                            "<h2>Source-reviewed engineering narrative</h2>",
                        )
                    ],
                )
            )
            page.save_revision().publish()

    def test_each_source_story_has_source_links_and_correct_layout(self):
        self.assertEqual(len(STORIES), 5)
        for slug, story in STORIES.items():
            with self.subTest(slug=slug):
                response = self.client.get(f"/en/projects/{slug}/")
                self.assertEqual(response.status_code, 200)
                self.assertContains(
                    response, 'class="lotot-story source-story"'
                )
                self.assertContains(
                    response, 'class="lotot-story__spotlight"', count=4
                )
                self.assertContains(response, "lotot-story__flow")
                self.assertContains(response, story["sha"])
                self.assertContains(response, story["caveat"])
                self.assertContains(
                    response, "Source-reviewed engineering narrative"
                )
                self.assertEqual(len(story["flow"]), 6)

    def test_unrelated_page_has_no_new_story(self):
        r = self.client.get("/en/projects/")
        self.assertEqual(r.status_code, 200)
        self.assertNotContains(r, 'class="lotot-story source-story"')
