from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST

from .forms import CallbackForm
from .models import CallbackRequest


@require_POST
def callback_request_view(request):
    form = CallbackForm(request.POST)
    if form.is_valid():
        lead = form.save(commit=False)
        lead.page_url = request.POST.get("page_url", "")
        lead.save()

        from apps.integrations.telegram import notify_new_lead
        notify_new_lead(lead)

        return TemplateResponse(
            request,
            "leads/callback_success.html",
            {"name": lead.name},
        )

    return TemplateResponse(
        request,
        "leads/callback_modal.html",
        {"form": form},
    )
