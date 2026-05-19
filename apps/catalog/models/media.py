import os

from django.db import models
from django.utils.translation import gettext_lazy as _


def series_image_path(instance, filename):
    ext = filename.rsplit(".", 1)[-1].lower()
    series_slug = instance.series.slug if instance.series else "misc"
    return f"products/{series_slug}/{instance.id or 'new'}.{ext}"


class ProductImage(models.Model):
    """Фото товару. Може бути прив'язане до серії або до конкретного варіанту."""

    series = models.ForeignKey(
        "catalog.ProductSeries",
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Серія"),
    )
    variant = models.ForeignKey(
        "catalog.ProductVariant",
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Варіант (опційно)"),
        null=True,
        blank=True,
    )
    image = models.ImageField(_("Фото"), upload_to=series_image_path)
    image_webp = models.ImageField(
        _("WebP версія"), upload_to="products/webp/", blank=True, editable=False
    )
    image_thumb = models.ImageField(
        _("Мініатюра"), upload_to="products/thumb/", blank=True, editable=False
    )
    alt = models.CharField(
        _("Alt-текст"), max_length=160, blank=True,
        help_text=_("Залишити порожнім для автогенерації з назви серії")
    )
    is_primary = models.BooleanField(_("Головне фото"), default=False)
    sort_order = models.PositiveSmallIntegerField(_("Порядок"), default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Фото товару")
        verbose_name_plural = _("Фото товарів")
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"Фото #{self.sort_order} — {self.series.name}"

    def save(self, *args, **kwargs):
        if not self.alt and self.series_id:
            self.alt = self.series.name
        super().save(*args, **kwargs)

    def get_image_url(self, size="original"):
        """Повертає URL для потрібного розміру (original / thumb / webp)."""
        if size == "thumb" and self.image_thumb:
            return self.image_thumb.url
        if size == "webp" and self.image_webp:
            return self.image_webp.url
        return self.image.url if self.image else ""
