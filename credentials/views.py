from django.views.generic import ListView, CreateView, DeleteView
from .models import Credential

from .forms import CredentialForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin


class CredentialListView(LoginRequiredMixin, ListView):
    model = Credential
    ordering = ["-created_at"]
    context_object_name = "credential_list"
    template_name = "credentials/credential_list.html"


class CredentialCreateView(LoginRequiredMixin, CreateView):
    model = Credential
    form_class = CredentialForm
    template_name = "credentials/credential_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse("credentials:list")
