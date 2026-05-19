from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from apps.catalog.models.variant import ProductVariant


@admin.register(ProductVariant)
class ProductVariantAdmin(ModelAdmin):
    list_display = (
        "sku",
        "series",
        "color",
        "size_display_col",
        "price_uah",
        "old_price_uah",
        "in_stock",
        "ready_to_ship",
    )
    list_filter = ("in_stock", "ready_to_ship", "is_per_meter", "series__section")
    search_fields = ("sku", "series__name")
    autocomplete_fields = ("series", "color", "size")
    list_editable = ("price_uah", "in_stock", "ready_to_ship")

    fieldsets = (
        (
            _("Основне"),
            {
                "fields": ("series", "sku", "color", "size"),
            },
        ),
        (
            _("Розміри"),
            {
                "fields": ("width_cm", "length_cm", "is_per_meter"),
            },
        ),
        (
            _("Ціна"),
            {
                "fields": ("price_uah", "old_price_uah"),
            },
        ),
        (
            _("Наявність"),
            {
                "fields": ("stock", "in_stock", "ready_to_ship", "sort_order"),
            },
        ),
    )

    @admin.display(description=_("Розмір"))
    def size_display_col(self, obj):
        return obj.size_display
