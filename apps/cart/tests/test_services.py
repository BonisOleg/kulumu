"""Тести кошика."""
from django.test import TestCase, RequestFactory


class TestCartServices(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        from apps.catalog.models import Facet, ProductSeries, ProductVariant, Section
        self.section = Section.objects.create(slug="kylymy", name="Килими", sort_order=0)
        self.color = Facet.objects.create(type="color", slug="siryi", name="Сірий")
        self.series = ProductSeries.objects.create(
            section=self.section, slug="test-carpet", name="Test Carpet"
        )
        self.variant = ProductVariant.objects.create(
            series=self.series,
            sku="TC-001",
            color=self.color,
            width_cm=160,
            length_cm=230,
            price_uah=3000,
            in_stock=True,
        )

    def _make_request(self):
        from django.contrib.sessions.backends.db import SessionStore
        request = self.factory.get("/")
        request.session = SessionStore()
        return request

    def test_add_to_cart(self):
        from apps.cart.services import add_to_cart, get_cart
        request = self._make_request()
        add_to_cart(request, self.variant.pk, qty=2)
        cart = get_cart(request)
        self.assertIn(str(self.variant.pk), cart)
        self.assertEqual(cart[str(self.variant.pk)]["qty"], 2)

    def test_remove_from_cart(self):
        from apps.cart.services import add_to_cart, remove_from_cart, get_cart
        request = self._make_request()
        add_to_cart(request, self.variant.pk)
        remove_from_cart(request, self.variant.pk)
        self.assertNotIn(str(self.variant.pk), get_cart(request))

    def test_get_cart_total(self):
        from apps.cart.services import add_to_cart, get_cart_total
        request = self._make_request()
        add_to_cart(request, self.variant.pk, qty=2)
        total = get_cart_total(request)
        self.assertEqual(total, 6000)


class TestCheckoutView(TestCase):
    def test_checkout_redirects_when_empty(self):
        response = self.client.get("/cart/checkout/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/cart/", fetch_redirect_response=False)
