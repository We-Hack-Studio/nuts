import json

from rest_framework import serializers
from rest_framework.fields import DurationField as DrfDurationField
from rest_framework.serializers import FloatField

from credentials.serializers import CredentialKeysSerializer
from exchanges.serializers import ExchangeSerializer
from strategies.serializers import StrategySerializer, StrategyTemplateSerializer
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
        return "{:.2f}%".format(result)


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


class RobotSerializer(serializers.ModelSerializer):
    user = UserSerializer(source="credential.user", read_only=True)
    exchange = ExchangeSerializer(source="credential.exchange", read_only=True)
    duration_display = DurationField(source="duration", read_only=True)
    asset_record = AssetRecordSerializer(read_only=True)
    strategy_parameters = serializers.JSONField(read_only=True)
    param_preview = serializers.SerializerMethodField()

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
            "param_preview",
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

    def get_param_preview(self, obj: Robot):
        spec = json.loads(obj.strategy_template.param_spec)
        parameters = obj.strategy_parameters
        preview = {}
        for code, field in spec["fields"].items():
            preview[code] = {
                "code": field["code"],
                "name": field.get("name", field["code"].title()),
                "type": field["type"],
                "help_text": field["help_text"],
                "value": parameters["fields"][code],
            }
        return preview


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
            # "principal",
            "strategy_parameters",
        ]
