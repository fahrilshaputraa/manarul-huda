from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField

# Import MultiFieldPanel instead of MultipleFieldPanel
from wagtail.admin.panels import MultiFieldPanel, FieldPanel
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import CharBlock, TextBlock, StructBlock

class HomePage(Page):
    # only one home page is allowed
    max_count = 1
    
    # add the hero selection of HomePage
    hero_carousel = models.ForeignKey(
        "wagtailcore.Page", 
        verbose_name=_("Hero Carousel"), 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        related_name='+'
    )
    
    about_us_card = StreamField([
        ("about_us", StructBlock([
            ("title", CharBlock(max_length=50)),
            ("text", TextBlock(max_length=150)),
        ])),
    ],
        use_json_field=True,
        null=True,
        max_num=4,
        min_num=4,
    )
    
    about_us_title = models.CharField(max_length=100, null=True)
    about_us_text = RichTextField(null=True)
    
    # modify the panels using MultiFieldPanel
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("hero_carousel"),
        ], heading="Hero section"),
        MultiFieldPanel([
            FieldPanel("about_us_card"),
            FieldPanel("about_us_title"),
            FieldPanel("about_us_text"),
        ], heading="About Us section"),
    ]
    
