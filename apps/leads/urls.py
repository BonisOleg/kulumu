from django.urls import path

from .views import callback_request_view

app_name = "leads"

urlpatterns = [
    path("callback/", callback_request_view, name="callback"),
]
