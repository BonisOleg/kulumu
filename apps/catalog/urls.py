from django.urls import path

from .views.facet import FacetView, htmx_filter_view
from .views.home import HomeView
from .views.search import SearchView
from .views.section import SectionView
from .views.series import SeriesView, htmx_per_meter_calc_view, htmx_variant_view

app_name = "catalog"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("search/", SearchView.as_view(), name="search"),

    # HTMX partials
    path("htmx/filter/<slug:section_slug>/", htmx_filter_view, name="htmx_filter"),
    path("htmx/series/<int:series_id>/variant/", htmx_variant_view, name="htmx_variant"),
    path("htmx/series/<int:series_id>/calc/", htmx_per_meter_calc_view, name="htmx_calc"),

    # Catalog pages
    path("<slug:section_slug>/", SectionView.as_view(), name="section"),
    path("<slug:section_slug>/seriya/<slug:series_slug>/", SeriesView.as_view(), name="series"),
    path("<slug:section_slug>/<slug:facet_slug>/", FacetView.as_view(), name="facet1"),
    path("<slug:section_slug>/<slug:f1>/<slug:f2>/", FacetView.as_view(), name="facet2"),
]
