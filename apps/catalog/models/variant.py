from django.db import models
from django.utils.translation import gettext_lazy as _


class ProductVariant(models.Model):
    """Варіант серії: один розмір × один колір = один SKU з ціною."""

    series = models.ForeignKey(
        "catalog.ProductSeries",
        on_delete=models.CASCADE,
        related_name="variants",
        verbose_name=_("Серія"),
    )
    sku = models.CharField(_("Артикул (SKU)"), max_length=64, unique=True)
    color = models.ForeignKey(
        "catalog.Facet",
        on_delete=models.PROTECT,
        related_name="variant_colors",
        verbose_name=_("Колір"),
        limit_choices_to={"type": "color"},
    )
    size = models.ForeignKey(
        "catalog.Facet",
        on_delete=models.PROTECT,
        related_name="variant_sizes",
        verbose_name=_("Розмір"),
        limit_choices_to={"type": "size"},
        null=True,
        blank=True,
    )

    # Розміри в сантиметрах
    width_cm = models.PositiveSmallIntegerField(_("Ширина (см)"))
    length_cm = models.PositiveSmallIntegerField(
        _("Довжина (см)"),
        null=True,
        blank=True,
        help_text=_("Залишити порожнім для продажу на відріз (пог.м)"),
    )
    is_per_meter = models.BooleanField(
        _("Продається на відріз (пог.м)"),
        default=False,
        db_index=True,
    )

    # Ціна
    price_uah = models.PositiveIntegerField(_("Ціна (грн)"))
    old_price_uah = models.PositiveIntegerField(
        _("Стара ціна (грн)"), null=True, blank=True
    )

    # Наявність
    stock = models.PositiveIntegerField(_("Залишок"), default=0)
    in_stock = models.BooleanField(_("В наявності"), default=True, db_index=True)
    ready_to_ship = models.BooleanField(_("Готово до відправки"), default=True)

    sort_order = models.PositiveSmallIntegerField(_("Порядок"), default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Варіант товару")
        verbose_name_plural = _("Варіанти товарів")
        ordering = ["sort_order", "width_cm", "length_cm"]
        indexes = [
            models.Index(fields=["series", "in_stock"]),
        ]

    def __str__(self):
        size_str = f"{self.width_cm}×{self.length_cm}" if self.length_cm else f"{self.width_cm} пог.м"
        return f"{self.series.name} | {self.color.name} | {size_str}"

    @property
    def size_display(self):
        w = self.width_cm / 100
        if self.length_cm:
            l = self.length_cm / 100
            return f"{w:.1f}×{l:.1f} м"
        return f"{w:.1f} м (на відріз)"

    @property
    def discount_percent(self):
        if self.old_price_uah and self.old_price_uah > self.price_uah:
            return round((1 - self.price_uah / self.old_price_uah) * 100)
        return 0
