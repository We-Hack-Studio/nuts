from typing import Type

from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, permissions, throttling, viewsets
from rest_framework.serializers import BaseSerializer

from .models import Credential
from .serializers import CredentialCreateSerializer, CredentialListSerializer


@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="",
        request_body=CredentialCreateSerializer(),
    ),
)
class CredentialViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    action_serializer_map = {
        "list": CredentialListSerializer,
        "create": CredentialCreateSerializer,
    }
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [throttling.UserRateThrottle]
    pagination_class = None
    resource_name = "credentials"

    def get_queryset(self):
        qs = Credential.objects.filter(user=self.request.user)
        if self.action in {"list"}:
            qs = qs.select_related("exchange").order_by("-created_at")
        return qs

    def get_serializer_class(self) -> Type[BaseSerializer]:
        if getattr(self, "swagger_fake_view", False):
            return CredentialListSerializer

        assert self.action in self.action_serializer_map
        return self.action_serializer_map[self.action]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
