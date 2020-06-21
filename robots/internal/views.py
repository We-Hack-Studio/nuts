from datetime import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from grids.models import Grid
from grids.serializers import GridSerializer
from robots.serializers import RobotConfigSerializer

from ..forms import RobotForm
from ..models import Robot
from ..serializers import RobotSerializer
from rest_framework.permissions import IsAdminUser


class RobotViewSet(
    mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet,
):
    serializer_class = RobotSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Robot.objects.all()

    @action(
        methods=["GET"],
        detail=True,
        serializer_class=GridSerializer,
        url_path="grids",
        url_name="grid",
    )
    def list_grids(self, request, *args, **kwargs):
        robot = self.get_object()
        grids = robot.grids.all().order_by("entry_price")
        serializer = self.get_serializer(instance=grids, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["GET"], detail=True, serializer_class=RobotConfigSerializer,
    )
    def config(self, request, *args, **kwargs):
        robot = self.get_object()
        serializer = self.get_serializer(instance=robot)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, url_path="logs")
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
