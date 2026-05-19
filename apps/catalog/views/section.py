from django.http import Http404
from django.views.generic import ListView

from apps.catalog.filters import CatalogFilter
from apps.catalog.models.facet import FacetType
from apps.catalog.selectors import get_facets_by_type, get_filtered_series, get_section_by_slug


class SectionView(ListView):
    template_name = "catalog/section.html"
    context_object_name = "series_list"
    paginate_by = 24

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.section = get_section_by_slug(kwargs["section_slug"])
        if not self.section:
            raise Http404
        self.catalog_filter = CatalogFilter.from_request(request)

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
        ctx.update(
            {
                "section": self.section,
                "catalog_filter": self.catalog_filter,
                "facets_by_type": {
                    ft.value: get_facets_by_type(ft.value)
                    for ft in [FacetType.CATEGORY, FacetType.PURPOSE, FacetType.STYLE, FacetType.FORM]
                },
                "page_title": self.section.get_seo_title(),
                "page_description": self.section.seo_description or "",
                "total_count": ctx["paginator"].count,
                "breadcrumbs": [("Головна", "/"), (self.section.name, None)],
            }
        )
        return ctx
