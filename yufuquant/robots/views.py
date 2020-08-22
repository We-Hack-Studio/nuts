from typing import Type

from core.mixins import ApiErrorsMixin
from django.utils import timezone
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from robots.serializers import RobotConfigSerializer

from .models import Robot
from .serializers import RobotListSerializer, RobotRetrieveSerializer


class RobotViewSet(
    ApiErrorsMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = RobotListSerializer
    permission_classes = [IsAuthenticated]
    action_serializer_map = {
        "retrieve": RobotRetrieveSerializer,
    }

    def get_queryset(self):
        return (
            Robot.objects.filter(credential__user=self.request.user)
            .select_related("credential__user", "credential__exchange", "asset_record")
            .order_by("-created_at")
        )

    def get_serializer_class(self) -> Type[BaseSerializer]:
        return self.action_serializer_map.get(self.action, RobotListSerializer)

    @action(
        methods=["GET"],
        detail=True,
        serializer_class=RobotConfigSerializer,
        permission_classes=[IsAuthenticated],
    )
    def config(self, request, *args, **kwargs) -> Response:
        robot = self.get_object()
        serializer = self.get_serializer(instance=robot)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=True,
        url_path="ping",
        permission_classes=[IsAuthenticated],
    )
    def ping(self, request, *args, **kwargs) -> Response:
        robot = self.get_object()
        robot.ping_time = timezone.now()
        robot.save(update_fields=["ping_time"])
        return Response({"detail": "pong"}, status=status.HTTP_200_OK)
