"""Smoke-тести views каталогу."""
import pytest
from django.test import TestCase
from django.urls import reverse


class TestHomeView(TestCase):
    def test_home_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/home.html")


class TestSectionView(TestCase):
    def setUp(self):
        from apps.catalog.models import Section
        self.section = Section.objects.create(slug="kylymy", name="Килими", sort_order=0, is_active=True)

    def test_section_200(self):
        response = self.client.get("/kylymy/")
        self.assertEqual(response.status_code, 200)

    def test_section_404(self):
        response = self.client.get("/nonexistent-section/")
        self.assertEqual(response.status_code, 404)


class TestRobotsTxt(TestCase):
    def test_robots_txt(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User-agent", response.content)
        self.assertIn(b"/admin/", response.content)

    def test_robots_content_type(self):
        response = self.client.get("/robots.txt")
        self.assertIn("text/plain", response.get("Content-Type", ""))


class TestSitemapIndex(TestCase):
    def test_sitemap_xml(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"sitemapindex", response.content)


class TestSearchView(TestCase):
    def test_search_empty(self):
        response = self.client.get("/search/")
        self.assertEqual(response.status_code, 200)

    def test_search_with_query(self):
        response = self.client.get("/search/?q=kilym")
        self.assertEqual(response.status_code, 200)


class TestHtmxVariantById(TestCase):
    """GET ?variant=<pk> має повертати ціну саме цього варіанту (клік по розміру на сторінці серії)."""

    def setUp(self):
        from apps.catalog.models import Facet, ProductSeries, ProductVariant, Section

        self.section = Section.objects.create(slug="kylymy", name="Килими", sort_order=0)
        self.color = Facet.objects.create(type="color", slug="c1", name="Колір 1")
        self.series = ProductSeries.objects.create(
            section=self.section, slug="s1", name="Серія", is_active=True
        )
        self.v1 = ProductVariant.objects.create(
            series=self.series,
            sku="SKU-SMALL",
            color=self.color,
            width_cm=80,
            length_cm=150,
            price_uah=780,
            in_stock=True,
        )
        self.v2 = ProductVariant.objects.create(
            series=self.series,
            sku="SKU-LARGE",
            color=self.color,
            width_cm=200,
            length_cm=300,
            price_uah=3900,
            in_stock=True,
        )

    def test_variant_query_returns_matching_price(self):
        url = reverse("catalog:htmx_variant", kwargs={"series_id": self.series.pk})
        r = self.client.get(url, {"variant": str(self.v2.pk)})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "3\u00a0900")
        self.assertNotContains(r, "780")

    def test_invalid_variant_falls_back_to_color_filters(self):
        url = reverse("catalog:htmx_variant", kwargs={"series_id": self.series.pk})
        r = self.client.get(url, {"variant": "999999", "color": str(self.color.pk)})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "780")
