from typing import Type

from credentials.serializers import CredentialKeySerializer
from django.db.models import F
from django.utils import timezone
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
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


@method_decorator(
    name="update",
    decorator=extend_schema(
        operation=None,
    ),
)
@method_decorator(
    name="partial_update",
    decorator=extend_schema(
        summary="Update a robot",
        request=RobotUpdateSerializer,
    ),
)
@method_decorator(
    name="create",
    decorator=extend_schema(
        summary="Create a robot",
        request=RobotCreateSerializer,
    ),
)
@method_decorator(
    name="list",
    decorator=extend_schema(
        summary="Return all robot",
        request=RobotListSerializer,
    ),
)
@method_decorator(
    name="retrieve",
    decorator=extend_schema(
        summary="Get robot detail",
        request=RobotRetrieveSerializer,
    ),
)
@method_decorator(
    name="destroy",
    decorator=extend_schema(
        summary="Delete a robot",
    ),
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
        "partial_update_asset_record": AssetRecordSerializer,
        "retrieve_credential_key": CredentialKeySerializer,
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

    @extend_schema(
        summary="Ping robot", responses={200: {"pong": "timestamp in milliseconds."}}
    )
    @action(
        methods=["POST"],
        detail=True,
        url_path="ping",
        url_name="ping",
        permission_classes=[IsAdminUser],
    )
    def ping(self, request, *args, **kwargs) -> Response:
        robot = self.get_object()
        now = timezone.now()
        robot.ping_time = now
        robot.save(update_fields=["ping_time"])
        return Response(
            {"pong": int(now.timestamp() * 1000)}, status=status.HTTP_200_OK
        )

    @extend_schema(
        summary="Get robot strategy parameters",
    )
    @action(
        methods=["GET"],
        detail=True,
        url_path="strategyParameters",
        url_name="strategy-parameters",
        permission_classes=[IsAdminUser],
    )
    def retrieve_strategy_parameters(self, request, *args, **kwargs) -> Response:
        robot = self.get_object()
        return Response(robot.strategy_parameters, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Adjust robot strategy parameters",
    )
    @retrieve_strategy_parameters.mapping.patch  # type:ignore
    def adjust_strategy_parameters(self, request, *args, **kwargs) -> Response:
        robot = self.get_object()
        # todo: validate by specification
        robot.strategy_parameters.update(request.data)
        robot.save(update_fields=["strategy_parameters"])
        return Response(robot.strategy_parameters, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Get robot strategy specification view",
    )
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

    @extend_schema(
        summary="Get robot exchange credential key",
    )
    @action(
        methods=["GET"],
        detail=True,
        url_path="credentialKey",
        url_name="credential-key",
        permission_classes=[IsAdminUser],
    )
    def retrieve_credential_key(self, request, *args, **kwargs) -> Response:
        robot = self.get_object()
        return Response(robot.credential.key, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update robot asset record",
    )
    @action(
        methods=["PATCH"],
        detail=True,
        url_path="assetRecord",
        url_name="asset-record",
        permission_classes=[IsAdminUser],
        serializer_class=AssetRecordSerializer,
        resource_name="asset_records",
    )
    def partial_update_asset_record(self, request, *args, **kwargs) -> Response:
        robot = self.get_object()
        asset_record = robot.asset_record
        serializer = self.get_serializer(instance=asset_record, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
