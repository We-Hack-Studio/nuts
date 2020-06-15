from rest_framework import mixins, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_bulk import mixins as bulk_mixins

from .models import Grid
from .serializers import GridSerializer


class GridMakeInputSerializer(serializers.Serializer):
    max_price = serializers.FloatField(min_value=0)
    min_price = serializers.FloatField(min_value=0)
    take_profit_range = serializers.IntegerField()
    num_grids = serializers.IntegerField(min_value=1)
    capital = serializers.FloatField()
    leverage = serializers.FloatField()

    def make(self):
        min_price = self.validated_data["min_price"]
        max_price = self.validated_data["max_price"]
        num_grids = self.validated_data["num_grids"]
        capital = self.validated_data["capital"]
        leverage = self.validated_data["leverage"]
        take_profit_range = self.validated_data["take_profit_range"]

        price_diff = max_price - min_price
        spacing = int(price_diff / num_grids)
        grid_qty = self._cal_grid_qty(
            min_price=min_price,
            spacing=spacing,
            num_grids=num_grids,
            capital=capital,
            leverage=leverage,
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
                "index": i,
            }
            grid = Grid(**kwargs)
            grids.append(grid)

        Grid.objects.bulk_create(grids, batch_size=100)

    @staticmethod
    def _cal_grid_qty(*, min_price, spacing, num_grids, capital, leverage):
        m = capital
        n = 0
        for i in range(0, num_grids):
            n += 1 / (min_price + i * spacing)
        qty = int(m / n)
        return qty * leverage

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        return validated_data


class GridViewSet(
    mixins.ListModelMixin,
    bulk_mixins.BulkCreateModelMixin,
    bulk_mixins.BulkUpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = GridSerializer
    lookup_value_regex = "[0-9]+"

    def get_queryset(self):
        return Grid.objects.all().order_by("index")

    @action(methods=["POST"], detail=False, url_path="clear")
    def clear(self, request, *args, **kwargs):
        grids = Grid.objects.all()
        if any(grid.holding for grid in grids):
            return Response({"detail": "有已开仓网格，不能删除"}, status=400)
        grids.delete()
        return Response({"detail": "ok"}, status=200)

    @action(
        methods=["POST"],
        detail=False,
        url_path="make",
        serializer_class=GridMakeInputSerializer,
    )
    def make(self, request, *args, **kwargs):
        if Grid.objects.exists():
            return Response({"detail": "请清除已有网格再创建"}, status=400)
        serializer: GridMakeInputSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.make()
        return Response({"detail": "ok"}, status=200)


# class GridParameterViewSet(
#     mixins.ListModelMixin,
#     mixins.CreateModelMixin,
#     mixins.UpdateModelMixin,
#     viewsets.GenericViewSet,
# ):
#     serializer_class = GridParameterSerializer
#
#     def get_queryset(self):
#         return GridParameter.objects.all()
