from django import forms
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Robot


class RobotForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "robot-form"
        self.helper.form_class = "robot-form"
        self.helper.form_method = "post"
        self.helper.form_action = reverse("robots:add")
        self.helper.add_input(Submit("submit", "创建"))

    class Meta:
        model = Robot
        fields = ["name", "pair", "enable", "credential"]

    def save(self, commit=True):
        self.instance.user = self.user
        return super().save(commit=commit)
