from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST

from .forms import CheckoutForm
from .services import add_to_cart, create_order_from_cart, get_cart_items, get_cart_total, remove_from_cart


def cart_view(request):
    items = get_cart_items(request)
    total = get_cart_total(request)
    return TemplateResponse(request, "cart/cart.html", {"items": items, "total": total})


@require_POST
def add_to_cart_view(request):
    try:
        variant_id = int(request.POST["variant_id"])
        qty = int(request.POST.get("qty", 1))
        length_m = request.POST.get("length_m")
        if length_m:
            length_m = float(length_m)
    except (KeyError, ValueError):
        return JsonResponse({"error": "Невірні дані"}, status=400)

    add_to_cart(request, variant_id, qty=qty, length_m=length_m)

    cart_count = sum(v.get("qty", 1) for v in request.session.get("cart", {}).values())

    if request.htmx:
        return TemplateResponse(
            request,
            "cart/partials/mini_cart_toast.html",
            {"cart_count": cart_count, "message": "Товар додано до кошика"},
        )
    return JsonResponse({"cart_count": cart_count})


@require_POST
def remove_from_cart_view(request, variant_id):
    remove_from_cart(request, variant_id)
    if request.htmx:
        items = get_cart_items(request)
        total = get_cart_total(request)
        return TemplateResponse(
            request,
            "cart/partials/cart_items.html",
            {"items": items, "total": total},
        )
    return redirect("cart:cart")


def checkout_view(request):
    items = get_cart_items(request)
    if not items:
        return redirect("cart:cart")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = create_order_from_cart(request, form.cleaned_data)
            if order:
                from apps.integrations.mailer import send_order_confirmation
                from apps.integrations.telegram import notify_new_order
                send_order_confirmation(order)
                notify_new_order(order)
                return redirect("cart:success", order_id=order.pk)
    else:
        form = CheckoutForm()

    return TemplateResponse(
        request,
        "cart/checkout.html",
        {
            "form": form,
            "items": items,
            "total": get_cart_total(request),
            "page_title": "Оформлення замовлення | Kylymy",
        },
    )


def order_success_view(request, order_id):
    from .models import Order
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return redirect("catalog:home")
    return TemplateResponse(request, "cart/success.html", {"order": order})


def htmx_np_cities_view(request):
    """HTMX автокомпліт міст Нової Пошти."""
    query = request.GET.get("q", "").strip()
    if len(query) < 2:
        return TemplateResponse(request, "cart/partials/np_cities.html", {"cities": []})

    from apps.integrations.nova_poshta import search_cities
    cities = search_cities(query)
    return TemplateResponse(request, "cart/partials/np_cities.html", {"cities": cities})


def htmx_np_warehouses_view(request):
    """HTMX автокомпліт відділень НП."""
    city_ref = request.GET.get("city_ref", "")
    query = request.GET.get("q", "")
    if not city_ref:
        return TemplateResponse(request, "cart/partials/np_warehouses.html", {"warehouses": []})

    from apps.integrations.nova_poshta import search_warehouses
    warehouses = search_warehouses(city_ref, query)
    return TemplateResponse(request, "cart/partials/np_warehouses.html", {"warehouses": warehouses})
