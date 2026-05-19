from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def dashboard_callback(request, context):
    """Unfold dashboard KPI callback."""
    from apps.cart.models import Order
    from apps.catalog.models.series import ProductSeries
    from apps.catalog.models.media import ProductImage
    from apps.leads.models import CallbackRequest
    from apps.reviews.models import Review

    today = timezone.now().date()

    orders_today = Order.objects.filter(created_at__date=today)
    orders_today_count = orders_today.count()
    orders_today_sum = sum(o.total_uah for o in orders_today)

    pending_leads = CallbackRequest.objects.filter(is_processed=False)
    pending_reviews = Review.objects.filter(is_approved=False)

    total_series = ProductSeries.objects.count()
    inactive_series = ProductSeries.objects.filter(is_active=False).count()
    series_without_photos = (
        ProductSeries.objects.filter(is_active=True)
        .exclude(id__in=ProductImage.objects.values("series_id"))
        .count()
    )

    recent_leads = list(
        pending_leads.order_by("-created_at")[:5].values(
            "id", "name", "phone", "created_at"
        )
    )
    recent_reviews = list(
        pending_reviews.order_by("-created_at")[:5].values(
            "id", "author_name", "series__name", "rating", "created_at"
        )
    )

    context.update(
        {
            "kpi": [
                {
                    "title": _("Замовлення сьогодні"),
                    "metric": str(orders_today_count),
                    "footer": f"{orders_today_sum:,} ₴".replace(",", " "),
                    "icon": "receipt_long",
                },
                {
                    "title": _("Необроблені ліди"),
                    "metric": str(pending_leads.count()),
                    "footer": _("потребують відповіді"),
                    "icon": "phone_in_talk",
                },
                {
                    "title": _("Товарів у каталозі"),
                    "metric": str(total_series),
                    "footer": f"{inactive_series} неактивних · {series_without_photos} без фото",
                    "icon": "inventory_2",
                },
                {
                    "title": _("Відгуки на модерації"),
                    "metric": str(pending_reviews.count()),
                    "footer": _("очікують схвалення"),
                    "icon": "rate_review",
                },
            ],
            "recent_leads": recent_leads,
            "recent_reviews": recent_reviews,
        }
    )
    return context
