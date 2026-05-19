from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Order


class CheckoutForm(forms.Form):
    name = forms.CharField(label=_("Ім'я та прізвище"), max_length=100,
                           widget=forms.TextInput(attrs={"placeholder": "Іван Іваненко", "class": "input"}))
    phone = forms.CharField(label=_("Телефон"), max_length=32,
                            widget=forms.TextInput(attrs={"placeholder": "+380 63 000 00 00", "class": "input", "type": "tel"}))
    email = forms.EmailField(label=_("Email"), required=False,
                             widget=forms.EmailInput(attrs={"placeholder": "email@example.com", "class": "input"}))
    delivery_type = forms.ChoiceField(
        label=_("Спосіб доставки"),
        choices=Order.DeliveryType.choices,
        widget=forms.RadioSelect(attrs={"class": "radio-group"}),
        initial=Order.DeliveryType.NP_WAREHOUSE,
    )
    np_city_ref = forms.CharField(required=False, widget=forms.HiddenInput())
    np_city_name = forms.CharField(required=False, label=_("Місто"),
                                   widget=forms.TextInput(attrs={"placeholder": "Почніть вводити місто...", "class": "input", "autocomplete": "off"}))
    np_warehouse_ref = forms.CharField(required=False, widget=forms.HiddenInput())
    np_warehouse_address = forms.CharField(required=False, label=_("Відділення / адреса"),
                                           widget=forms.TextInput(attrs={"placeholder": "Вкажіть відділення або адресу", "class": "input"}))
    payment_type = forms.ChoiceField(
        label=_("Спосіб оплати"),
        choices=Order.PaymentType.choices,
        widget=forms.RadioSelect(attrs={"class": "radio-group"}),
        initial=Order.PaymentType.ONLINE,
    )
    note = forms.CharField(label=_("Коментар до замовлення"), required=False,
                           widget=forms.Textarea(attrs={"placeholder": "Додаткові побажання...", "class": "textarea", "rows": 3}))
