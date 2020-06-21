from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin

from .models import Grid


class GridSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Grid
        list_serializer_class = BulkListSerializer
        fields = [
            "id",
            "entry_qty",
            "entry_price",
            "exit_price",
            "filled_qty",
            "index",
            "holding",
            "robot",
        ]
