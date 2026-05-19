from django.urls import path
from django.views.generic import ListView, DetailView, TemplateView

from .models.article import Article
from .models.faq import FAQItem
from .models.page import StaticPage

app_name = "content"


class ArticleListView(ListView):
    model = Article
    template_name = "content/article_list.html"
    context_object_name = "articles"
    paginate_by = 12

    def get_queryset(self):
        return Article.objects.filter(is_published=True).select_related("category")


class ArticleDetailView(DetailView):
    model = Article
    template_name = "content/article_detail.html"
    context_object_name = "article"
    queryset = Article.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["related_articles"] = (
            Article.objects.filter(is_published=True, category=self.object.category)
            .exclude(pk=self.object.pk)[:3]
        )
        return ctx


class FAQView(TemplateView):
    template_name = "content/faq.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["faq_items"] = FAQItem.objects.filter(is_active=True).select_related("category")
        ctx["page_title"] = "Питання та відповіді — Kylymy"
        return ctx


class StaticPageView(DetailView):
    model = StaticPage
    template_name = "pages/static_page.html"
    context_object_name = "page"

    def get_object(self, queryset=None):
        try:
            return StaticPage.objects.get(slug=self.kwargs["slug"])
        except StaticPage.DoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.object is None:
            slug = self.kwargs["slug"]
            ctx["page_title_fallback"] = dict(StaticPage.SLUG_CHOICES).get(
                slug, slug.replace("-", " ").capitalize()
            )
        return ctx


urlpatterns = [
    path("", ArticleListView.as_view(), name="article_list"),
    path("faq/", FAQView.as_view(), name="faq"),
    path("<slug:slug>/", ArticleDetailView.as_view(), name="article"),
    path("page/<slug:slug>/", StaticPageView.as_view(), name="page"),
]
