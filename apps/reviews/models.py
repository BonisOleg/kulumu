from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Review(models.Model):
    series = models.ForeignKey(
        "catalog.ProductSeries",
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("Серія товарів"),
        null=True,
        blank=True,
    )
    author_name = models.CharField(_("Ім'я"), max_length=80)
    rating = models.PositiveSmallIntegerField(
        _("Оцінка (1-5)"),
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    body = models.TextField(_("Текст відгуку"))
    photo = models.ImageField(_("Фото"), upload_to="reviews/", blank=True)
    is_approved = models.BooleanField(_("Схвалено"), default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Відгук")
        verbose_name_plural = _("Відгуки")
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["series", "is_approved"])]

    def __str__(self):
        return f"{self.author_name} — {'★' * self.rating}"
