"""Тести LiqPay інтеграції."""
from django.test import TestCase, override_settings


@override_settings(
    LIQPAY_PUBLIC_KEY="test_public_key",
    LIQPAY_PRIVATE_KEY="test_private_key",
)
class TestLiqPay(TestCase):
    def test_generate_payment_form_data(self):
        from apps.cart.models import Order
        from apps.integrations.liqpay import generate_payment_form_data, verify_callback

        order = Order.objects.create(
            name="Тест",
            phone="+380631234567",
            total_uah=5000,
        )
        data = generate_payment_form_data(order)
        self.assertIn("data", data)
        self.assertIn("signature", data)
        self.assertIn("form_url", data)

    def test_verify_callback_wrong_signature(self):
        from apps.integrations.liqpay import verify_callback
        self.assertFalse(verify_callback("some_data", "wrong_signature"))

    def test_verify_callback_correct_signature(self):
        from apps.integrations.liqpay import _signature, verify_callback
        import base64
        data = base64.b64encode(b'{"test": 1}').decode()
        sig = _signature(data)
        self.assertTrue(verify_callback(data, sig))
