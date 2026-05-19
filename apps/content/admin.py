from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE
from unfold.admin import ModelAdmin, TabularInline

from .models.article import Article, ArticleCategory
from .models.faq import FAQCategory, FAQItem
from .models.page import StaticPage


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(ModelAdmin):
    list_display = ("name", "slug", "sort_order")
    prepopulated_fields = {"slug": ("name",)}


class FAQItemInline(TabularInline):
    model = FAQItem
    extra = 1
    fields = ("question", "answer", "sort_order", "is_active")


@admin.register(FAQCategory)
class FAQCategoryAdmin(ModelAdmin):
    list_display = ("name", "sort_order")
    inlines = [FAQItemInline]


@admin.register(FAQItem)
class FAQItemAdmin(ModelAdmin):
    list_display = ("question", "category", "sort_order", "is_active")
    list_filter = ("category", "is_active")
    list_editable = ("sort_order", "is_active")
    search_fields = ("question",)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in ("answer", "answer_uk", "answer_en"):
            kwargs["widget"] = TinyMCE()
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    list_display = ("cover_preview", "title", "category", "is_published", "published_at", "updated_at")
    list_display_links = ("cover_preview", "title")
    list_filter = ("is_published", "category")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("cover_preview_large", "created_at", "updated_at")
    fieldsets = (
        (_("Основне"), {"fields": ("title", "slug", "category", "cover", "cover_preview_large", "excerpt")}),
        (_("Контент"), {"fields": ("body",)}),
        (_("Пов'язані матеріали"), {"fields": ("related_facets", "related_series"), "classes": ("collapse",)}),
        (_("Публікація"), {"fields": ("is_published", "published_at")}),
        (_("SEO"), {"fields": ("seo_title", "seo_description"), "classes": ("collapse",)}),
        (_("Службове"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in ("body", "body_uk", "body_en"):
            kwargs["widget"] = TinyMCE()
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    @admin.display(description="")
    def cover_preview(self, obj):
        if obj.cover:
            return format_html('<img src="{}" style="width:60px;height:45px;object-fit:cover;border-radius:4px;">', obj.cover.url)
        return "—"

    @admin.display(description=_("Обкладинка"))
    def cover_preview_large(self, obj):
        if obj.cover:
            return format_html('<img src="{}" style="max-width:400px;border-radius:8px;">', obj.cover.url)
        return "—"


@admin.register(StaticPage)
class StaticPageAdmin(ModelAdmin):
    list_display = ("title", "slug", "updated_at")
    search_fields = ("title",)
    readonly_fields = ("updated_at",)
    fieldsets = (
        (_("Основне"), {"fields": ("slug", "title")}),
        (_("Контент"), {"fields": ("body",)}),
        (_("SEO"), {"fields": ("seo_title", "seo_description"), "classes": ("collapse",)}),
        (_("Службове"), {"fields": ("updated_at",), "classes": ("collapse",)}),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in ("body", "body_uk", "body_en"):
            kwargs["widget"] = TinyMCE()
        return super().formfield_for_dbfield(db_field, request, **kwargs)
