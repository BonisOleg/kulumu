from django.http import Http404
from django.template.response import TemplateResponse
from django.views.generic import DetailView

from apps.catalog.models.series import ProductSeries
from apps.catalog.models.variant import ProductVariant
from apps.catalog.selectors import get_related_series, get_series_detail
from apps.catalog.services.recently_viewed import add_to_recently_viewed, get_recently_viewed


class SeriesView(DetailView):
    template_name = "catalog/series.html"
    context_object_name = "series"

    def get_object(self, queryset=None):
        obj = get_series_detail(
            section_slug=self.kwargs["section_slug"],
            series_slug=self.kwargs["series_slug"],
        )
        if not obj:
            raise Http404
        return obj

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        add_to_recently_viewed(request, self.object.pk)
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        series = self.object
        recently_viewed_ids = get_recently_viewed(self.request, exclude_pk=series.pk)

        ctx.update(
            {
                "related_series": get_related_series(series, count=6),
                "recently_viewed_ids": recently_viewed_ids,
                "page_title": series.get_seo_title(),
                "page_description": series.get_seo_description(),
                "breadcrumbs": [
                    ("Головна", "/"),
                    (series.section.name, series.section.get_absolute_url()),
                    (series.name, None),
                ],
                "all_colors": series.variants.values(
                    "color__id", "color__name", "color__color_hex"
                ).distinct().order_by("color__sort_order"),
                "all_sizes": series.variants.values(
                    "id", "width_cm", "length_cm", "price_uah",
                    "old_price_uah", "in_stock", "is_per_meter",
                ).order_by("width_cm", "length_cm"),
                "selected_variant": series.variants.filter(in_stock=True).first(),
            }
        )
        return ctx


def htmx_variant_view(request, series_id):
    """HTMX: перерендерити блок ціни/наявності при зміні кольору чи розміру."""
    try:
        series = ProductSeries.objects.get(pk=series_id, is_active=True)
    except ProductSeries.DoesNotExist:
        raise Http404

    variant_id = request.GET.get("variant")
    variant = None
    if variant_id:
        try:
            variant = series.variants.filter(pk=int(variant_id)).first()
        except (ValueError, TypeError):
            variant = None

    if variant is None:
        color_id = request.GET.get("color")
        width_cm = request.GET.get("width")
        length_cm = request.GET.get("length")

        qs = series.variants.all()
        if color_id:
            qs = qs.filter(color_id=color_id)
        if width_cm:
            qs = qs.filter(width_cm=width_cm)
        if length_cm:
            qs = qs.filter(length_cm=length_cm)

        variant = qs.first()

    return TemplateResponse(
        request,
        "catalog/partials/variant_block.html",
        {"series": series, "variant": variant},
    )


def htmx_per_meter_calc_view(request, series_id):
    """HTMX: розрахунок ціни доріжки на відріз."""
    width_cm = request.GET.get("width_cm")
    length_m = request.GET.get("length_m")

    try:
        variant = ProductVariant.objects.filter(
            series_id=series_id, is_per_meter=True, width_cm=width_cm
        ).first()
        length_m = float(length_m) if length_m else 1.0
        price = int(variant.price_uah * length_m) if variant else 0
    except (TypeError, ValueError):
        price = 0
        variant = None

    return TemplateResponse(
        request,
        "catalog/partials/calc_result.html",
        {"variant": variant, "length_m": length_m, "total_price": price},
    )
