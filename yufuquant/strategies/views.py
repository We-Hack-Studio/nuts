from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from .models import Strategy
from .serializers import StrategySerializer


class StrategyPagination(LimitOffsetPagination):
    default_limit = 50


@method_decorator(
    name="list",
    decorator=extend_schema(
        summary="Return all strategies",
        request=StrategySerializer,
    ),
)
@method_decorator(
    name="retrieve",
    decorator=extend_schema(
        summary="Strategy detail",
        request=StrategySerializer,
    ),
)
@method_decorator(
    name="create",
    decorator=extend_schema(
        summary="Add strategy",
        request=StrategySerializer,
    ),
)
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
