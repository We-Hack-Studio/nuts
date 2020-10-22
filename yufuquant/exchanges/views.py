from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets

from .models import Exchange
from .serializers import ExchangeSerializer


@method_decorator(
    name="list",
    decorator=extend_schema(
        summary="Return all exchanges",
    ),
)
class ExchangeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ExchangeSerializer
    pagination_class = None

    def get_queryset(self):
        return Exchange.objects.all().order_by("-created_at")
