from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from .models import Review


def action_approve(modeladmin, request, queryset):
    queryset.update(is_approved=True)
action_approve.short_description = _("Схвалити вибрані відгуки")


def action_reject(modeladmin, request, queryset):
    queryset.update(is_approved=False)
action_reject.short_description = _("Відхилити вибрані відгуки")


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ("author_name", "rating_stars", "series", "is_approved", "created_at")
    list_filter = ("is_approved", "rating", "created_at")
    search_fields = ("author_name", "body", "series__name")
    readonly_fields = ("created_at", "photo_preview")
    list_editable = ("is_approved",)
    actions = [action_approve, action_reject]
    fieldsets = (
        (_("Відгук"), {"fields": ("series", "author_name", "rating", "body", "photo", "photo_preview")}),
        (_("Модерація"), {"fields": ("is_approved", "created_at")}),
    )

    @admin.display(description=_("Оцінка"))
    def rating_stars(self, obj):
        return "★" * obj.rating + "☆" * (5 - obj.rating)

    @admin.display(description=_("Фото"))
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height:100px;border-radius:6px;">', obj.photo.url)
        return "—"
