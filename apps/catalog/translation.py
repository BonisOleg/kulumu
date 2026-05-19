from modeltranslation.translator import TranslationOptions, register

from .models.facet import Facet, Section
from .models.series import ProductSeries


@register(Section)
class SectionTranslationOptions(TranslationOptions):
    fields = ("name", "name_genitive", "seo_title", "seo_description", "seo_text")


@register(Facet)
class FacetTranslationOptions(TranslationOptions):
    fields = ("name", "seo_title", "seo_description", "seo_text")


@register(ProductSeries)
class ProductSeriesTranslationOptions(TranslationOptions):
    fields = ("name", "short_descr", "full_descr", "care_instructions", "seo_title", "seo_description")
