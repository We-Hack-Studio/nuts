from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView
from rest_framework import mixins, permissions, throttling, viewsets

from .models import Credential
from .serializers import CredentialSerializer


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
