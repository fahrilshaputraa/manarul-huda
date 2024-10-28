from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField

# Import MultiFieldPanel instead of MultipleFieldPanel
from wagtail.admin.panels import MultiFieldPanel, FieldPanel


class HomePage(Page):
    # add the hero selection of HomePage
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Home page image",
    )
    hero_text = models.CharField(max_length=255, blank=True, help_text="Write a short text for the hero section")
    hero_cta = models.CharField(max_length=255, blank=True, verbose_name="Hero CTA text", help_text="CTA for the hero section")
    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Hero CTA link",
        help_text="CTA a page link to for the call to action",
    )
    
    body = RichTextField(blank=True)
    
    # modify the panels using MultiFieldPanel
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("image"),
            FieldPanel("hero_text"),
            FieldPanel("hero_cta"),
            FieldPanel("hero_cta_link"),
        ], heading="Hero section"),
        FieldPanel("body"),
    ]
    
