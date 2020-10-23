from django.db.models import QuerySet
from rest_framework import mixins, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from .models import Strategy
from .serializers import StrategySerializer


class StrategyPagination(LimitOffsetPagination):
    default_limit = 50


class StrategyViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = StrategySerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = StrategyPagination

    def get_queryset(self) -> QuerySet:
        return Strategy.objects.all().order_by("-created_at")
