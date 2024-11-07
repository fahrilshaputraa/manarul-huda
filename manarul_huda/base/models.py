from django.db import models
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,

    # import PublishingPanel:
    PublishingPanel,
)

# import RichTextField:
from wagtail.fields import RichTextField

# import DraftStateMixin, PreviewableMixin, RevisionMixin, TranslatableMixin:
from wagtail.models import (
    DraftStateMixin,
    PreviewableMixin,
    RevisionMixin,
    TranslatableMixin,
)

from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting,
)

from wagtail.models import Page
from django.core.exceptions import ValidationError

# import register_snippet:
from wagtail.snippets.models import register_snippet
@register_setting
class NavigationSettings(BaseGenericSetting):
    twitter_url = models.URLField(verbose_name="Twitter URL", blank=True)
    github_url = models.URLField(verbose_name="GitHub URL", blank=True)
    mastodon_url = models.URLField(verbose_name="Mastodon URL", blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("twitter_url"),
                FieldPanel("github_url"),
                FieldPanel("mastodon_url"),
            ],
            "Social settings",
        )
    ]


@register_snippet
class FooterText(
    DraftStateMixin,
    RevisionMixin,
    PreviewableMixin,
    TranslatableMixin,
    models.Model,
):

    body = RichTextField()

    panels = [
        FieldPanel("body"),
        PublishingPanel(),
    ]

    def __str__(self):
        return "Footer text"

    def get_preview_template(self, request, mode_name):
        return "base.html"

    def get_preview_context(self, request, mode_name):
        return {"footer_text": self.body}

    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = "Footer Text"
        
@register_snippet
class MenuItem(models.Model):
    name_item = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    page = models.ForeignKey(
        Page,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='+',
        limit_choices_to={'show_in_menus': True},
        help_text='Select a page that is marked to show in menus'
    )
    is_parent = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE,
        null=True, 
        blank=True, 
        limit_choices_to={'is_parent': True},
        related_name='sub_items'
    )
    icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Upload an SVG icon for this menu item"
    )

    def __str__(self):
        return self.name_item

    def get_url(self):
        if self.page:
            return self.page.url
        elif self.url:
            return self.url
        return '#'

    def get_children(self):
        return self.sub_items.all()

    def clean(self):
        if self.icon:
            # Check if uploaded file is SVG
            if not self.icon.filename.lower().endswith('.svg'):
                raise ValidationError({'icon': 'Only SVG files are allowed for icons.'})

    class Meta:
        ordering = ['name_item']