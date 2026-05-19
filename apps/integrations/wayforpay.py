"""Інтеграція з WayForPay."""
import hashlib
import hmac
import logging
import time

from django.conf import settings

logger = logging.getLogger(__name__)

_SEPARATOR = ";"
_CURRENCY = "UAH"


def _make_signature(*parts: str) -> str:
    message = _SEPARATOR.join(str(p) for p in parts)
    return hmac.new(
        settings.WAYFORPAY_MERCHANT_SECRET.encode(),
        message.encode(),
        hashlib.md5,
    ).hexdigest()


def generate_payment_form_data(order) -> dict:
    """Повертає dict-параметри для прихованої форми WayForPay."""
    merchant = settings.WAYFORPAY_MERCHANT_ACCOUNT
    domain = settings.SITE_URL.rstrip("/").replace("https://", "").replace("http://", "")
    order_ref = f"kylymy-{order.pk}"
    order_date = int(time.time())
    amount = str(order.total_uah)
    product_name = f"Замовлення #{order.pk}"
    product_count = "1"
    product_price = amount

    signature = _make_signature(
        merchant, domain, order_ref, order_date,
        amount, _CURRENCY,
        product_name, product_count, product_price,
    )

    return {
        "merchantAccount": merchant,
        "merchantDomainName": domain,
        "merchantTransactionSecureType": "AUTO",
        "orderReference": order_ref,
        "orderDate": order_date,
        "amount": amount,
        "currency": _CURRENCY,
        "productName[]": product_name,
        "productCount[]": product_count,
        "productPrice[]": product_price,
        "returnUrl": f"{settings.SITE_URL}/cart/success/{order.pk}/",
        "serviceUrl": f"{settings.SITE_URL}/payments/wayforpay/callback/",
        "merchantSignature": signature,
        "language": "UA",
        "form_url": "https://secure.wayforpay.com/pay",
    }


def verify_callback(post_data: dict) -> bool:
    """Перевіряє підпис вхідного callback від WayForPay."""
    received = post_data.get("merchantSignature", "")
    try:
        expected = _make_signature(
            post_data.get("merchantAccount", ""),
            post_data.get("orderReference", ""),
            post_data.get("amount", ""),
            post_data.get("currency", ""),
            post_data.get("authCode", ""),
            post_data.get("cardPan", ""),
            post_data.get("transactionStatus", ""),
            post_data.get("reasonCode", ""),
        )
        return hmac.compare_digest(received, expected)
    except Exception as exc:
        logger.warning("WayForPay callback signature error: %s", exc)
        return False
