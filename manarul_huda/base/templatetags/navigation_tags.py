from django import template

from base.models import FooterText, MenuItem
from wagtail.models import Site, Page

register = template.Library()

# get the footer text
@register.inclusion_tag("base/includes/footer_text.html", takes_context=True)
def get_footer_text(context):
    footer_text = context.get("footer_text", "")

    if not footer_text:
        instance = FooterText.objects.filter(live=True).first()
        footer_text = instance.body if instance else ""

    return {
        "footer_text": footer_text,
    }

# breadcrumb
@register.inclusion_tag("includes/tags/breadcrumbs.html", takes_context=True)
def breadcrumbs(context):
    self = context.get("self")
    if self is None or self.depth <= 2:
        # When on the home page, displaying breadcrumbs is irrelevant.
        ancestors = ()
    else:
        ancestors = Page.objects.ancestor_of(self, inclusive=True).filter(depth__gt=1)
    return {
        "ancestors": ancestors,
        "request": context["request"],
    }

@register.inclusion_tag('includes/tags/navigation.html', takes_context=True)
def get_menu_items(context):
    menu_items = MenuItem.objects.filter(parent=None)
    return {
        'menu_items': menu_items,
        'request': context['request'],
    }