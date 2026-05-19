from django.db import models
from django.utils.translation import gettext_lazy as _


class ProductSeries(models.Model):
    """Одна модель/серія = одна SEO-сторінка з кількома варіантами (колір × розмір)."""

    section = models.ForeignKey(
        "catalog.Section",
        on_delete=models.PROTECT,
        related_name="series",
        verbose_name=_("Розділ"),
    )
    slug = models.SlugField(_("URL (slug)"), max_length=120)
    name = models.CharField(_("Назва серії"), max_length=120)
    short_descr = models.TextField(_("Короткий опис"), blank=True)
    full_descr = models.TextField(_("Повний опис"), blank=True)
    care_instructions = models.TextField(_("Догляд та чищення"), blank=True)

    facets = models.ManyToManyField(
        "catalog.Facet",
        related_name="series",
        verbose_name=_("Фасети (тип/стиль/призначення/форма/виробник)"),
        blank=True,
    )

    # Характеристики
    pile_height_mm = models.PositiveSmallIntegerField(
        _("Висота ворсу (мм)"), null=True, blank=True
    )
    pile_type = models.CharField(_("Тип ворсу"), max_length=80, blank=True)
    base_material = models.CharField(_("Матеріал основи"), max_length=80, blank=True)
    composition = models.CharField(_("Склад"), max_length=120, blank=True)
    country = models.CharField(_("Країна-виробник"), max_length=40, blank=True)
    manufacturer_brand = models.CharField(_("Бренд виробника"), max_length=80, blank=True)
    weight_per_m2 = models.PositiveIntegerField(
        _("Вага (г/м²)"), null=True, blank=True
    )
    density = models.PositiveIntegerField(
        _("Щільність (точок/м²)"), null=True, blank=True
    )

    # Маркетинг
    is_active = models.BooleanField(_("Активний"), default=True, db_index=True)
    is_top = models.BooleanField(_("Топ"), default=False)
    is_new = models.BooleanField(_("Новинка"), default=False)
    discount_percent = models.PositiveSmallIntegerField(_("Знижка %"), default=0)

    # SEO
    seo_title = models.CharField(_("SEO Title"), max_length=180, blank=True)
    seo_description = models.CharField(_("SEO Description"), max_length=300, blank=True)

    views_count = models.PositiveIntegerField(_("Переглядів"), default=0, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Серія товарів")
        verbose_name_plural = _("Серії товарів")
        unique_together = ("section", "slug")
        indexes = [
            models.Index(fields=["section", "is_active"]),
            models.Index(fields=["is_top", "is_new"]),
        ]
        ordering = ["-is_top", "-is_new", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse(
            "catalog:series",
            kwargs={"section_slug": self.section.slug, "series_slug": self.slug},
        )

    @property
    def min_price(self):
        prices = list(self.variants.filter(in_stock=True).values_list("price_uah", flat=True))
        if not prices:
            prices = list(self.variants.values_list("price_uah", flat=True))
        return min(prices) if prices else 0

    @property
    def primary_image(self):
        # Якщо є prefetch-кеш (to_attr="primary_images" з selectors) — DB-запит не потрібен
        if hasattr(self, "primary_images"):
            return self.primary_images[0] if self.primary_images else None
        img = self.images.filter(is_primary=True).first()
        if not img:
            img = self.images.first()
        return img

    def get_seo_title(self):
        if self.seo_title:
            return self.seo_title
        return f"{self.name} — купити в Україні | Kylymy"

    def get_seo_description(self):
        if self.seo_description:
            return self.seo_description
        parts = []
        if self.country:
            parts.append(f"виробництво {self.country}")
        if self.pile_height_mm:
            parts.append(f"висота ворсу {self.pile_height_mm} мм")
        # Use prefetch cache when available (avoids extra DB query on detail page)
        _cache = getattr(self, "_prefetched_objects_cache", {})
        variants_count = len(_cache["variants"]) if "variants" in _cache else self.variants.count()
        if variants_count:
            parts.append(f"{variants_count} розмірів")
        parts.append(f"від {self.min_price:,} ₴".replace(",", "\u00a0"))
        base = f"Купити {self.name}"
        if parts:
            base += " — " + ", ".join(parts)
        return base + ". Доставка по Україні."
