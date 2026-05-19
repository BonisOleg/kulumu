from django.db.models import Min, Prefetch, Q

from .models.facet import Facet, FacetType, Section
from .models.media import ProductImage
from .models.series import ProductSeries
from .models.variant import ProductVariant

def get_active_sections():
    return Section.objects.filter(is_active=True).order_by("sort_order")


def get_section_by_slug(slug):
    return Section.objects.filter(slug=slug, is_active=True).first()


def get_facets_by_type(facet_type):
    return Facet.objects.filter(type=facet_type).order_by("sort_order", "name")


def get_filtered_series(section=None, facet_slugs=None, price_min=None, price_max=None, sort="default"):
    """
    Основний query для каталогу з фільтрацією та prefetch.
    Логіка фасетів: OR всередині одного типу, AND між різними типами.
    """
    qs = ProductSeries.objects.filter(is_active=True)

    if section:
        qs = qs.filter(section=section)

    if facet_slugs:
        selected = list(
            Facet.objects.filter(slug__in=facet_slugs).values_list("slug", "type")
        )
        type_groups: dict = {}
        for slug, ftype in selected:
            type_groups.setdefault(ftype, []).append(slug)
        for slugs_in_type in type_groups.values():
            qs = qs.filter(facets__slug__in=slugs_in_type)

    if price_min is not None or price_max is not None:
        price_q = Q(variants__in_stock=True)
        if price_min is not None:
            price_q &= Q(variants__price_uah__gte=price_min)
        if price_max is not None:
            price_q &= Q(variants__price_uah__lte=price_max)
        qs = qs.filter(price_q)

    # Мінімальна ціна на картці / сортування: ті самі умови, що й для фільтра діапазону
    # (якщо діапазон задано — рахуємо Min лише серед варіантів у межах, інакше — усі in_stock)
    ann_variant_filter = Q(variants__in_stock=True)
    if price_min is not None:
        ann_variant_filter &= Q(variants__price_uah__gte=price_min)
    if price_max is not None:
        ann_variant_filter &= Q(variants__price_uah__lte=price_max)

    qs = qs.annotate(
        min_price_ann=Min("variants__price_uah", filter=ann_variant_filter),
    )

    sort_map = {
        "price_asc": "min_price_ann",
        "price_desc": "-min_price_ann",
        "new": "-is_new",
        "top": "-is_top",
        "default": ["-is_top", "-is_new", "name"],
    }
    ordering = sort_map.get(sort, ["-is_top", "-is_new", "name"])
    if isinstance(ordering, list):
        qs = qs.order_by(*ordering)
    else:
        qs = qs.order_by(ordering)

    primary_images = Prefetch(
        "images",
        queryset=ProductImage.objects.filter(is_primary=True),
        to_attr="primary_images",
    )
    in_stock_variants = Prefetch(
        "variants",
        queryset=ProductVariant.objects.filter(in_stock=True).only("id", "series_id"),
        to_attr="in_stock_variants",
    )
    qs = qs.select_related("section").prefetch_related(primary_images, in_stock_variants, "facets")

    return qs.distinct()


def get_series_detail(section_slug, series_slug):
    return (
        ProductSeries.objects.filter(
            slug=series_slug,
            section__slug=section_slug,
            is_active=True,
        )
        .select_related("section")
        .prefetch_related(
            "images",
            "variants__color",
            "variants__size",
            "facets",
        )
        .first()
    )


def get_related_series(series, count=6):
    """Схожі товари: той самий розділ + спільні фасети."""
    facet_ids = series.facets.values_list("id", flat=True)
    return (
        ProductSeries.objects.filter(is_active=True, section=series.section)
        .filter(facets__in=facet_ids)
        .exclude(pk=series.pk)
        .distinct()
        .annotate(
            min_price_ann=Min("variants__price_uah", filter=Q(variants__in_stock=True))
        )
        .prefetch_related(
            Prefetch("images", queryset=ProductImage.objects.filter(is_primary=True), to_attr="primary_images"),
            Prefetch("variants", queryset=ProductVariant.objects.filter(in_stock=True).only("id", "series_id"), to_attr="in_stock_variants"),
        )
        .order_by("-is_top", "name")[:count]
    )


def get_top_facets_for_footer(count=30):
    """Топ-фасети для footer-посилань (по кількості активних серій)."""
    from django.db.models import Count

    return (
        Facet.objects.filter(is_indexable=True)
        .annotate(series_count=Count("series", filter=Q(series__is_active=True)))
        .filter(series_count__gt=0)
        .order_by("-series_count")[:count]
    )
