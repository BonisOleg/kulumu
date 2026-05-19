"""Бізнес-логіка кошика і оформлення замовлення."""

CART_SESSION_KEY = "cart"


def get_cart(request: object) -> dict:
    return request.session.setdefault(CART_SESSION_KEY, {})


def add_to_cart(request, variant_id: int, qty: int = 1, length_m: float = None):
    cart = get_cart(request)
    key = str(variant_id)
    if key in cart:
        if length_m:
            cart[key]["length_m"] = length_m
        else:
            cart[key]["qty"] = cart[key].get("qty", 1) + qty
    else:
        cart[key] = {"qty": qty, "length_m": length_m}
    request.session.modified = True


def remove_from_cart(request, variant_id: int):
    cart = get_cart(request)
    cart.pop(str(variant_id), None)
    request.session.modified = True


def clear_cart(request):
    request.session[CART_SESSION_KEY] = {}
    request.session.modified = True


def get_cart_items(request):
    """Повертає список варіантів з кошика з їх даними."""
    from apps.catalog.models.variant import ProductVariant

    cart = get_cart(request)
    if not cart:
        return []

    variant_ids = [int(k) for k in cart.keys()]
    variants = ProductVariant.objects.filter(pk__in=variant_ids).select_related(
        "series__section", "color", "size"
    )
    items = []
    for v in variants:
        cart_data = cart[str(v.pk)]
        qty = cart_data.get("qty", 1)
        length_m = cart_data.get("length_m")
        total = int(v.price_uah * (float(length_m) if length_m else qty))
        items.append({"variant": v, "qty": qty, "length_m": length_m, "total": total})
    return items


def get_cart_total(request) -> int:
    return sum(item["total"] for item in get_cart_items(request))


def create_order_from_cart(request, form_data: dict):
    from .models import Order, OrderItem

    items = get_cart_items(request)
    if not items:
        return None

    total = get_cart_total(request)
    order = Order.objects.create(
        name=form_data["name"],
        phone=form_data["phone"],
        email=form_data.get("email", ""),
        delivery_type=form_data["delivery_type"],
        np_city_ref=form_data.get("np_city_ref", ""),
        np_city_name=form_data.get("np_city_name", ""),
        np_warehouse_ref=form_data.get("np_warehouse_ref", ""),
        np_warehouse_address=form_data.get("np_warehouse_address", ""),
        payment_type=form_data["payment_type"],
        total_uah=total,
        note=form_data.get("note", ""),
    )
    for item in items:
        v = item["variant"]
        OrderItem.objects.create(
            order=order,
            series_name=v.series.name,
            variant_sku=v.sku,
            color_name=v.color.name,
            size_display=v.size_display,
            quantity=item["qty"],
            price_uah=v.price_uah,
            is_per_meter=v.is_per_meter,
            length_m=item.get("length_m"),
        )

    clear_cart(request)
    return order
