from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from .models import CallbackRequest


@admin.register(CallbackRequest)
class CallbackRequestAdmin(ModelAdmin):
    list_display = ("name", "phone", "series", "is_processed", "created_at")
    list_filter = ("is_processed", "created_at")
    search_fields = ("name", "phone")
    list_editable = ("is_processed",)
    readonly_fields = ("created_at", "page_url")
