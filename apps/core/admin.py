from django.contrib import admin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    """Singleton-адмінка для налаштувань сайту."""

    fieldsets = (
        (
            _("Контакти"),
            {
                "fields": ("phone", "phone_display", "work_hours", "email", "address"),
            },
        ),
        (
            _("Соціальні мережі"),
            {
                "fields": ("instagram_url", "facebook_url", "telegram_url", "tiktok_url"),
            },
        ),
        (
            _("Аналітика"),
            {
                "fields": ("gtm_id", "meta_pixel_id"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Юридичне"),
            {
                "fields": ("company_name", "company_iban", "company_edrpou"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Доставка та повернення"),
            {
                "fields": ("free_delivery_threshold", "delivery_price", "return_days"),
            },
        ),
        (
            _("SEO головної"),
            {
                "fields": ("site_title", "site_description"),
            },
        ),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj, _ = SiteSettings.objects.get_or_create(pk=1)
        return redirect("admin:core_sitesettings_change", obj.pk)
