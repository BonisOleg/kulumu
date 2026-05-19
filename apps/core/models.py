from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteSettings(models.Model):
    """Singleton — налаштування сайту. Один запис завжди."""

    phone = models.CharField(_("Телефон"), max_length=32, default="+380XXXXXXXXX")
    phone_display = models.CharField(
        _("Телефон для відображення"), max_length=40, default="+380 (XX) XXX-XX-XX"
    )
    work_hours = models.CharField(
        _("Графік роботи"), max_length=120, default="Пн–Пт 9:00–19:00, Сб 10:00–18:00"
    )
    email = models.EmailField(_("Email"), default="info@kylymy.ua")
    address = models.CharField(_("Адреса"), max_length=200, blank=True)

    # Соцмережі
    instagram_url = models.URLField(_("Instagram"), blank=True)
    facebook_url = models.URLField(_("Facebook"), blank=True)
    telegram_url = models.URLField(_("Telegram"), blank=True)
    tiktok_url = models.URLField(_("TikTok"), blank=True)

    # SEO / аналітика
    gtm_id = models.CharField(
        _("GTM ID"), max_length=20, blank=True, help_text="GTM-XXXXXXX"
    )
    meta_pixel_id = models.CharField(_("Meta Pixel ID"), max_length=20, blank=True)

    # Юридична інформація
    company_name = models.CharField(_("Юр. назва"), max_length=200, blank=True)
    company_iban = models.CharField(_("IBAN"), max_length=40, blank=True)
    company_edrpou = models.CharField(_("ЄДРПОУ"), max_length=20, blank=True)

    # Доставка
    free_delivery_threshold = models.PositiveIntegerField(
        _("Безкоштовна доставка від (грн)"), default=1500
    )
    delivery_price = models.PositiveIntegerField(_("Ціна доставки (грн)"), default=70)

    # Повернення
    return_days = models.PositiveSmallIntegerField(
        _("Повернення протягом (днів)"), default=30
    )

    # Метадані для SEO (головна)
    site_title = models.CharField(
        _("Title сайту"),
        max_length=180,
        default="Kupyty kylym v Ukraini — Kylymy",
    )
    site_description = models.CharField(
        _("Description сайту"),
        max_length=300,
        blank=True,
    )

    class Meta:
        verbose_name = _("Налаштування сайту")
        verbose_name_plural = _("Налаштування сайту")

    def __str__(self):
        return "Налаштування сайту"

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
