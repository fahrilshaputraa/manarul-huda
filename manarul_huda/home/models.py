from django.db import models

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField

# Import MultiFieldPanel instead of MultipleFieldPanel
from wagtail.admin.panels import MultiFieldPanel, FieldPanel
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import CharBlock, TextBlock, StructBlock, PageChooserBlock, URLBlock
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import PageChooserPanel, InlinePanel
from django.core.exceptions import ValidationError
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Collection
from wagtailmetadata.models import MetadataPageMixin

class HomePage(MetadataPageMixin, Page):
    # only one home page is allowed
    max_count = 1
    
    about_us_card = StreamField([
        ("about_us", StructBlock([
            ("title", CharBlock(max_length=50)),
            ("icon", ImageChooserBlock(required=False, help_text="Icon to display before the title")),
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
    featured_section_title = models.CharField(
        blank=True, max_length=255, help_text="Title to display above the promo copy"
    )
    featured_section = models.ForeignKey(
        "blogpages.BlogPage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="First featured section for the homepage. Will display latest "
        "blog posts.",
        verbose_name="Featured section",
    )
    cta_selection = StreamField([
        ("cta_button", StructBlock([
            ("title", CharBlock(max_length=50)),
            ("icon", ImageChooserBlock(required=False, help_text="Icon to display before the title")),
            ("link", PageChooserBlock(required=False)),
            ("external_link", URLBlock(required=False)),
        ])),
    ],
        use_json_field=True,
        null=True,
    )
    
    collection = models.ForeignKey(
        Collection,
        limit_choices_to=~models.Q(name__in=["Root"]),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Select the image collection for this carousel.",
    )
     
    collection_introduction = models.TextField(help_text="Text to describe the page", blank=True)
    
    collection_link = models.ForeignKey(
        "base.Gallery",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def get_featured_posts(self):
        if self.featured_section:
            return self.featured_section.get_children().live().public().order_by('-first_published_at')
        return None
    
    def clean(self):
        super().clean()
        for block in self.cta_selection:
            if not (bool(block.value['link']) ^ bool(block.value['external_link'])):
                raise ValidationError({'cta_selection': "Please choose exactly one: internal link or external link"})
            icon = block.value.get('icon')
            if icon and not icon.filename.lower().endswith('.svg'):
                raise ValidationError({'cta_selection': "Icon must be an SVG file"})

    # modify the panels using MultiFieldPanel
    content_panels = Page.content_panels + [
        InlinePanel("carousel_items", label="Carousel Items", max_num=5),
        MultiFieldPanel([
            FieldPanel("featured_section_title"),
            FieldPanel("featured_section"),
        ], heading="Featured Section"),
        MultiFieldPanel([
            FieldPanel("cta_selection"),
        ], heading="CTA Selection"),
        MultiFieldPanel([
            FieldPanel("about_us_card"),
            FieldPanel("about_us_title"),
            FieldPanel("about_us_text"),
        ], heading="About Us section"),
        MultiFieldPanel([
            FieldPanel("collection_introduction"),
            FieldPanel("collection"),
            FieldPanel("collection_link"),
        ], heading="Carousel Collection"),
    ]
    
class CarouselItem(Orderable):
    page = ParentalKey(
        "HomePage",
        related_name="carousel_items",
        on_delete=models.CASCADE,
    )
    
    link_page = models.ForeignKey(
        "blogpages.BlogPageDetail",
        verbose_name=_("Link Page"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    
    panels = [
        PageChooserPanel(
            "link_page",
        ),
    ]