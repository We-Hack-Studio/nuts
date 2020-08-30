from typing import List

from core.mixins import ApiErrorsMixin
from django.db.models import QuerySet
from rest_framework import mixins, permissions, viewsets
from rest_framework.permissions import BasePermission

from .models import Strategy
from .serializers import StrategySerializer
from rest_framework import pagination


class StrategyViewSet(
    ApiErrorsMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = StrategySerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self) -> QuerySet:
        return Strategy.objects.all().order_by("-created_at")
