from django.db.models import Q
from django.views.generic import ListView

from apps.catalog.models.series import ProductSeries
from apps.catalog.selectors import get_filtered_series


class SearchView(ListView):
    template_name = "catalog/search.html"
    context_object_name = "series_list"
    paginate_by = 24

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        if not query or len(query) < 2:
            return ProductSeries.objects.none()
        return (
            get_filtered_series()
            .filter(
                Q(name__icontains=query)
                | Q(short_descr__icontains=query)
                | Q(variants__sku__icontains=query)
            )
            .distinct()
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "")
        ctx.update(
            {
                "query": query,
                "total_count": ctx["paginator"].count,
                "page_title": f'Пошук: "{query}" | Kylymy',
            }
        )
        return ctx
