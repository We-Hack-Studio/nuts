from typing import Type

from django.db.models import F
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from .models import Robot
from .serializers import (
    AssetRecordSerializer,
    RobotCreateSerializer,
    RobotListSerializer,
    RobotRetrieveSerializer,
    RobotUpdateSerializer,
)


class RobotViewSet(viewsets.ModelViewSet):
    serializer_class = RobotListSerializer
    permission_classes = [IsAdminUser]
    pagination_class = None
    action_serializer_map = {
        "list": RobotListSerializer,
        "retrieve": RobotRetrieveSerializer,
        "create": RobotCreateSerializer,
        "update": RobotUpdateSerializer,
        "partial_update": RobotUpdateSerializer,
        "update_asset_record": AssetRecordSerializer,
    }
    resource_name = "robots"

    def get_queryset(self):
        qs = Robot.objects.filter(credential__user=self.request.user).order_by(
            "-created_at"
        )
        if self.action in {"list"}:
            qs = qs.annotate(strategy_name=F("strategy__name"))
        return qs

    def get_serializer_class(self) -> Type[BaseSerializer]:
        assert self.action in self.action_serializer_map
        return self.action_serializer_map[self.action]

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
        methods=["GET"],
        detail=True,
        url_path="strategyParameters",
        url_name="strategy-parameters",
        permission_classes=[IsAdminUser],
    )
    def strategy_parameters(self, request, *args, **kwargs) -> Response:
        robot = self.get_object()
        return Response(robot.strategy_parameters, status=status.HTTP_200_OK)

    @strategy_parameters.mapping.post
    def adjust_strategy_parameters(self, request, *args, **kwargs) -> Response:
        robot = self.get_object()
        # todo: validate by specification
        strategy_parameters = request.data.copy()
        del strategy_parameters["id"]
        robot.strategy_parameters.update(strategy_parameters)
        robot.save(update_fields=["strategy_parameters"])
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)

    @action(
        methods=["GET"],
        detail=True,
        url_path="strategySpecView",
        url_name="strategy-spec-view",
        permission_classes=[IsAdminUser],
    )
    def retrieve_strategy_spec_view(self, request, *args, **kwargs) -> Response:
        robot = self.get_object()
        return Response(robot.strategy_spec_view, status=status.HTTP_200_OK)

    @action(
        methods=["GET"],
        detail=True,
        url_path="credentialKeys",
        url_name="credential-keys",
        permission_classes=[IsAdminUser],
    )
    def retrieve_credential_keys(self, request, *args, **kwargs) -> Response:
        robot = self.get_object()
        return Response(robot.credential.keys, status=status.HTTP_200_OK)

    @action(
        methods=["PATCH"],
        detail=True,
        url_path="assetRecord",
        url_name="asset-record",
        permission_classes=[IsAdminUser],
        serializer_class=AssetRecordSerializer,
    )
    def update_asset_record(self, request, *args, **kwargs) -> Response:
        robot = self.get_object()
        asset_record = robot.asset_record
        serializer = self.get_serializer(instance=asset_record, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)
