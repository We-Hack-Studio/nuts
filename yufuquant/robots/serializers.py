from typing import Any, Dict

from credentials.serializers import CredentialKeysSerializer
from exchanges.serializers import ExchangeSerializer
from rest_framework.fields import DurationField as DrfDurationField
from rest_framework.serializers import FloatField
from rest_framework_json_api import serializers
from users.serializers import UserSerializer

from .models import AssetRecord, Robot


class DurationField(DrfDurationField):
    def to_representation(self, value):
        days = value.days
        seconds = value.seconds
        hours = seconds // 3600
        return f"{days}天{hours}小时"


class PercentageField(FloatField):
    def to_representation(self, value):
        result = super().to_representation(value)
        return "{:.2f}%".format(result * 100)


class AssetRecordSerializer(serializers.ModelSerializer):
    total_pnl_abs = serializers.FloatField(read_only=True)
    total_pnl_abs_24h = serializers.FloatField(read_only=True)
    total_pnl_rel_ptg = PercentageField(source="total_pnl_rel", read_only=True)
    total_pnl_rel_ptg_24h = PercentageField(source="total_pnl_rel_24h", read_only=True)

    class Meta:
        model = AssetRecord
        resource_name = "asset_records"
        fields = [
            "currency",
            "total_principal",
            "total_balance",
            "total_pnl_abs",
            "total_pnl_abs_24h",
            "total_pnl_rel_ptg",
            "total_pnl_rel_ptg_24h",
        ]
        read_only_fields = [
            "currency",
            "total_principal_24h_ago",
            "total_balance_24h_ago",
            "robot",
        ]


class RobotListSerializer(serializers.ModelSerializer):
    included_serializers = {
        "exchange": ExchangeSerializer,
        "asset_record": AssetRecordSerializer,
    }
    duration_display = DurationField(source="duration", read_only=True)
    strategy_name = serializers.CharField(read_only=True)
    exchange = ExchangeSerializer(source="credential.exchange", read_only=True)

    class Meta:
        model = Robot
        fields = [
            "id",
            "name",
            "pair",
            "market_type",
            "target_currency",
            "base_currency",
            "quote_currency",
            "enabled",
            "start_time",
            "ping_time",
            "duration_display",
            "asset_record",
            "credential",
            "strategy",
            "strategy_name",
            "exchange",
            "created_at",
            "modified_at",
        ]
        read_only_fields = [
            "ping_time",
            "asset_record",
            "created_at",
            "modified_at",
        ]
        extra_kwargs = {
            "credential": {"write_only": True},
            "strategy": {"write_only": True},
        }

    class JSONAPIMeta:
        resource_name = "robots"
        included_resources = ["exchange", "asset_record"]


class RobotRetrieveSerializer(serializers.ModelSerializer):
    included_serializers = {
        "exchange": ExchangeSerializer,
        "asset_record": AssetRecordSerializer,
        "user": UserSerializer,
    }
    user = UserSerializer(source="credential.user", read_only=True)
    exchange = ExchangeSerializer(source="credential.exchange", read_only=True)
    duration_display = DurationField(source="duration", read_only=True)
    asset_record = AssetRecordSerializer(read_only=True)
    strategy_parameters = serializers.JSONField(read_only=True)
    strategy_parameters_view = serializers.SerializerMethodField()

    class Meta:
        model = Robot
        fields = [
            "id",
            "name",
            "pair",
            "target_currency",
            "base_currency",
            "quote_currency",
            "enabled",
            "start_time",
            "ping_time",
            "duration_display",
            "asset_record",
            "credential",
            "strategy_parameters",
            "strategy_parameters_view",
            "user",
            "exchange",
            "created_at",
            "modified_at",
        ]
        read_only_fields = [
            "ping_time",
            "created_at",
            "modified_at",
        ]
        extra_kwargs = {
            "credential": {"write_only": True},
        }

    class JSONAPIMeta:
        resource_name = "robots"
        included_resources = ["exchange", "asset_record", "user"]

    def get_strategy_parameters_view(self, obj: Robot) -> Dict[str, Any]:
        spec = obj.strategy.specification
        parameters = obj.strategy_parameters
        for parameter in spec["parameters"]:
            parameter["value"] = parameters[parameter["code"]]
        return spec


class RobotConfigSerializer(serializers.ModelSerializer):
    user = UserSerializer(source="credential.user", read_only=True)
    exchange = ExchangeSerializer(source="credential.exchange", read_only=True)
    credential_keys = CredentialKeysSerializer(source="credential", read_only=True)
    test_net = serializers.BooleanField(source="credential.test_net", read_only=True)
    strategy_parameters = serializers.JSONField()

    class Meta:
        model = Robot
        fields = [
            "id",
            "name",
            "pair",
            "target_currency",
            "enabled",
            "is_test_net",
            "user",
            "exchange",
            "credential_keys",
            "strategy_parameters",
        ]

    class JSONAPIMeta:
        resource_name = "robot_configs"
