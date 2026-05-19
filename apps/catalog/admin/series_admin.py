from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, StackedInline, TabularInline

from apps.catalog.models.media import ProductImage
from apps.catalog.models.series import ProductSeries
from apps.catalog.models.variant import ProductVariant


class ProductVariantInline(TabularInline):
    model = ProductVariant
    extra = 1
    fields = (
        "sku", "color", "size", "width_cm", "length_cm",
        "is_per_meter", "price_uah", "old_price_uah", "in_stock", "ready_to_ship", "sort_order",
    )
    autocomplete_fields = ("color", "size")
    show_change_link = True
    ordering = ("sort_order", "width_cm")


class ProductImageInline(StackedInline):
    model = ProductImage
    extra = 1
    fields = ("image", "variant", "alt", "is_primary", "sort_order", "image_preview_inline")
    readonly_fields = ("image_preview_inline",)
    ordering = ("sort_order",)

    @admin.display(description=_("Попередній перегляд"))
    def image_preview_inline(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:80px;max-width:120px;border-radius:6px;'
                'object-fit:cover;">',
                obj.image.url,
            )
        return "—"


def action_activate(modeladmin, request, queryset):
    queryset.update(is_active=True)
action_activate.short_description = _("Опублікувати вибрані")


def action_deactivate(modeladmin, request, queryset):
    queryset.update(is_active=False)
action_deactivate.short_description = _("Приховати вибрані")


def action_make_top(modeladmin, request, queryset):
    queryset.update(is_top=True)
action_make_top.short_description = _("Зробити топом")


def action_remove_discount(modeladmin, request, queryset):
    queryset.update(discount_percent=0)
action_remove_discount.short_description = _("Зняти знижку")


@admin.register(ProductSeries)
class ProductSeriesAdmin(ModelAdmin):
    list_display = (
        "image_preview",
        "name",
        "section",
        "variants_count",
        "min_price_display",
        "badges_display",
        "is_active",
        "updated_at",
    )
    list_display_links = ("image_preview", "name")
    list_filter = ("section", "is_active", "is_top", "is_new")
    search_fields = ("name", "slug", "variants__sku")
    autocomplete_fields = ("facets",)
    readonly_fields = ("id", "created_at", "updated_at", "image_preview_large", "views_count")
    actions = [action_activate, action_deactivate, action_make_top, action_remove_discount]
    inlines = [ProductVariantInline, ProductImageInline]

    fieldsets = (
        (
            _("Основне"),
            {
                "fields": (
                    "id", "section", "name", "slug",
                    "short_descr", "full_descr", "care_instructions",
                ),
            },
        ),
        (
            _("Класифікація (фасети)"),
            {
                "fields": ("facets",),
                "description": _(
                    "Оберіть усі відповідні фасети: тип, стиль, призначення, форму, виробника."
                ),
            },
        ),
        (
            _("Характеристики"),
            {
                "fields": (
                    "pile_height_mm", "pile_type", "base_material",
                    "composition", "country", "manufacturer_brand",
                    "weight_per_m2", "density",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Маркетинг"),
            {
                "fields": (
                    "is_active", "is_top", "is_new", "discount_percent", "views_count",
                    "image_preview_large",
                ),
            },
        ),
        (
            _("SEO"),
            {
                "fields": ("seo_title", "seo_description"),
                "classes": ("collapse",),
                "description": _("Залишити порожнім — буде згенеровано автоматично."),
            },
        ),
        (
            _("Службове"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    @admin.display(description="")
    def image_preview(self, obj):
        img = obj.images.filter(is_primary=True).first() or obj.images.first()
        if img and img.image:
            return format_html(
                '<img src="{}" style="width:56px;height:56px;object-fit:cover;'
                'border-radius:6px;">',
                img.image.url,
            )
        return format_html('<span style="color:#ccc;">—</span>')

    @admin.display(description=_("Фото"))
    def image_preview_large(self, obj):
        img = obj.images.filter(is_primary=True).first() or obj.images.first()
        if img and img.image:
            return format_html(
                '<img src="{}" style="max-width:300px;border-radius:10px;">',
                img.image.url,
            )
        return "—"

    @admin.display(description=_("Варіантів"))
    def variants_count(self, obj):
        return obj.variants.count()

    @admin.display(description=_("Мін. ціна"))
    def min_price_display(self, obj):
        p = obj.min_price
        if p:
            return format_html("<b>{}</b> ₴", f"{p:,}".replace(",", "\u00a0"))
        return "—"

    @admin.display(description=_("Статус"))
    def badges_display(self, obj):
        parts = []
        if obj.is_top:
            parts.append('<span style="background:#b48a5e;color:#fff;padding:1px 6px;'
                        'border-radius:3px;font-size:10px;">ТОП</span>')
        if obj.is_new:
            parts.append('<span style="background:#4f8a4a;color:#fff;padding:1px 6px;'
                        'border-radius:3px;font-size:10px;">НОВЕ</span>')
        if obj.discount_percent:
            parts.append(f'<span style="background:#c44343;color:#fff;padding:1px 6px;'
                        f'border-radius:3px;font-size:10px;">-{obj.discount_percent}%</span>')
        return format_html(" ".join(parts)) if parts else format_html('<span style="color:#aaa;">—</span>')
