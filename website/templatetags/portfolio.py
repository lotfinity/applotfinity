"""CMS-backed project carousel shared by the homepage and project pages."""
from django import template
from wagtail.models import Site

from website.models import AppPage


register = template.Library()


@register.simple_tag(takes_context=True)
def get_portfolio_projects(context):
    """Show published projects belonging to this Wagtail site, in editor order."""
    projects = AppPage.objects.live().public().filter(show_on_homepage=True)
    request = context.get("request")
    site = Site.find_for_request(request) if request else None
    if site:
        projects = projects.descendant_of(site.root_page)
    return (
        projects.order_by("display_order", "title")
        .select_related("mockup_design")
        .prefetch_related("tech_stack", "tech_stack__logo")
    )
