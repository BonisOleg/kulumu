from django.db import models
from django.utils.translation import gettext_lazy as _


class Section(models.Model):
    """Верхній рівень каталогу: kilymi / dorizhky / kovrolin / dlya-vannoyi / akciyi."""

    slug = models.SlugField(_("URL (slug)"), unique=True, max_length=80)
    name = models.CharField(_("Назва"), max_length=80)
    name_genitive = models.CharField(
        _("Назва у родовому відмінку"), max_length=80, blank=True,
        help_text="Для шаблонів: 'купити {kilymiv}'"
    )
    icon_name = models.CharField(
        _("Іконка (Material Symbols)"), max_length=40, blank=True
    )
    seo_title = models.CharField(_("SEO Title"), max_length=180, blank=True)
    seo_description = models.CharField(_("SEO Description"), max_length=300, blank=True)
    seo_text = models.TextField(_("SEO-текст (внизу каталогу)"), blank=True)
    sort_order = models.PositiveSmallIntegerField(_("Порядок"), default=0)
    is_active = models.BooleanField(_("Активний"), default=True)

    class Meta:
        verbose_name = _("Розділ")
        verbose_name_plural = _("Розділи")
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("catalog:section", kwargs={"section_slug": self.slug})

    def get_seo_title(self):
        if self.seo_title:
            return self.seo_title
        return f"{self.name} — купити в Україні | Kylymy"


class FacetType(models.TextChoices):
    CATEGORY = "category", _("Тип / матеріал")
    PURPOSE = "purpose", _("Призначення")
    STYLE = "style", _("Стиль")
    FORM = "form", _("Форма")
    SIZE = "size", _("Розмір")
    COLOR = "color", _("Колір")
    MANUFACTURER = "manufacturer", _("Виробник")


class Facet(models.Model):
    """Фасет — один елемент будь-якого зрізу класифікації."""

    type = models.CharField(
        _("Тип фасету"), max_length=16, choices=FacetType.choices, db_index=True
    )
    slug = models.SlugField(_("URL (slug)"), max_length=100)
    name = models.CharField(_("Назва"), max_length=100)
    color_hex = models.CharField(
        _("HEX-колір (для swатчу)"), max_length=7, blank=True,
        help_text="#RRGGBB, тільки для type=color"
    )
    is_indexable = models.BooleanField(
        _("Індексувати як окрему SEO-сторінку"), default=True
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
        verbose_name=_("Батьківський фасет"),
    )
    sort_order = models.PositiveSmallIntegerField(_("Порядок"), default=0)
    seo_title = models.CharField(_("SEO Title"), max_length=180, blank=True)
    seo_description = models.CharField(_("SEO Description"), max_length=300, blank=True)
    seo_text = models.TextField(_("SEO-текст (внизу каталогу)"), blank=True)

    class Meta:
        verbose_name = _("Фасет")
        verbose_name_plural = _("Фасети")
        unique_together = ("type", "slug")
        ordering = ["type", "sort_order", "name"]
        indexes = [
            models.Index(fields=["type", "is_indexable"]),
        ]

    def __str__(self):
        return f"{self.get_type_display()} — {self.name}"
