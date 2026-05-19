from django.utils.translation import gettext_lazy as _


def new_orders_count(request):
    from apps.cart.models import Order

    count = Order.objects.filter(status=Order.Status.NEW).count()
    return str(count) if count else None


def pending_leads_count(request):
    from apps.leads.models import CallbackRequest

    count = CallbackRequest.objects.filter(is_processed=False).count()
    return str(count) if count else None


def pending_reviews_count(request):
    from apps.reviews.models import Review

    count = Review.objects.filter(is_approved=False).count()
    return str(count) if count else None
