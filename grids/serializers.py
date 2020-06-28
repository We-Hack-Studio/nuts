from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin

from .models import Grid, GridStrategyParameter


class GridStrategyParameterSerializer(serializers.ModelSerializer):
    min_price = serializers.FloatField(min_value=0)
    max_price = serializers.FloatField(min_value=0)
    num_grids = serializers.IntegerField(min_value=1)
    principal = serializers.FloatField()
    max_leverage = serializers.FloatField()
    take_profit_range = serializers.IntegerField()

    class Meta:
        model = GridStrategyParameter
        fields = [
            "id",
            "min_price",
            "max_price",
            "num_grids",
            "max_leverage",
            "principal",
            "take_profit_range",
            "created_at",
            "modified_at",
        ]
        read_only_fields = [
            "created_at",
            "modified_at",
        ]

    def make_grids(self):
        min_price = self.validated_data["min_price"]
        max_price = self.validated_data["max_price"]
        num_grids = self.validated_data["num_grids"]
        principal = self.validated_data["principal"]
        max_leverage = self.validated_data["max_leverage"]
        take_profit_range = self.validated_data["take_profit_range"]

        price_diff = max_price - min_price
        spacing = int(price_diff / num_grids)
        grid_qty = self._cal_grid_qty(
            min_price=min_price,
            spacing=spacing,
            num_grids=num_grids,
            principal=principal,
            max_leverage=max_leverage,
        )
        grids = []
        for i in range(0, num_grids):
            entry_price = min_price + i * spacing
            exit_price = entry_price - take_profit_range
            kwargs = {
                "entry_qty": grid_qty,
                "entry_price": entry_price,
                "exit_price": exit_price,
                "filled_qty": 0,
                "level": i + 1,
                "robot": self.instance.robot,
            }
            grid = Grid(**kwargs)
            grids.append(grid)

        Grid.objects.bulk_create(grids, batch_size=100)

    @staticmethod
    def _cal_grid_qty(*, min_price, spacing, num_grids, principal, max_leverage):
        m = principal
        n = 0
        for i in range(0, num_grids):
            n += 1 / (min_price + i * spacing)
        qty = int(m / n)
        return qty * max_leverage


class GridSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Grid
        list_serializer_class = BulkListSerializer
        fields = [
            "id",
            "level",
            "entry_price",
            "exit_price",
            "filled_qty",
            "entry_qty",
            "holding",
            "robot",
        ]
