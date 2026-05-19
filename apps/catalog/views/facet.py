from django.http import Http404
from django.views.generic import ListView

from apps.catalog.filters import CatalogFilter
from apps.catalog.models.facet import Facet, FacetType
from apps.catalog.selectors import get_facets_by_type, get_filtered_series, get_section_by_slug


class FacetView(ListView):
    template_name = "catalog/facet.html"
    context_object_name = "series_list"
    paginate_by = 24

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.section = get_section_by_slug(kwargs["section_slug"])
        if not self.section:
            raise Http404

        self.facet1 = self._get_facet(kwargs.get("f1") or kwargs.get("facet_slug"))
        self.facet2 = self._get_facet(kwargs.get("f2"))
        self.catalog_filter = CatalogFilter.from_request(request)

        active_slugs = [f.slug for f in [self.facet1, self.facet2] if f]
        self.catalog_filter.facet_slugs = list(set(active_slugs + self.catalog_filter.facet_slugs))

    def _get_facet(self, slug):
        if not slug:
            return None
        return Facet.objects.filter(slug=slug).first()

    def get_queryset(self):
        return get_filtered_series(
            section=self.section,
            facet_slugs=self.catalog_filter.facet_slugs,
            price_min=self.catalog_filter.price_min,
            price_max=self.catalog_filter.price_max,
            sort=self.catalog_filter.sort,
        )

    def get_template_names(self):
        if self.request.htmx:
            return ["catalog/partials/product_grid.html"]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        facet_name = self.facet1.name if self.facet1 else self.section.name
        page_title = f"{facet_name} — купити в Україні | Kylymy"

        facet_description = (self.facet1.seo_description if self.facet1 else "") or ""
        ctx.update(
            {
                "section": self.section,
                "facet1": self.facet1,
                "facet2": self.facet2,
                "catalog_filter": self.catalog_filter,
                "facets_by_type": {
                    ft.value: get_facets_by_type(ft.value)
                    for ft in FacetType
                },
                "page_title": page_title,
                "page_description": facet_description,
                "total_count": ctx["paginator"].count,
                "breadcrumbs": self._build_breadcrumbs(),
                "is_noindex": bool(self.catalog_filter.facet_slugs) and not (self.facet1 and self.facet1.is_indexable),
            }
        )
        return ctx

    def _build_breadcrumbs(self):
        crumbs = [("Головна", "/"), (self.section.name, self.section.get_absolute_url())]
        if self.facet1:
            if self.facet2:
                crumbs.append((self.facet1.name, None))
                crumbs.append((self.facet2.name, None))
            else:
                crumbs.append((self.facet1.name, None))
        return crumbs


def htmx_filter_view(request, section_slug):
    """HTMX partial — повертає grid + pagination без перезавантаження сторінки."""
    from django.core.paginator import Paginator
    from django.template.response import TemplateResponse
    from django.urls import reverse

    section = get_section_by_slug(section_slug)
    if not section:
        raise Http404

    catalog_filter = CatalogFilter.from_request(request)
    qs = get_filtered_series(
        section=section,
        facet_slugs=catalog_filter.facet_slugs,
        price_min=catalog_filter.price_min,
        price_max=catalog_filter.price_max,
        sort=catalog_filter.sort,
    )

    paginator = Paginator(qs, catalog_filter.per_page)
    page_obj = paginator.get_page(catalog_filter.page)

    response = TemplateResponse(
        request,
        "catalog/partials/product_grid.html",
        {
            "series_list": page_obj.object_list,
            "page_obj": page_obj,
            "section": section,
            "catalog_filter": catalog_filter,
            "total_count": paginator.count,
            "is_htmx": True,
        },
    )

    # URL у браузері: той самий шлях сторінки (розділ / фасет), не endpoint HTMX
    from urllib.parse import urlparse

    params = request.GET.copy()
    params.pop("page", None)
    query = params.urlencode()

    push_path = None
    current = request.headers.get("HX-Current-URL") or request.headers.get("Hx-Current-Url")
    if current:
        try:
            parsed = urlparse(current)
            path = parsed.path or ""
            if path.startswith("/") and ".." not in path:
                push_path = path
        except (TypeError, ValueError):
            push_path = None

    if not push_path:
        push_path = reverse("catalog:section", kwargs={"section_slug": section_slug})

    push_url = f"{push_path}?{query}" if query else push_path
    response["HX-Push-Url"] = push_url

    return response
