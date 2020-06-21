from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework_bulk import mixins as bulk_mixins

from ..filters import GridFilter
from ..models import Grid
from ..serializers import GridSerializer


class GridViewSet(
    mixins.ListModelMixin,
    bulk_mixins.BulkCreateModelMixin,
    bulk_mixins.BulkUpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = GridSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = GridFilter
    lookup_value_regex = "[0-9]+"

    def get_queryset(self):
        return Grid.objects.all().order_by("entry_price")
