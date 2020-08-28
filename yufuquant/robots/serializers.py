from typing import Any, Dict

from credentials.serializers import CredentialKeysSerializer
from exchanges.serializers import ExchangeSerializer
from rest_framework import serializers
from rest_framework.fields import DurationField as DrfDurationField
from rest_framework.serializers import FloatField
from users.serializers import UserSerializer

from .models import AssetRecord, Robot


class DurationField(DrfDurationField):
    def to_representation(self, value):
        days = value.days
        seconds = value.secondsø
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
    exchange = ExchangeSerializer(source="credential.exchange", read_only=True)
    duration_display = DurationField(source="duration", read_only=True)
    asset_record = AssetRecordSerializer(read_only=True)
    strategy_template_name = serializers.CharField(read_only=True)

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
            "strategy_template",
            "strategy_template_name",
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
            "strategy_template": {"write_only": True},
        }


class RobotRetrieveSerializer(serializers.ModelSerializer):
    user = UserSerializer(source="credential.user", read_only=True)
    exchange = ExchangeSerializer(source="credential.exchange", read_only=True)
    duration_display = DurationField(source="duration", read_only=True)
    asset_record = AssetRecordSerializer(read_only=True)
    strategy_parameters = serializers.JSONField(read_only=True)
    strategy_view = serializers.SerializerMethodField()

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
            "strategy_template",
            "strategy_parameters",
            "strategy_view",
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

    def get_strategy_view(self, obj: Robot) -> Dict[str, Any]:
        spec = obj.strategy_template.parameter_spec
        parameters = obj.strategy_parameters
        for field in spec["fields"]:
            field["value"] = parameters["fields"][field["code"]]
        return spec


class RobotConfigSerializer(serializers.ModelSerializer):
    user = UserSerializer(source="credential.user", read_only=True)
    exchange = ExchangeSerializer(source="credential.exchange", read_only=True)
    credential_keys = CredentialKeysSerializer(source="credential", read_only=True)
    is_test_net = serializers.BooleanField(
        source="credential.is_test_net", read_only=True
    )
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
