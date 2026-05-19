from django import template

register = template.Library()


@register.filter
def price(value):
    """Форматує ціну: 3950 → '3 950 ₴'"""
    try:
        return f"{int(value):,} ₴".replace(",", "\u00a0")
    except (TypeError, ValueError):
        return value


@register.filter
def discount_pct(old_price, new_price):
    """Повертає відсоток знижки."""
    try:
        pct = round((1 - new_price / old_price) * 100)
        return f"-{pct}%"
    except (TypeError, ValueError, ZeroDivisionError):
        return ""


@register.filter
def size_display(variant):
    """Форматує розмір варіанту: 200x300 → '2.0×3.0 м'"""
    try:
        w = variant.width_cm / 100
        if variant.length_cm:
            l = variant.length_cm / 100
            return f"{w:.1f}×{l:.1f} м"
        return f"{w:.1f} м (на відріз)"
    except (AttributeError, TypeError):
        return ""


@register.simple_tag(takes_context=True)
def url_with_page(context, page_num):
    """Будує URL зі збереженням усіх query-параметрів, замінюючи тільки page."""
    request = context.get("request")
    if not request:
        return f"?page={page_num}"
    params = request.GET.copy()
    params["page"] = page_num
    return "?" + params.urlencode()
