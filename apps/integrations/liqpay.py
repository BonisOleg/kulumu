"""Інтеграція з LiqPay."""
import base64
import hashlib
import json
import logging

from django.conf import settings

logger = logging.getLogger(__name__)


def _signature(data: str) -> str:
    private_key = settings.LIQPAY_PRIVATE_KEY
    raw = private_key + data + private_key
    return base64.b64encode(hashlib.sha1(raw.encode()).digest()).decode()


def generate_payment_form_data(order) -> dict:
    params = {
        "public_key": settings.LIQPAY_PUBLIC_KEY,
        "version": "3",
        "action": "pay",
        "amount": str(order.total_uah),
        "currency": "UAH",
        "description": f"Замовлення #{order.pk} — Kylymy",
        "order_id": f"kylymy-{order.pk}",
        "result_url": f"{settings.SITE_URL}/cart/success/{order.pk}/",
        "server_url": f"{settings.SITE_URL}/payments/liqpay/callback/",
    }
    data_b64 = base64.b64encode(json.dumps(params).encode()).decode()
    return {
        "data": data_b64,
        "signature": _signature(data_b64),
        "form_url": "https://www.liqpay.ua/api/3/checkout",
    }


def verify_callback(data: str, signature: str) -> bool:
    return _signature(data) == signature


def decode_callback_data(data: str) -> dict:
    return json.loads(base64.b64decode(data).decode())
