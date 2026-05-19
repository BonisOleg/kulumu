"""Тести selectors (query-логіка)."""
from django.test import TestCase


class TestGetFilteredSeries(TestCase):
    def setUp(self):
        from apps.catalog.models import Facet, ProductSeries, Section
        self.section = Section.objects.create(slug="kylymy", name="Килими", sort_order=0)
        self.facet = Facet.objects.create(type="category", slug="shaggy", name="Shaggy")
        self.s1 = ProductSeries.objects.create(
            section=self.section, slug="s1", name="Carpet 1", is_active=True, is_top=True
        )
        self.s1.facets.add(self.facet)
        self.s2 = ProductSeries.objects.create(
            section=self.section, slug="s2", name="Carpet 2", is_active=True
        )

    def test_returns_only_active(self):
        from apps.catalog.selectors import get_filtered_series
        qs = get_filtered_series()
        self.assertEqual(qs.count(), 2)

    def test_filter_by_section(self):
        from apps.catalog.selectors import get_filtered_series
        qs = get_filtered_series(section=self.section)
        self.assertEqual(qs.count(), 2)

    def test_filter_by_facet(self):
        from apps.catalog.selectors import get_filtered_series
        qs = get_filtered_series(facet_slugs=["shaggy"])
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first().slug, "s1")

    def test_inactive_excluded(self):
        from apps.catalog.models import ProductSeries
        from apps.catalog.selectors import get_filtered_series
        ProductSeries.objects.create(
            section=self.section, slug="s3", name="Inactive", is_active=False
        )
        qs = get_filtered_series()
        self.assertFalse(qs.filter(slug="s3").exists())


class TestGetFilteredSeriesPriceFilter(TestCase):
    """Ціновий діапазон + min_price_ann узгоджені між собою."""

    def setUp(self):
        from apps.catalog.models import Facet, ProductSeries, ProductVariant, Section

        self.section = Section.objects.create(slug="kylymy", name="Килими", sort_order=0)
        self.color = Facet.objects.create(type="color", slug="c-red", name="Червоний")
        self.series = ProductSeries.objects.create(
            section=self.section,
            slug="dual-price",
            name="Дві ціни",
            is_active=True,
        )
        ProductVariant.objects.create(
            series=self.series,
            sku="dual-a",
            color=self.color,
            width_cm=200,
            length_cm=300,
            price_uah=3000,
            in_stock=True,
        )
        ProductVariant.objects.create(
            series=self.series,
            sku="dual-b",
            color=self.color,
            width_cm=250,
            length_cm=300,
            price_uah=8000,
            in_stock=True,
        )

    def test_without_price_filter_min_is_global_in_stock(self):
        from apps.catalog.selectors import get_filtered_series

        row = get_filtered_series(section=self.section).filter(pk=self.series.pk).first()
        self.assertEqual(row.min_price_ann, 3000)

    def test_with_price_filter_min_only_within_range(self):
        from apps.catalog.selectors import get_filtered_series

        qs = get_filtered_series(section=self.section, price_min=5000)
        self.assertTrue(qs.filter(pk=self.series.pk).exists())
        row = qs.filter(pk=self.series.pk).first()
        self.assertEqual(row.min_price_ann, 8000)

    def test_price_range_excludes_series_with_no_variant_in_band(self):
        from apps.catalog.selectors import get_filtered_series

        qs = get_filtered_series(section=self.section, price_min=9000, price_max=9500)
        self.assertFalse(qs.filter(pk=self.series.pk).exists())
