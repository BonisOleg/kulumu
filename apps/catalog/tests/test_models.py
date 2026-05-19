"""Тести моделей каталогу."""
import pytest
from django.test import TestCase


class TestSection(TestCase):
    def test_section_str(self):
        from apps.catalog.models import Section
        s = Section.objects.create(slug="test", name="Тест", sort_order=0)
        assert str(s) == "Тест"

    def test_section_absolute_url(self):
        from apps.catalog.models import Section
        s = Section.objects.create(slug="kylymy", name="Килими", sort_order=0)
        assert s.get_absolute_url() == "/kylymy/"


class TestFacet(TestCase):
    def test_facet_str(self):
        from apps.catalog.models import Facet
        f = Facet.objects.create(type="category", slug="shaggy", name="Shaggy")
        assert "Shaggy" in str(f)
        assert "Тип / матеріал" in str(f)


class TestProductSeries(TestCase):
    def setUp(self):
        from apps.catalog.models import Section
        self.section = Section.objects.create(slug="kylymy", name="Килими", sort_order=0)

    def test_series_str(self):
        from apps.catalog.models import ProductSeries
        s = ProductSeries.objects.create(
            section=self.section, slug="shaggy-roco", name="Shaggy Roco"
        )
        assert str(s) == "Shaggy Roco"

    def test_series_min_price_zero_no_variants(self):
        from apps.catalog.models import ProductSeries
        s = ProductSeries.objects.create(
            section=self.section, slug="test-empty", name="Empty"
        )
        assert s.min_price == 0

    def test_series_seo_title_generated(self):
        from apps.catalog.models import ProductSeries
        s = ProductSeries.objects.create(
            section=self.section, slug="auto-seo", name="Test Carpet"
        )
        title = s.get_seo_title()
        assert "Test Carpet" in title
        assert "Kylymy" in title

    def test_series_slug_auto_generated(self):
        from apps.catalog.models import ProductSeries
        s = ProductSeries(section=self.section, name="Auto Slug Test")
        s.save()
        assert s.slug == "auto-slug-test"


class TestProductVariant(TestCase):
    def setUp(self):
        from apps.catalog.models import Facet, Section, ProductSeries
        self.section = Section.objects.create(slug="kylymy", name="Килими", sort_order=0)
        self.color = Facet.objects.create(type="color", slug="siryi", name="Сірий")
        self.series = ProductSeries.objects.create(
            section=self.section, slug="shaggy-v", name="Shaggy"
        )

    def test_variant_size_display(self):
        from apps.catalog.models import ProductVariant
        v = ProductVariant.objects.create(
            series=self.series,
            sku="TEST-001",
            color=self.color,
            width_cm=160,
            length_cm=230,
            price_uah=5000,
        )
        assert v.size_display == "1.6×2.3 м"

    def test_variant_per_meter_display(self):
        from apps.catalog.models import ProductVariant
        v = ProductVariant.objects.create(
            series=self.series,
            sku="TEST-002",
            color=self.color,
            width_cm=100,
            is_per_meter=True,
            price_uah=500,
        )
        assert "на відріз" in v.size_display

    def test_variant_discount_percent(self):
        from apps.catalog.models import ProductVariant
        v = ProductVariant.objects.create(
            series=self.series,
            sku="TEST-003",
            color=self.color,
            width_cm=80,
            length_cm=150,
            price_uah=850,
            old_price_uah=1000,
        )
        assert v.discount_percent == 15
