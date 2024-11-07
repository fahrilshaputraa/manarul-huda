from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
import re

class BlogPage(Page):
    template = "blogpages/blog_page.html"
    # parent_page_types = ["home.HomePage"]
    
    subtitle = models.CharField(max_length=255,
                                help_text=_("Subtitle of the blog page"),
                                verbose_name=_("Subtitle"),
                                blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
    ]
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["blog_pages"] = BlogPageDetail.objects.child_of(self).live().public().order_by("-created_at")
        
        return context

class BlogPageDetail(Page):
    parent_page_types = ["BlogPage"]
    subpage_types = []
    
    subtitle = models.CharField(max_length=255,
                                help_text=_("Subtitle of the blog detail page"),
                                verbose_name=_("Subtitle"),
                                blank=True)
    
    blog_image = models.ForeignKey("wagtailimages.Image",
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True,
                                  verbose_name=_("Blog image"))
    body = RichTextField(blank=True, 
                         verbose_name=_("Body"),
                         help_text=_("Body of the blog detail page"))
    created_at = models.DateTimeField(auto_now_add=True, 
                                     verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, 
                                      verbose_name=_("Updated at"))


    content_panels = Page.content_panels + [
        FieldPanel("blog_image"),
        FieldPanel("body", classname="full"),
    ]

    def clean(self):
        # Cari isi dari tag <p> pertama di self.body
        match = re.search(r'<p[^>]*>(.*?)<\/p>', self.body, re.DOTALL)
        
        # Ambil teks dari <p> pertama atau langsung dari body kalau gak ada <p>
        text = match.group(1).strip() if match else self.body.strip()
        
        # Potong di 250 karakter, lalu cek spasi terakhir untuk kata utuh
        truncated = text[:250]
        self.subtitle = truncated.rsplit(" ", 1)[0] if len(text) > 250 else text


class BlogPageDetailV2(BlogPageDetail):
    template = "blogpages/blog_page_detail_v2.html"
