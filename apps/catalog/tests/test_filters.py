"""Тести нормалізації query-параметрів каталогу."""
from django.test import RequestFactory, SimpleTestCase

from apps.catalog.filters import CatalogFilter


class TestCatalogFilterPrice(SimpleTestCase):
    def test_swaps_min_max_when_inverted(self):
        req = RequestFactory().get("/x/", {"price_min": "9000", "price_max": "1000"})
        f = CatalogFilter.from_request(req)
        self.assertEqual(f.price_min, 1000)
        self.assertEqual(f.price_max, 9000)

    def test_negative_prices_dropped(self):
        req = RequestFactory().get("/x/", {"price_min": "-10", "price_max": "5000"})
        f = CatalogFilter.from_request(req)
        self.assertIsNone(f.price_min)
        self.assertEqual(f.price_max, 5000)

    def test_zero_min_is_kept(self):
        req = RequestFactory().get("/x/", {"price_min": "0", "price_max": "10000"})
        f = CatalogFilter.from_request(req)
        self.assertEqual(f.price_min, 0)
        self.assertEqual(f.price_max, 10000)
