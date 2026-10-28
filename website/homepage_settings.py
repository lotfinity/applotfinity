"""Editable homepage content, layout toggles and ordered services/skills.

Keep page-specific portfolio entries in AppPage; only shared homepage presentation
belongs here. Settings are per Wagtail site, not per translation locale.
"""
from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel
from wagtail.admin.panels import InlinePanel
from wagtail.admin.panels import MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.models import register_setting
from wagtail.models import Orderable


@register_setting
class HomepageSettings(BaseSiteSetting, ClusterableModel):
    """The content editor for the original animated Lotfinity landing page."""

    site_title = models.CharField(max_length=160, default="Lotfinity | Creative Web Studio")
    seo_description = models.TextField(
        default="Lotfinity builds creative websites, web applications, AI systems, and digital experiences."
    )
    byline_verb = models.CharField(max_length=100, default="Crafting")
    byline_description = models.CharField(max_length=160, default="Digital artistery")
    hero_prefix = models.CharField(max_length=100, default="Unique")
    hero_emphasis = models.CharField(max_length=100, default="Digital")
    hero_suffix = models.CharField(max_length=100, default="artistery")

    web_marker = models.CharField(max_length=120, default="Fullstack Development")
    web_kicker = models.CharField(
        max_length=220, default="Why manage your website when it can manage itself?"
    )
    web_heading = models.CharField(
        max_length=260,
        default="Imagine a website that can listen, think, act – and REMEMBER..!!",
    )
    web_intro_before = models.TextField(default=(
        "Having an AI-powered website is great—it can assist with content creation, SEO, and basic "
        "management. But what if your website was an autonomous intelligence, built to understand, "
        "adapt, and evolve with you? With MEMORY at its core, you never have to repeat yourself—once "
        "it learns your preferences, content style, and design approach, it handles everything seamlessly. "
        "The websites we create at "
    ))
    web_intro_after = models.TextField(default=(
        " are not just AI-supported; they are AI itself—self-thinking, self-optimizing, and constantly "
        "improving. This is not just a website. This is intelligence in motion."
    ))
    show_projects = models.BooleanField(default=True)
    projects_heading = models.CharField(max_length=100, default="Web-apps")
    projects_subheading = models.CharField(
        max_length=160, default="Smart & Fast : Click to Preview !"
    )

    show_services = models.BooleanField(default=True)
    web_secondary_kicker = models.CharField(
        max_length=220, default="Your Website. Your Data. Your Control."
    )
    web_secondary_heading = models.CharField(
        max_length=260, default="A Website That Operates Locally, Securely, and Intelligently."
    )
    web_secondary_lead_before = models.TextField(default=(
        "Unlike AI systems that rely on external APIs, every website we create at "
    ))
    web_secondary_lead_after = models.TextField(default=(
        " runs entirely on private hardware  either yours or ours—ensuring total independence "
        "and security. Your website, your chatbot, and every lead or interaction it handles remain "
        "stored in a dedicated environment. No third-party access, no unnecessary data exposure—only "
        "YOU control your digital ecosystem."
    ))
    web_automation = models.TextField(default=(
        "More than just a management system, this AI functions as an integrated chatbot that captures "
        "leads, automates interactions, and serves as a seamless bridge between human teams and AI "
        "automation. Whether it's assisting customers, structuring content, or executing tasks in "
        "real time, it operates like an intelligent digital assistant always working behind the scenes."
    ))
    contact_label = models.CharField(max_length=100, default="Get in Touch")
    contact_email = models.EmailField(default="lotfinity2023.io51023@gmail.com")
    telegram_url = models.URLField(blank=True, default="https://t.me/Lotfikanouni")
    whatsapp_url = models.URLField(blank=True, default="https://wa.me/905380546393")
    github_url = models.URLField(blank=True, default="https://github.com/lotfinity")
    contact_city = models.CharField(max_length=140, default="Istanbul - Turkey")

    show_studio = models.BooleanField(default=True)
    studio_title = models.CharField(max_length=120, default="Studio")
    studio_subtitle = models.CharField(max_length=180, default="passion & profession")
    studio_bio = models.CharField(
        max_length=220, default="LOTFI KANOUNI, FSDev & Designer, SEO & Marketing"
    )
    hosted_services_label = models.CharField(
        max_length=200, default="Check our Hosted Services"
    )
    hosted_services_url = models.URLField(blank=True)
    studio_manifesto = models.TextField(default=(
        "Mind. Clean code from scratch, immersive web experience, performance, organized workflow, fun!"
    ))
    expertise_title = models.CharField(max_length=120, default="Expertise in:")
    expertise_description = models.TextField(default=(
        "Django, Flask, PaaS APIs, LLM Models, Hosting Solutions, Server Development, and more – "
        "Providing high-performance, scalable solutions for top-tier clients – Thanks!"
    ))

    panels = [
        MultiFieldPanel([
            FieldPanel("site_title"), FieldPanel("seo_description"),
        ], heading="Search & browser metadata"),
        MultiFieldPanel([
            FieldPanel("byline_verb"), FieldPanel("byline_description"),
            FieldPanel("hero_prefix"), FieldPanel("hero_emphasis"),
            FieldPanel("hero_suffix"),
        ], heading="Hero / landing headline"),
        MultiFieldPanel([
            FieldPanel("web_marker"), FieldPanel("web_kicker"),
            FieldPanel("web_heading"), FieldPanel("web_intro_before"),
            FieldPanel("web_intro_after"),
        ], heading="Work: introduction"),
        MultiFieldPanel([
            FieldPanel("show_projects"), FieldPanel("projects_heading"),
            FieldPanel("projects_subheading"),
        ], heading="Projects carousel (project records are edited under Pages)"),
        MultiFieldPanel([
            FieldPanel("show_services"), FieldPanel("web_secondary_kicker"),
            FieldPanel("web_secondary_heading"), FieldPanel("web_secondary_lead_before"),
            FieldPanel("web_secondary_lead_after"), FieldPanel("web_automation"),
            InlinePanel("services", label="Service", heading="Service checklist"),
        ], heading="Services & approach"),
        MultiFieldPanel([
            FieldPanel("show_studio"), FieldPanel("studio_title"),
            FieldPanel("studio_subtitle"), FieldPanel("studio_bio"),
            InlinePanel("skills", label="Skill", heading="Animated skill circles"),
            FieldPanel("hosted_services_label"), FieldPanel("hosted_services_url"),
            FieldPanel("studio_manifesto"), FieldPanel("expertise_title"),
            FieldPanel("expertise_description"),
        ], heading="Studio & skills"),
        MultiFieldPanel([
            FieldPanel("contact_label"), FieldPanel("contact_email"),
            FieldPanel("telegram_url"), FieldPanel("whatsapp_url"),
            FieldPanel("github_url"), FieldPanel("contact_city"),
        ], heading="Contact and social links"),
    ]

    class Meta:
        verbose_name = "Lotfinity homepage"


class HomepageService(Orderable):
    homepage = ParentalKey(
        HomepageSettings, related_name="services", on_delete=models.CASCADE
    )
    text = models.CharField(max_length=240)
    panels = [FieldPanel("text")]


class HomepageSkill(Orderable):
    homepage = ParentalKey(
        HomepageSettings, related_name="skills", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=180, blank=True)
    percentage = models.PositiveSmallIntegerField(default=80)
    icon = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+",
    )
    panels = [
        FieldPanel("name"), FieldPanel("description"),
        FieldPanel("percentage"), FieldPanel("icon"),
    ]

    def clean(self):
        from django.core.exceptions import ValidationError
        super().clean()
        if not 0 <= self.percentage <= 100:
            raise ValidationError({"percentage": "Enter a percentage between 0 and 100."})
