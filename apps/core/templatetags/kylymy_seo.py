import json

from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def canonical_url(context):
    request = context.get("request")
    if not request:
        return ""
    url = request.build_absolute_uri(request.path)
    return format_html('<link rel="canonical" href="{}">', url)


@register.simple_tag(takes_context=True)
def hreflang_tags(context):
    request = context.get("request")
    if not request:
        return ""
    path = request.path
    site_url = request.build_absolute_uri("/").rstrip("/")

    tags = [
        f'<link rel="alternate" hreflang="uk" href="{site_url}{path}">',
        f'<link rel="alternate" hreflang="x-default" href="{site_url}{path}">',
    ]
    return mark_safe("\n".join(tags))


@register.simple_tag
def json_ld(data):
    """Виводить JSON-LD блок."""
    if data is None:
        return ""
    # Розкриваємо lazy-об'єкти (SimpleLazyObject, dict, callable)
    if hasattr(data, "_wrapped"):
        data = data._wrapped if data._wrapped is not None else data.__class__.__wrapped__(data)
    if callable(data) and not isinstance(data, dict):
        data = data()
    if not isinstance(data, dict):
        try:
            data = dict(data)
        except (TypeError, ValueError):
            return ""
    return mark_safe(
        f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'
    )


@register.inclusion_tag("base/_breadcrumbs.html", takes_context=True)
def breadcrumbs(context, *items):
    """Рендерить хлібні крихти. items = список (назва, url) або тільки назва."""
    return {"items": items, "request": context.get("request")}
