from rest_framework import serializers

from .models import Position


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = [
            "id",
            "direction",
            "qty",
            "avg_price",
            "unrealized_pnl",
            "liq_price",
            "leverage",
            "robot",
        ]
