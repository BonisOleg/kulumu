from django.db import models
from django.utils.translation import gettext_lazy as _


class StaticPage(models.Model):
    """Статичні сторінки: Доставка, Про нас, Контакти, Гарантії тощо."""

    SLUG_CHOICES = [
        ("delivery", "Доставка та оплата"),
        ("about", "Про нас"),
        ("contacts", "Контакти"),
        ("guarantee", "Гарантії та повернення"),
        ("how-to-choose", "Як вибрати килим"),
        ("care", "Догляд за килимом"),
    ]

    slug = models.SlugField(_("Slug"), unique=True, choices=SLUG_CHOICES)
    title = models.CharField(_("Заголовок"), max_length=200)
    body = models.TextField(_("Вміст"))
    seo_title = models.CharField(_("SEO Title"), max_length=180, blank=True)
    seo_description = models.CharField(_("SEO Description"), max_length=300, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Статична сторінка")
        verbose_name_plural = _("Статичні сторінки")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("content:page", kwargs={"slug": self.slug})
