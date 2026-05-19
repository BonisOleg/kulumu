from django.utils.functional import SimpleLazyObject

from .models import SiteSettings


def global_context(request):
    """Глобальний контекст — доступний у всіх шаблонах."""
    settings_obj = SimpleLazyObject(SiteSettings.get)

    cart_count = 0
    cart = request.session.get("cart", {})
    if cart:
        cart_count = sum(item.get("qty", 1) for item in cart.values())

    from apps.catalog.selectors import get_active_sections
    sections = SimpleLazyObject(get_active_sections)

    return {
        "site_settings": settings_obj,
        "cart_count": cart_count,
        "sections": sections,
        "json_ld_product": None,
        "json_ld_faq": None,
        "json_ld_article": None,
    }
