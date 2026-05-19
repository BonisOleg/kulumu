"""Telegram сповіщення для адміна."""
import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"


def _send(text: str):
    token = getattr(settings, "TELEGRAM_BOT_TOKEN", "")
    chat_id = getattr(settings, "TELEGRAM_ADMIN_CHAT_ID", "")
    if not token or not chat_id:
        return
    try:
        requests.post(
            TELEGRAM_API.format(token=token),
            data={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
            timeout=5,
        )
    except Exception as exc:
        logger.warning("Telegram send error: %s", exc)


def notify_new_order(order):
    text = (
        f"🛒 <b>Нове замовлення #{order.pk}</b>\n"
        f"👤 {order.name} | {order.phone}\n"
        f"💰 {order.total_uah:,} ₴\n"
        f"📦 {order.get_delivery_type_display()}\n"
        f"💳 {order.get_payment_type_display()}"
    )
    _send(text)


def notify_new_lead(lead):
    text = (
        f"📞 <b>Запит на дзвінок</b>\n"
        f"👤 {lead.name} | {lead.phone}\n"
        f"📄 {lead.page_url or '—'}"
    )
    _send(text)
