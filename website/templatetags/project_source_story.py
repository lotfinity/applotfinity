"""Curated, source-linked engineering details for non-LotoT featured projects."""

from django import template

from website.project_source_stories import STORIES


register = template.Library()


@register.simple_tag
def engineering_story(slug):
    return STORIES.get(slug)
