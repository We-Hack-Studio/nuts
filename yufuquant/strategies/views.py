from typing import List

from django.db.models import QuerySet
from rest_framework import mixins, permissions, viewsets
from rest_framework.permissions import BasePermission

from .models import StrategyTemplate
from .serializers import StrategyTemplateSerializer


class StrategyTemplateViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    serializer_class = StrategyTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        return StrategyTemplate.objects.all().order_by("-created_at")

    def get_permissions(self) -> List[BasePermission]:
        if self.action in {"list"}:
            return [permissions.AllowAny()]
        return super().get_permissions()
