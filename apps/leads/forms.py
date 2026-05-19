from django import forms

from .models import CallbackRequest


class CallbackForm(forms.ModelForm):
    class Meta:
        model = CallbackRequest
        fields = ("name", "phone", "note")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Ваше ім'я", "class": "input"}),
            "phone": forms.TextInput(attrs={"placeholder": "+380XXXXXXXXX", "class": "input", "type": "tel"}),
            "note": forms.Textarea(attrs={"placeholder": "Коментар (опційно)", "class": "textarea", "rows": 3}),
        }
