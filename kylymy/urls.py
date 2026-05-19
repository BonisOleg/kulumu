from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.i18n import JavaScriptCatalog

from apps.seo.views import robots_view, sitemap_index_view, sitemap_section_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tinymce/", include("tinymce.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    # SEO static files
    path("robots.txt", robots_view, name="robots"),
    path("sitemap.xml", sitemap_index_view, name="sitemap_index"),
    path("sitemap-<str:section>.xml", sitemap_section_view, name="sitemap_section"),
]

urlpatterns += i18n_patterns(
    # Специфічні маршрути ПЕРЕД каталогом (щоб не перехоплювались <slug:section_slug>/)
    path("blog/", include("apps.content.urls")),
    path("leads/", include("apps.leads.urls")),
    path("cart/", include("apps.cart.urls")),
    # Каталог — catch-all, завжди ОСТАННІМ
    path("", include("apps.catalog.urls")),
    prefix_default_language=False,
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
