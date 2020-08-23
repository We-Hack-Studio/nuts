from typing import Type

from core.mixins import ApiErrorsMixin
from rest_framework import mixins, permissions, throttling, viewsets
from rest_framework.serializers import BaseSerializer

from .serializers import CredentialListSerializer, CredentialSerializer


class CredentialViewSet(
    ApiErrorsMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    action_serializer_map = {
        "list": CredentialListSerializer,
        "retrieve": CredentialSerializer,
    }
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [throttling.UserRateThrottle]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        qs = user.credential_set.select_related("exchange").order_by("-created_at")
        return qs

    def get_serializer_class(self) -> Type[BaseSerializer]:
        return self.action_serializer_map.get(self.action, CredentialSerializer)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
