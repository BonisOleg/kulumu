from django.urls import path

from .views import (
    add_to_cart_view, cart_view, checkout_view,
    htmx_np_cities_view, htmx_np_warehouses_view,
    order_success_view, remove_from_cart_view,
)

app_name = "cart"

urlpatterns = [
    path("", cart_view, name="cart"),
    path("add/", add_to_cart_view, name="add"),
    path("remove/<int:variant_id>/", remove_from_cart_view, name="remove"),
    path("checkout/", checkout_view, name="checkout"),
    path("success/<int:order_id>/", order_success_view, name="success"),
    path("htmx/cities/", htmx_np_cities_view, name="htmx_cities"),
    path("htmx/warehouses/", htmx_np_warehouses_view, name="htmx_warehouses"),
]
