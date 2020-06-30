from rest_framework import serializers
from rest_framework.fields import DurationField as DrfDurationField
from rest_framework.serializers import FloatField

from credentials.serializers import CredentialKeysSerializer
from exchanges.serializers import ExchangeSerializer
from users.serializers import UserSerializer

from .models import Robot


class DurationField(DrfDurationField):
    def to_representation(self, value):
        days = value.days
        seconds = value.seconds
        hours = seconds // 3600
        return f"{days}天{hours}小时"


class PercentageField(FloatField):
    def to_representation(self, value):
        result = super().to_representation(value)
        return "{:.2%}".format(result)


class RobotSerializer(serializers.ModelSerializer):
    user = UserSerializer(source="credential.user", read_only=True)
    exchange = ExchangeSerializer(source="credential.exchange", read_only=True)
    duration_display = DurationField(source="duration", read_only=True)
    balance = serializers.FloatField(source="asset_balance", read_only=True)
    profit_ratio_ptg = PercentageField(source="asset_profit_ratio", read_only=True)
    test_net = serializers.BooleanField(source="credential.test_net", read_only=True)

    class Meta:
        model = Robot
        fields = [
            "id",
            "name",
            "pair",
            "margin_currency",
            "enabled",
            "test_net",
            "start_time",
            "ping_time",
            "duration_display",
            "profit_ratio_ptg",
            "order_sync_ts",
            "balance",
            "credential",
            "user",
            "exchange",
            "stream_key",
            "created_at",
            "modified_at",
        ]
        read_only_fields = [
            "ping_time",
            "stream_key",
            "created_at",
            "modified_at",
        ]
        extra_kwargs = {
            "credential": {"write_only": True},
        }


class RobotConfigSerializer(serializers.ModelSerializer):
    user = UserSerializer(source="credential.user", read_only=True)
    exchange = ExchangeSerializer(source="credential.exchange", read_only=True)
    credential_keys = CredentialKeysSerializer(source="credential", read_only=True)
    principal = serializers.FloatField(source="asset_principal", read_only=True)
    position_id = serializers.IntegerField(source="position.id", read_only=True)
    asset_id = serializers.IntegerField(read_only=True)
    test_net = serializers.BooleanField(source="credential.test_net", read_only=True)

    class Meta:
        model = Robot
        fields = [
            "id",
            "name",
            "pair",
            "margin_currency",
            "enabled",
            "order_sync_ts",
            "test_net",
            "user",
            "exchange",
            "position_id",
            "asset_id",
            "credential_keys",
            "principal",
            "stream_key",
        ]
