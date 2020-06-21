from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView
from rest_framework import mixins, permissions, throttling, viewsets

from .forms import CredentialForm
from .models import Credential
from .serializers import CredentialSerializer


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


class CredentialViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = CredentialSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [throttling.UserRateThrottle]

    def get_queryset(self):
        user = self.request.user
        qs = user.credential_set.select_related("exchange").order_by("-created_at")
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
