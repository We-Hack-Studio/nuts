from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin

from .models import Grid, Position


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = [
            "id",
            "direction",
            "size",
            "max_position_size",
            "addition_size",
            "entry_size",
            "entry_price",
            "realized_pnl",
            "unrealized_pnl",
            "liquidation_price",
            "margin_leverage",
        ]


class GridSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    holding = serializers.BooleanField(read_only=True)

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
        ]
