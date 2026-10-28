from coderedcms import admin_urls as crx_admin_urls
from coderedcms import search_urls as crx_search_urls
from coderedcms import urls as crx_urls
from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path
from wagtail.documents import urls as wagtaildocs_urls
from django.conf.urls.i18n import i18n_patterns
from website.models import InstagramPostPage

urlpatterns = [
    # Other URL patterns
]


urlpatterns = [
    # Admin
    path("django-admin/", admin.site.urls),
    path("admin/", include(crx_admin_urls)),
    # Documents
    path("docs/", include(wagtaildocs_urls)),
    # Search
    path("search/", include(crx_search_urls)),
    path('rosetta/', include('rosetta.urls')),  # Add Rosetta
    # For anything not caught by a more specific rule above, hand over to
    # the page serving mechanism. This should be the last pattern in
    # the list:
    # Alternatively, if you want pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(crx_urls)),
    path('get_post_content/<int:post_id>/', InstagramPostPage.get_post_content, name='get_post_content'),
]

urlpatterns += i18n_patterns(
    path("", include(crx_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath of your site:
    # path("pages/", include(wagtail_urls)),
)
# fmt: off
if settings.DEBUG:
    from django.conf.urls.static import static

    # Serve static and media files from development server
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # type: ignore
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # type: ignore
# fmt: on

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

# Local-only preview serves media from the isolated preview filesystem.
# Public deployments must use the web server / storage backend instead.
if getattr(settings, "IS_LOCAL_PREVIEW", False):
    from django.urls import re_path
    from django.views.static import serve as serve_local_media

    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve_local_media,
                {"document_root": settings.MEDIA_ROOT}),
    ]
