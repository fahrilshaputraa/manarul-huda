from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from wagtail.contrib.sitemaps import Sitemap

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from comments import views as comment_views

sitemaps = {
    'pages': Sitemap,
}

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}),
    # Override default django_comments URLs with our custom views
    path("comments/post/", comment_views.post_comment, name="comments-post-comment"),
    path("comments/", include("django_comments.urls")),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by the above patterns, fall back to the Wagtail page serving mechanism
    path("", include(wagtail_urls)),
]
