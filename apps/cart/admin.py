from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, TabularInline

from .models import Order, OrderItem


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("series_name", "variant_sku", "color_name", "size_display", "quantity", "price_uah", "total_inline")
    can_delete = False

    @admin.display(description=_("Сума"))
    def total_inline(self, obj):
        if obj is None or not obj.pk:
            return "—"
        return format_html("<b>{}</b> ₴", f"{obj.total:,}".replace(",", "\u00a0"))


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = (
        "id", "name", "phone", "status_badge", "total_formatted",
        "payment_type", "payment_status", "created_at",
    )
    list_filter = ("status", "payment_type", "delivery_type", "created_at")
    search_fields = ("name", "phone", "email", "np_tracking_number", "payment_ref")
    readonly_fields = ("created_at", "updated_at", "payment_ref", "payment_status")
    inlines = [OrderItemInline]
    fieldsets = (
        (_("Контакти"), {"fields": ("name", "phone", "email")}),
        (_("Доставка"), {"fields": ("delivery_type", "np_city_name", "np_warehouse_address", "np_tracking_number")}),
        (_("Оплата"), {"fields": ("payment_type", "payment_status", "payment_ref")}),
        (_("Статус"), {"fields": ("status", "total_uah", "note")}),
        (_("Службове"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    @admin.display(description=_("Статус"))
    def status_badge(self, obj):
        colors = {
            "new": "#dc2626", "confirmed": "#b48a5e",
            "paid": "#2563eb", "processing": "#7c3aed",
            "shipped": "#0891b2", "delivered": "#16a34a",
            "cancelled": "#6b7280", "returned": "#374151",
        }
        color = colors.get(obj.status, "#888")
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:4px;font-size:11px;">{}</span>',
            color, obj.get_status_display()
        )

    @admin.display(description=_("Сума"))
    def total_formatted(self, obj):
        return format_html("<b>{}</b> ₴", f"{obj.total_uah:,}".replace(",", "\u00a0"))
