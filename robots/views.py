from datetime import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from core.utils import KeyHelper
from grids.models import Grid
from grids.serializers import GridSerializer
from robots.serializers import RobotConfigSerializer

from .models import Robot
from .serializers import RobotSerializer


class GridMakeInputSerializer(serializers.Serializer):
    min_price = serializers.FloatField(min_value=0)
    max_price = serializers.FloatField(min_value=0)
    num_grids = serializers.IntegerField(min_value=1)
    principal = serializers.FloatField()
    max_leverage = serializers.FloatField()
    take_profit_range = serializers.IntegerField()

    def make(self, robot):
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
                "index": i,
                "robot": robot,
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

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        return validated_data


class RobotViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = RobotSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = (
            Robot.objects.select_related(
                "credential__user", "credential__exchange", "position"
            )
            .with_stats()
            .order_by("-created_at")
        )
        if user.is_superuser:
            return qs
        return qs.filter(credential__user=user)

    @action(
        methods=["GET"],
        detail=True,
        serializer_class=GridSerializer,
        url_path="grids",
        url_name="grid",
        permission_classes=[IsAuthenticated],
    )
    def list_grids(self, request, *args, **kwargs):
        robot = self.get_object()
        grids = robot.grids.all().order_by("entry_price")
        serializer = self.get_serializer(instance=grids, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=True,
        serializer_class=GridMakeInputSerializer,
        url_path="grids/make",
        url_name="grid-make",
    )
    def make_grids(self, request, *args, **kwargs):
        robot = self.get_object()
        if robot.grids.exists():
            return Response({"detail": "请清除已有网格再创建"}, status=400)
        serializer: GridMakeInputSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.make(robot)
        return Response({"detail": "ok"}, status=200)

    @action(
        methods=["DELETE"], detail=True, url_path="grids/clear", url_name="grid-clear"
    )
    def clear_grids(self, request, *args, **kwargs):
        robot = self.get_object()
        grids = robot.grids.all()
        if any(grid.holding for grid in grids):
            return Response({"detail": "有已开仓网格，不能清除"}, status=400)
        grids.delete()
        return Response(status=204)

    @action(
        methods=["GET"],
        detail=True,
        serializer_class=RobotConfigSerializer,
        permission_classes=[IsAuthenticated | IsAdminUser],
    )
    def config(self, request, *args, **kwargs):
        robot = self.get_object()
        serializer = self.get_serializer(instance=robot)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=False,
        url_path="logs",
        permission_classes=[IsAuthenticated | IsAdminUser],
    )
    def send_log(self, request, *args, **kwargs):
        channel_layer = get_channel_layer()
        data = request.data
        robot_id = data["robot_id"]
        text = {
            "topic": "log",
            "robot_id": robot_id,
            "datetime": datetime.now().strftime("%H:%M:%S"),
            "data": {"msg": data["msg"]},
        }
        event = {
            "type": "robot.stream",
            "text": text,
        }
        group_name = f"robot.{robot_id}"
        async_to_sync(channel_layer.group_send)(
            group_name, event,
        )
        return Response({"detail": "ok"})

    @action(
        methods=["POST"],
        detail=True,
        url_path="ping",
        permission_classes=[IsAuthenticated | IsAdminUser],
    )
    def ping(self, request, *args, **kwargs):
        robot = self.get_object()
        now = timezone.now()
        robot.ping_time = now
        robot.save(update_fields=["ping_time"])
        return Response({"detail": "pong"}, status=status.HTTP_200_OK)
