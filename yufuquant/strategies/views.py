from django.db.models import QuerySet
from rest_framework import mixins, pagination, permissions, viewsets

from .models import Strategy
from .serializers import StrategySerializer


class StrategyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = StrategySerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self) -> QuerySet:
        return Strategy.objects.all().order_by("-created_at")
