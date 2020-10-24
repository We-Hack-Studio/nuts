from typing import List, Type

from credentials.serializers import CredentialKeySerializer
from django.db.models import F
from django.utils import timezone
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import BasePermission, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.settings import api_settings
from rest_framework_api_key.permissions import HasAPIKey

from .models import Robot
from .serializers import (
    AssetRecordSerializer,
    AssetRecordSnapSerializer,
    RobotCreateSerializer,
    RobotListSerializer,
    RobotRetrieveSerializer,
    RobotUpdateSerializer,
)


class RobotAssetRecordSnapPagination(LimitOffsetPagination):
    default_limit = 100


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
        "partial_update": RobotUpdateSerializer,
        "partial_update_asset_record": AssetRecordSerializer,
        "retrieve_credential_key": CredentialKeySerializer,
        "list_asset_record_snap": AssetRecordSnapSerializer,
    }

    def get_queryset(self):
        qs = Robot.objects.all().order_by("-created_at")
        if self.action in {"list"}:
            qs = qs.annotate(strategy_name=F("strategy__name"))
        if self.action in {"retrieve"}:
            qs = qs.annotate(test_net=F("credential__test_net"))
        return qs

    def get_serializer_class(self) -> Type[BaseSerializer]:
        assert self.action in self.action_serializer_map
        return self.action_serializer_map[self.action]

    def get_permissions(self) -> List[BasePermission]:
        if self.action == "adjust_strategy_parameters":
            return [IsAdminUser()]
        return super().get_permissions()

    def initialize_request(self, request, *args, **kwargs) -> Request:
        # Dynamically set `authentication_classes` for `adjust_strategy_parameters`
        # action view. Note self.action was not set before `initialize_request` invoked,
        # so we need get it from `action_map`. Here is nearest to the place where
        # request.authenticators be set.
        method = request.method.lower()
        a = self.action_map.get(method)
        if a == "adjust_strategy_parameters":
            self.authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
        return super(RobotViewSet, self).initialize_request(request, *args, **kwargs)

    @extend_schema(
        summary="Ping robot", responses={200: {"pong": "timestamp in milliseconds."}}
    )
    @action(
        methods=["POST"],
        detail=True,
        url_path="ping",
        url_name="ping",
        permission_classes=[HasAPIKey],
        authentication_classes=[],
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
        permission_classes=[HasAPIKey],
        authentication_classes=[],
    )
    def retrieve_strategy_parameters(self, request, *args, **kwargs) -> Response:
        robot = self.get_object()
        return Response(robot.strategy_parameters, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Adjust robot strategy parameters",
    )
    @retrieve_strategy_parameters.mapping.patch
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
        permission_classes=[HasAPIKey],
        authentication_classes=[],
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
        permission_classes=[HasAPIKey],
        authentication_classes=[],
        serializer_class=AssetRecordSerializer,
    )
    def partial_update_asset_record(self, request, *args, **kwargs) -> Response:
        robot = self.get_object()
        asset_record = robot.asset_record
        serializer = self.get_serializer(instance=asset_record, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Get asset record snaps",
    )
    @action(
        methods=["GET"],
        detail=True,
        url_path="assetRecordSnaps",
        url_name="asset-record-snap-list",
        permission_classes=[IsAdminUser],
        serializer_class=AssetRecordSnapSerializer,
        # todo: custom filter
        filter_backends=[],
        pagination_class=RobotAssetRecordSnapPagination,
    )
    def list_asset_record_snap(self, request, *args, **kwargs) -> Response:
        robot = self.get_object()
        asset_record = robot.asset_record
        snaps = asset_record.snaps.select_related("asset_record")
        filtered = self.filter_queryset(snaps)
        page = self.paginate_queryset(filtered)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
