from django.http import HttpResponse
from django.views.decorators.cache import cache_page


@cache_page(3600)
def robots_view(request):
    host = request.build_absolute_uri("/").rstrip("/")
    content = f"""User-agent: *
Disallow: /admin/
Disallow: /cart/
Disallow: /checkout/
Disallow: /leads/
Disallow: /search/
Disallow: /*?sort=
Disallow: /*?page=
Disallow: /*&page=
Allow: /static/
Allow: /media/
Sitemap: {host}/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")


def sitemap_index_view(request):
    from django.template.response import TemplateResponse
    sections = ["pages", "categories", "products", "blog"]
    host = request.build_absolute_uri("/").rstrip("/")
    return TemplateResponse(
        request,
        "seo/sitemap_index.xml",
        {"sections": sections, "host": host},
        content_type="application/xml",
    )


def sitemap_section_view(request, section):
    from django.template.response import TemplateResponse

    context = {"host": request.build_absolute_uri("/").rstrip("/")}

    if section == "pages":
        from apps.content.models.page import StaticPage
        context["items"] = StaticPage.objects.all()
        template = "seo/sitemap_pages.xml"
    elif section == "categories":
        from apps.catalog.models.facet import Facet, Section
        context["sections"] = Section.objects.filter(is_active=True)
        context["facets"] = Facet.objects.filter(is_indexable=True)
        template = "seo/sitemap_categories.xml"
    elif section == "products":
        from apps.catalog.models.series import ProductSeries
        context["items"] = ProductSeries.objects.filter(is_active=True).select_related("section")
        template = "seo/sitemap_products.xml"
    elif section == "blog":
        from apps.content.models.article import Article
        context["items"] = Article.objects.filter(is_published=True)
        template = "seo/sitemap_blog.xml"
    else:
        return HttpResponse("Not found", status=404)

    return TemplateResponse(request, template, context, content_type="application/xml")
