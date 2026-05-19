from django.db import models
from django.utils.translation import gettext_lazy as _


class CallbackRequest(models.Model):
    name = models.CharField(_("Ім'я"), max_length=80)
    phone = models.CharField(_("Телефон"), max_length=32)
    page_url = models.URLField(_("URL сторінки"), blank=True)
    series = models.ForeignKey(
        "catalog.ProductSeries",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Товар"),
    )
    note = models.TextField(_("Примітка"), blank=True)
    is_processed = models.BooleanField(_("Оброблено"), default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Запит на дзвінок")
        verbose_name_plural = _("Запити на дзвінок")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} {self.phone}"
