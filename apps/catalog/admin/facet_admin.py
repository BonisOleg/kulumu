from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from apps.catalog.models.facet import Facet, FacetType, Section


@admin.register(Section)
class SectionAdmin(ModelAdmin):
    list_display = ("name", "slug", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        (_("Основне"), {"fields": ("name", "name_genitive", "slug", "icon_name", "sort_order", "is_active")}),
        (_("SEO"), {"fields": ("seo_title", "seo_description", "seo_text"), "classes": ("collapse",)}),
    )


@admin.register(Facet)
class FacetAdmin(ModelAdmin):
    list_display = ("name", "type_badge", "slug", "is_indexable", "sort_order")
    list_editable = ("sort_order", "is_indexable")
    list_filter = ("type", "is_indexable")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        (
            _("Основне"),
            {
                "fields": ("type", "name", "slug", "color_hex", "parent", "sort_order", "is_indexable"),
            },
        ),
        (
            _("SEO"),
            {
                "fields": ("seo_title", "seo_description", "seo_text"),
                "classes": ("collapse",),
            },
        ),
    )

    @admin.display(description=_("Тип"))
    def type_badge(self, obj):
        colors = {
            FacetType.CATEGORY: "#4f8a4a",
            FacetType.PURPOSE: "#b48a5e",
            FacetType.STYLE: "#6366f1",
            FacetType.FORM: "#0891b2",
            FacetType.SIZE: "#dc2626",
            FacetType.COLOR: "#1a1a1a",
            FacetType.MANUFACTURER: "#9333ea",
        }
        color = colors.get(obj.type, "#888")
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:4px;'
            'font-size:11px;">{}</span>',
            color,
            obj.get_type_display(),
        )
