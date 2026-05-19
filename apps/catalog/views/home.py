from django.core.cache import cache
from django.views.generic import TemplateView

from apps.catalog.selectors import get_active_sections, get_filtered_series


class HomeView(TemplateView):
    template_name = "catalog/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        top_series = cache.get("home_top_series")
        if top_series is None:
            top_series = list(
                get_filtered_series(sort="top").filter(is_top=True)[:12]
            )
            cache.set("home_top_series", top_series, 1800)

        new_series = cache.get("home_new_series")
        if new_series is None:
            new_series = list(
                get_filtered_series(sort="new").filter(is_new=True)[:8]
            )
            cache.set("home_new_series", new_series, 1800)

        ctx.update(
            {
                "top_series": top_series,
                "new_series": new_series,
                "page_title": "Купити килим в Україні — інтернет-магазин Kylymy",
                "usp_items": [],
                "default_usp": [
                    ("local_shipping", "Доставка по Україні", "Нова Пошта у будь-яке місто"),
                    ("replay", "Повернення 30 днів", "Не підійшло — повернемо без питань"),
                    ("verified", "Тільки перевірені товари", "Усі товари перевірені перед відправкою"),
                    ("support_agent", "Консультація безкоштовно", "Допоможемо підібрати по розміру та стилю"),
                ],
            }
        )
        return ctx
