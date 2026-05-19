from django.db import models
from django.utils.translation import gettext_lazy as _


class ArticleCategory(models.Model):
    slug = models.SlugField(_("Slug"), unique=True)
    name = models.CharField(_("Назва"), max_length=80)
    sort_order = models.PositiveSmallIntegerField(_("Порядок"), default=0)

    class Meta:
        verbose_name = _("Рубрика блогу")
        verbose_name_plural = _("Рубрики блогу")
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class Article(models.Model):
    category = models.ForeignKey(
        ArticleCategory, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="articles", verbose_name=_("Рубрика")
    )
    slug = models.SlugField(_("Slug"), unique=True, max_length=120)
    title = models.CharField(_("Заголовок"), max_length=200)
    cover = models.ImageField(_("Обкладинка"), upload_to="articles/", blank=True)
    excerpt = models.CharField(_("Короткий опис"), max_length=300, blank=True)
    body = models.TextField(_("Текст статті"))

    related_facets = models.ManyToManyField(
        "catalog.Facet", blank=True, verbose_name=_("Пов'язані фасети")
    )
    related_series = models.ManyToManyField(
        "catalog.ProductSeries", blank=True, verbose_name=_("Пов'язані товари")
    )

    seo_title = models.CharField(_("SEO Title"), max_length=180, blank=True)
    seo_description = models.CharField(_("SEO Description"), max_length=300, blank=True)

    is_published = models.BooleanField(_("Опубліковано"), default=False, db_index=True)
    published_at = models.DateTimeField(_("Дата публікації"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Стаття")
        verbose_name_plural = _("Статті")
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("content:article", kwargs={"slug": self.slug})
