from modeltranslation.translator import TranslationOptions, register

from .models.article import Article, ArticleCategory
from .models.faq import FAQCategory, FAQItem
from .models.page import StaticPage


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ("title", "excerpt", "body", "seo_title", "seo_description")


@register(FAQItem)
class FAQItemTranslationOptions(TranslationOptions):
    fields = ("question", "answer")


@register(StaticPage)
class StaticPageTranslationOptions(TranslationOptions):
    fields = ("title", "body", "seo_title", "seo_description")
