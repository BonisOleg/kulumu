"""Email-сповіщення."""
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def send_order_confirmation(order):
    subject = f"Ваше замовлення #{order.pk} прийнято — Kylymy"
    body = render_to_string("emails/order_confirmation.txt", {"order": order})
    recipients = [r for r in [order.email, settings.ADMIN_EMAIL] if r]
    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            recipients,
            fail_silently=False,
        )
    except Exception as exc:
        logger.error("Email send error for order #%s: %s", order.pk, exc)


def send_lead_notification(lead):
    subject = f"Новий запит на дзвінок від {lead.name}"
    body = f"Ім'я: {lead.name}\nТелефон: {lead.phone}\nСторінка: {lead.page_url}"
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL], fail_silently=True)
    except Exception as exc:
        logger.warning("Lead email error: %s", exc)
