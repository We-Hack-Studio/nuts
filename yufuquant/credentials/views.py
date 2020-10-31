from typing import Type

from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, permissions, throttling, viewsets
from rest_framework.serializers import BaseSerializer

from .models import Credential
from .serializers import (
    CredentialCreateSerializer,
    CredentialListSerializer,
    CredentialUpdateSerializer,
)


@method_decorator(
    name="create",
    decorator=extend_schema(
        summary="Bind exchange credential",
        request=CredentialCreateSerializer,
    ),
)
@method_decorator(
    name="list",
    decorator=extend_schema(
        summary="Return bound exchange credentials",
    ),
)
@method_decorator(
    name="update",
    decorator=extend_schema(
        summary="Update bound exchange credential",
    ),
)
@method_decorator(
    name="destroy",
    decorator=extend_schema(
        summary="Unbind exchange credential",
    ),
)
class CredentialViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    action_serializer_map = {
        "list": CredentialListSerializer,
        "create": CredentialCreateSerializer,
        "partial_update": CredentialUpdateSerializer,
    }
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [throttling.UserRateThrottle]
    pagination_class = None

    def get_queryset(self):
        qs = Credential.objects.filter(user=self.request.user)
        if self.action in {"list"}:
            qs = qs.select_related("exchange").order_by("-created_at")
        return qs

    def get_serializer_class(self) -> Type[BaseSerializer]:
        assert self.action in self.action_serializer_map
        return self.action_serializer_map[self.action]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
