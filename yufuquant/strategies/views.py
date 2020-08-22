from typing import List

from core.mixins import ApiErrorsMixin
from django.db.models import QuerySet
from rest_framework import mixins, permissions, viewsets
from rest_framework.permissions import BasePermission

from .models import StrategyTemplate
from .serializers import StrategyTemplateSerializer
from rest_framework import pagination


class StrategyTemplateViewSet(
    ApiErrorsMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = StrategyTemplateSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self) -> QuerySet:
        return StrategyTemplate.objects.all().order_by("-created_at")
