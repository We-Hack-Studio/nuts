from rest_framework import serializers
from rest_framework.fields import DurationField as DrfDurationField

from credentials.serializers import CredentialKeysSerializer
from exchanges.serializers import ExchangeSerializer

from .models import Robot
from rest_framework.serializers import FloatField


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
    exchange = ExchangeSerializer(source="credential.exchange", read_only=True)
    duration_display = DurationField(source="duration", read_only=True)
    profit_ratio_ptg = PercentageField(source="asset_profit_ratio", read_only=True)

    class Meta:
        model = Robot
        fields = [
            "id",
            "name",
            "pair",
            "margin_currency",
            "enable",
            "start_time",
            "ping_time",
            "duration_display",
            "profit_ratio_ptg",
            "credential",
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


class RobotConfigSerializer(serializers.ModelSerializer):
    credential_keys = CredentialKeysSerializer(source="credential", read_only=True)

    class Meta:
        model = Robot
        fields = [
            "id",
            "name",
            "pair",
            "enable",
            "credential_keys",
        ]
