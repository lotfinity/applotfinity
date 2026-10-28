"""
Create or customize your page models here.
"""

from coderedcms.forms import CoderedFormField
from coderedcms.models import CoderedArticleIndexPage
from coderedcms.models import CoderedArticlePage
from coderedcms.models import CoderedEmail
from coderedcms.models import CoderedEventIndexPage
from coderedcms.models import CoderedEventOccurrence
from coderedcms.models import CoderedEventPage
from coderedcms.models import CoderedFormPage
from coderedcms.models import CoderedLocationIndexPage
from coderedcms.models import CoderedLocationPage
from coderedcms.models import CoderedWebPage
from modelcluster.fields import ParentalKey


class ArticlePage(CoderedArticlePage):
    """
    Article, suitable for news or blog content.
    """

    class Meta:
        verbose_name = "Article"
        ordering = ["-first_published_at"]

    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ["website.ArticleIndexPage"]

    template = "coderedcms/pages/article_page.html"
    search_template = "coderedcms/pages/article_page.search.html"


class ArticleIndexPage(CoderedArticleIndexPage):
    """
    Shows a list of article sub-pages.
    """

    class Meta:
        verbose_name = "Article Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "website.ArticlePage"

    # Only allow ArticlePages beneath this page.
    subpage_types = ["website.ArticlePage"]

    template = "coderedcms/pages/article_index_page.html"


class EventPage(CoderedEventPage):
    class Meta:
        verbose_name = "Event Page"

    parent_page_types = ["website.EventIndexPage"]
    template = "coderedcms/pages/event_page.html"


class EventIndexPage(CoderedEventIndexPage):
    """
    Shows a list of event sub-pages.
    """

    class Meta:
        verbose_name = "Events Landing Page"

    index_query_pagemodel = "website.EventPage"

    # Only allow EventPages beneath this page.
    subpage_types = ["website.EventPage"]

    template = "coderedcms/pages/event_index_page.html"


class EventOccurrence(CoderedEventOccurrence):
    event = ParentalKey(EventPage, related_name="occurrences")


class FormPage(CoderedFormPage):
    """
    A page with an html <form>.
    """

    class Meta:
        verbose_name = "Form"

    template = "coderedcms/pages/form_page.html"


class FormPageField(CoderedFormField):
    """
    A field that links to a FormPage.
    """

    class Meta:
        ordering = ["sort_order"]

    page = ParentalKey("FormPage", related_name="form_fields")


class FormConfirmEmail(CoderedEmail):
    """
    Sends a confirmation email after submitting a FormPage.
    """

    page = ParentalKey("FormPage", related_name="confirmation_emails")


class LocationPage(CoderedLocationPage):
    """
    A page that holds a location.  This could be a store, a restaurant, etc.
    """

    class Meta:
        verbose_name = "Location Page"

    template = "coderedcms/pages/location_page.html"

    # Only allow LocationIndexPages above this page.
    parent_page_types = ["website.LocationIndexPage"]


class LocationIndexPage(CoderedLocationIndexPage):
    """
    A page that holds a list of locations and displays them with a Google Map.
    This does require a Google Maps API Key in Settings > CRX Settings
    """

    class Meta:
        verbose_name = "Location Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "website.LocationPage"

    # Only allow LocationPages beneath this page.
    subpage_types = ["website.LocationPage"]

    template = "coderedcms/pages/location_index_page.html"


class WebPage(CoderedWebPage):
    """
    General use page with featureful streamfield and SEO attributes.
    """

    class Meta:
        verbose_name = "Web Page"

    template = "coderedcms/pages/web_page.html"

class PengaaPage(CoderedWebPage):
    """
    General use page with featureful streamfield and SEO attributes.
    """

    class Meta:
        verbose_name = "pengaa Page"

    template = "pengaa/pengaa.html"


from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel
from django.db import models

@register_snippet
class TechStack(models.Model):
    """
    Represents a reusable technology or tool that can be associated with apps.
    """
    name = models.CharField(max_length=255, verbose_name="Technology Name")
    description = models.TextField(blank=True, verbose_name="Description")
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Logo"
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("logo"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tech Stack"
        verbose_name_plural = "Tech Stacks"

from wagtail.blocks import RichTextBlock, StructBlock, StreamBlock
from wagtail.images.blocks import ImageChooserBlock

class AppStreamBlock(StreamBlock):
    heading = RichTextBlock(
        features=["h2", "h3", "bold", "italic"], 
        icon="title", 
        label="Heading"
    )
    paragraph = RichTextBlock(icon="pilcrow", label="Paragraph")
    image = ImageChooserBlock(icon="image", label="Image")

    class Meta:
        icon = "placeholder"
        label = "App Content Blocks"

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.images.fields import ImageField
from modelcluster.fields import ParentalManyToManyField
from django import forms

class AppPage(Page):
    """
    A page representing an individual app.
    """
    banner_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL,
        related_name="+", help_text="Designed project banner; keep screenshots in Mockup Design or device fields.",
    )
    mockup_design = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Mockup Design",
    )
    device_desktop_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL,
        related_name="+", help_text="Optional desktop screenshot for the CSS laptop showcase.",
    )
    device_mobile_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL,
        related_name="+", help_text="Optional mobile screenshot for the CSS phone showcase.",
    )
    device_mobile_secondary_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL,
        related_name="+", help_text="Optional second genuine mobile screenshot for the device gallery.",
    )
    description = models.TextField(blank=True, verbose_name="App Description")
    external_url = models.URLField(
        blank=True, help_text="Optional live demo or external project website."
    )
    source_url = models.URLField(
        blank=True,
        help_text="Public source repository (leave blank for private work).",
    )
    focus_area = models.CharField(
        max_length=90, blank=True, default="",
        help_text="Short category such as Hardware Simulation or Data Intelligence.",
    )
    project_stage = models.CharField(
        max_length=32,
        default="case_study",
        choices=[
            ("active", "Active development"),
            ("prototype", "Prototype"),
            ("test_release", "Test release"),
            ("case_study", "Case study"),
        ],
    )
    key_features = models.TextField(
        blank=True,
        help_text="One key feature per line; shown beneath the project description.",
    )
    show_on_homepage = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(
        default=0, help_text="Lower numbers appear first on the homepage."
    )
    tech_stack = ParentalManyToManyField("TechStack", blank=True)

    parent_page_types = ["website.AppsIndexPage"]

    @property
    def feature_items(self):
        return [line.strip() for line in self.key_features.splitlines() if line.strip()]

    body = StreamField(
        AppStreamBlock(),  # Use the custom block defined earlier
        verbose_name="Page Body",
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("banner_image"),
        FieldPanel("mockup_design"),
        FieldPanel("device_desktop_image"),
        FieldPanel("device_mobile_image"),
        FieldPanel("device_mobile_secondary_image"),
        FieldPanel("description"),
        FieldPanel("external_url"),
        FieldPanel("source_url"),
        FieldPanel("focus_area"),
        FieldPanel("project_stage"),
        FieldPanel("key_features"),
        FieldPanel("show_on_homepage"),
        FieldPanel("display_order"),
        FieldPanel("tech_stack", widget=forms.CheckboxSelectMultiple),
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "App Page"

class AppsIndexPage(Page):
    """
    An index page listing all apps.
    """
    introduction = models.TextField(help_text="Text to describe the page", blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="An image to represent this page.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("image"),
    ]

    # Restrict subpages to only AppPage
    subpage_types = ["AppPage"]

    def get_apps(self):
        return (
            AppPage.objects.live().public().descendant_of(self)
            .order_by("display_order", "title")
            .prefetch_related("tech_stack", "tech_stack__logo")
        )

    def get_context(self, request):
        context = super().get_context(request)
        apps = self.get_apps()
        context["apps"] = apps
        context["featured_apps"] = [app for app in apps if app.show_on_homepage]
        context["archive_apps"] = [app for app in apps if not app.show_on_homepage]
        context["featured_count"] = len(context["featured_apps"])
        return context


from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from wagtail_localize.fields import TranslatableField
from wagtail.models import TranslatableMixin

@register_snippet
class InstagramPostSnippet(TranslatableMixin, models.Model):
    """
    A translatable snippet model for Instagram posts.
    """

    caption = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="instagram_posts/", blank=True, null=True)
    video = models.FileField(upload_to="instagram_videos/", blank=True, null=True)
    json_metadata = models.JSONField(blank=True, null=True)
    timestamp = models.DateTimeField()

    # Translatable Fields
    translatable_fields = [
        TranslatableField("caption"),
    ]

    panels = [
        FieldPanel("caption"),
        FieldPanel("image"),
        FieldPanel("video"),
        FieldPanel("json_metadata"),
        FieldPanel("timestamp"),
    ]

    api_fields = [
        APIField("caption"),
        APIField("image"),
        APIField("video"),
        APIField("json_metadata"),
        APIField("timestamp"),
    ]

    def __str__(self):
        return f"Instagram Post - {self.timestamp}"


from wagtail.models import Page
from coderedcms.models import CoderedWebPage
from wagtail.models import Locale
from .models import InstagramPostSnippet
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

class InstagramPostPage(CoderedWebPage):
    """
    A page model to display Instagram posts.
    """
    template = "instagram_post_page.html"

    class Meta:
        verbose_name = "Instagram Post Page"

    def get_context(self, request):
        context = super().get_context(request)
        current_locale = Locale.get_active()
        posts = InstagramPostSnippet.objects.filter(locale=current_locale).order_by("timestamp")

        # Handle AJAX request for infinite scroll
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            page = int(request.GET.get('page', 1))
            count = int(request.GET.get('count', 10))
            start = (page - 1) * count
            end = start + count
            posts = posts[start:end]
            posts_data = [
                {
                    "image": post.image.url if post.image else None,
                    "video": post.video.url if post.video else None,
                }
                for post in posts
            ]
            return JsonResponse({"posts": posts_data})

        context["posts"] = posts[:50]
        context["post_id"] = request.GET.get('post_id', None)  # Ensure post_id is passed to the context
        return context

    @staticmethod
    def get_post_content(request, post_id):
        post = get_object_or_404(InstagramPostSnippet, id=post_id)
        content = render_to_string("post_content.html", {"post": post})
        return JsonResponse({"content": content})
# Site-level homepage content and ordered editor-controlled components.
from .homepage_settings import HomepageSettings, HomepageService, HomepageSkill  # noqa: E402,F401
