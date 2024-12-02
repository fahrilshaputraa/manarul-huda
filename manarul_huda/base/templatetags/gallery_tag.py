from django import template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.images.models import Image

register = template.Library()


# Retrieves a single gallery item and returns a gallery of images
@register.inclusion_tag("includes/tags/gallery.html", takes_context=True)
def gallery(context, gallery):
    images = Image.objects.filter(collection=gallery)

    return {
        "images": images,
        "request": context["request"],
    }

@register.inclusion_tag("includes/tags/gallery_tag.html", takes_context=True)
def gallery_tag(context, gallery):
    request = context['request']
    images = Image.objects.filter(collection=gallery).order_by('id')
    
    # Get the page number from the request
    page = request.GET.get('page', 1)
    items_per_page = 12  # Jumlah gambar yang ditampilkan per load
    
    paginator = Paginator(images, items_per_page)
    
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)

    return {
        "images": images,
        "request": request,
        "has_more": images.has_next(),
        "next_page": int(page) + 1,
    }

