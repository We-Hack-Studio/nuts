from django import forms
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Credential


class CredentialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-exampleForm"
        self.helper.form_class = "blueForms"
        self.helper.form_method = "post"
        self.helper.form_action = reverse("credentials:add")
        self.helper.add_input(Submit("submit", "提交"))

    class Meta:
        model = Credential
        fields = ["note", "exchange", "api_key", "secret", "passphrase"]

    def save(self, commit=True):
        self.instance.user = self.user
        return super().save(commit=commit)
