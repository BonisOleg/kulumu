from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.inclusion_tag("catalog/components/badge.html")
def product_badge(series):
    badges = []
    if series.is_new:
        badges.append(("new", "Новинка"))
    if series.is_top:
        badges.append(("top", "Топ"))
    if series.discount_percent:
        badges.append(("discount", f"-{series.discount_percent}%"))
    return {"badges": badges}


@register.filter
def star_rating(rating):
    """Перетворює 4.5 у зірочки ★★★★☆"""
    full = int(rating)
    empty = 5 - full
    return mark_safe("★" * full + "☆" * empty)


@register.simple_tag
def icon(name, css_class=""):
    """Material symbols icon."""
    return format_html(
        '<span class="material-symbols-outlined {}">{}</span>',
        css_class,
        name,
    )


@register.filter
def startswith(value, arg):
    """Перевіряє чи рядок починається з arg (для активного стану навігації)."""
    return str(value).startswith(str(arg))
