from django.db import models
from django.utils.translation import gettext_lazy as _


class FAQCategory(models.Model):
    name = models.CharField(_("Назва"), max_length=80)
    sort_order = models.PositiveSmallIntegerField(_("Порядок"), default=0)

    class Meta:
        verbose_name = _("Категорія FAQ")
        verbose_name_plural = _("Категорії FAQ")
        ordering = ["sort_order"]

    def __str__(self):
        return self.name


class FAQItem(models.Model):
    category = models.ForeignKey(
        FAQCategory, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="items", verbose_name=_("Категорія")
    )
    question = models.CharField(_("Питання"), max_length=300)
    answer = models.TextField(_("Відповідь"))
    sort_order = models.PositiveSmallIntegerField(_("Порядок"), default=0)
    is_active = models.BooleanField(_("Активний"), default=True)

    class Meta:
        verbose_name = _("FAQ питання")
        verbose_name_plural = _("FAQ питання")
        ordering = ["category__sort_order", "sort_order"]

    def __str__(self):
        return self.question
