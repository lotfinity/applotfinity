"""Expose the editable Wagtail homepage settings to the legacy animated page."""
from django import template
from wagtail.models import Site

from website.homepage_settings import HomepageSettings


register = template.Library()


@register.simple_tag(takes_context=True)
def get_homepage_settings(context):
    """Fetch site-specific homepage controls without changing Wagtail's Page types."""
    request = context.get("request")
    if request is None:
        return None
    site = Site.find_for_request(request)
    return HomepageSettings.for_site(site) if site else None
