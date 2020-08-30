from typing import Type

from core.mixins import ApiErrorsMixin
from django.utils import timezone
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer, Serializer

from .models import Robot
from .serializers import (
    AssetRecordSerializer,
    RobotConfigSerializer,
    RobotListSerializer,
    RobotRetrieveSerializer,
)


class RobotStrategyParametersSerializer(Serializer):
    strategy_parameters = serializers.JSONField(binary=True)


class RobotViewSet(
    ApiErrorsMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = RobotListSerializer
    permission_classes = [IsAdminUser]
    pagination_class = None
    action_serializer_map = {
        "retrieve": RobotRetrieveSerializer,
    }

    def get_queryset(self):
        return (
            Robot.objects.all()
            .select_related("credential__user", "credential__exchange", "asset_record")
            .order_by("-created_at")
        )

    def get_serializer_class(self) -> Type[BaseSerializer]:
        return self.action_serializer_map.get(
            self.action, super().get_serializer_class()
        )

    @action(
        methods=["GET"],
        detail=True,
        serializer_class=RobotConfigSerializer,
        permission_classes=[IsAdminUser],
        url_name="config",
        url_path="config",
    )
    def retrieve_config(self, request, *args, **kwargs) -> Response:
        robot = self.get_object()
        serializer = self.get_serializer(instance=robot)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=True,
        url_path="ping",
        permission_classes=[IsAdminUser],
    )
    def ping(self, request, *args, **kwargs) -> Response:
        robot = self.get_object()
        robot.ping_time = timezone.now()
        robot.save(update_fields=["ping_time"])
        return Response({"detail": "pong"}, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=True,
        url_path="strategyParameters",
        url_name="strategy-parameters",
        permission_classes=[IsAdminUser],
        serializer_class=RobotStrategyParametersSerializer,
    )
    def adjust_strategy_parameters(self, request, *args, **kwargs) -> Response:
        robot = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        parameters = serializer.validated_data["strategy_parameters"]
        robot.strategy_parameters.update(parameters)
        robot.save(update_fields=["strategy_parameters"])
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)

    @action(
        methods=["PATCH"],
        detail=True,
        url_path="assetRecord",
        url_name="asset-record",
        permission_classes=[IsAdminUser],
        serializer_class=AssetRecordSerializer,
    )
    def partial_update_asset_record(self, request, *args, **kwargs) -> Response:
        robot = self.get_object()
        asset_record = robot.asset_record
        serializer = self.get_serializer(instance=asset_record, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)
