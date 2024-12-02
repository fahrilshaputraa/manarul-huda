from django.db import models
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,

    # import PublishingPanel:
    PublishingPanel,
)

from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting,
)

from wagtail.models import Page
from django.core.exceptions import ValidationError

# import register_snippet:
from wagtail.snippets.models import register_snippet
from wagtail.models import Collection

from wagtailmetadata.models import MetadataPageMixin
from wagtail.blocks import StructBlock, CharBlock, PageChooserBlock, URLBlock, StreamBlock, StructBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.fields import StreamField
    
@register_setting(icon="site")
class WebsiteSettings(BaseGenericSetting):
    icon = "globe"
    name = models.CharField(max_length=255, help_text="Name of the website")
    sub_name = models.CharField(max_length=255, help_text="Sub Name of the website", null=True)
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    location = models.CharField(max_length=255, help_text="Location of the website")
    location_link = models.URLField(verbose_name="Location Url", null=True)
    phone = models.CharField(max_length=255, help_text="Phone number of the website")
    email = models.EmailField(help_text="Email of the website")
    copyright = models.CharField(max_length=255, help_text="Copyright of the website")
    
    panels = [
         MultiFieldPanel(
            [
            FieldPanel("name"),
            FieldPanel("sub_name"),
            FieldPanel("logo"),
            FieldPanel("location"),
            FieldPanel("location_link"),
            FieldPanel("phone"),
            FieldPanel("email"),
            FieldPanel("copyright"),
            ],
            "Website Settings"
         )
    ]


@register_setting(icon="site")
class FooterText(BaseGenericSetting):

    menu_items = StreamField([
        ("menu_item", StructBlock([
            ("title", CharBlock(max_length=100)),
            ("link", StreamBlock([
                ("items", StructBlock([
                    ("title", CharBlock(max_length=100)), 
                    ("page", PageChooserBlock(required=False)),
                    ("external_link", URLBlock(required=False)),
                ])),
            ],
            max_num=5,
            min_num=1,
            )),
        ])),
    ],
        use_json_field=True,
        max_num=2,
        min_num=2,
        null=True,
    )
    social_media = StreamField([
        ("social_media", StructBlock([
            ("icon", ImageChooserBlock(required=False)),
            ("link", URLBlock(required=False)),
        ])),
    ],
        use_json_field=True,
        max_num=5,
        min_num=1,
        null=True,
    )

    panels = [
        FieldPanel("menu_items"), 
        FieldPanel("social_media"),
        PublishingPanel(),
    ]

    def __str__(self):
        return "Footer text"
    
    def clean(self):
        for block in self.menu_items:
            for link in block.value['link']:
                if not (bool(link.value['page']) ^ bool(link.value['external_link'])):
                    raise ValidationError({'menu_items': "Please choose exactly one: page or external link"})
                    
        for block in self.social_media:
            if not block.value['icon'].filename.lower().endswith('.svg'):
                raise ValidationError({'social_media': "Icon must be an SVG file"})

        
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

class Gallery(MetadataPageMixin, Page):
    template = "base/gallery_page.html"
    introduction = models.TextField(help_text="Text to describe the page", blank=True)
    collection = models.ForeignKey(
        Collection,
        limit_choices_to=~models.Q(name__in=["Root"]),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Select the image collection for this gallery.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("collection"),
    ]

    subpage_types = []
    
    
from django.utils.html import format_html
from wagtail.admin.ui.components import Component

class WelcomePanel(Component):
    def render_html(self, parent_context):
        return format_html("<h1>{}</h1>", "Welcome to my app!")