from exchanges.serializers import ExchangeSerializer
from rest_framework import serializers
from rest_framework.serializers import FloatField

from .models import AssetRecord, AssetRecordSnap, Robot


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
    strategy_name = serializers.CharField(read_only=True)
    asset_record = AssetRecordSerializer(read_only=True)
    exchange = ExchangeSerializer(source="credential.exchange", read_only=True)

    class Meta:
        model = Robot
        fields = [
            # plain model fields
            "id",
            "name",
            "pair",
            "market_type",
            "enabled",
            "start_time",
            "ping_time",
            "target_currency",
            "base_currency",
            "quote_currency",
            "created_at",
            "modified_at",
            # related model fields
            "asset_record",
            # derived fields
            "duration_display",
            "duration_in_second",
            "duration",
            "strategy_name",
            "exchange",
        ]


class RobotRetrieveSerializer(serializers.ModelSerializer):
    strategy_name = serializers.CharField(read_only=True)
    asset_record = AssetRecordSerializer(read_only=True)
    test_net = serializers.BooleanField(read_only=True)
    exchange = ExchangeSerializer(source="credential.exchange", read_only=True)
    strategy_store = serializers.JSONField()
    position_store = serializers.JSONField()
    order_store = serializers.JSONField()
    market_type_display = serializers.CharField(source="get_market_type_display")

    class Meta:
        model = Robot
        fields = [
            # plain model fields
            "id",
            "name",
            "pair",
            "market_type",
            "enabled",
            "start_time",
            "ping_time",
            "target_currency",
            "base_currency",
            "quote_currency",
            "strategy_store",
            "position_store",
            "order_store",
            "created_at",
            "modified_at",
            # related fields
            "asset_record",
            # derived fields
            "duration_display",
            "duration_in_second",
            "strategy_name",
            "test_net",
            "exchange",
            "market_type_display",
        ]


class RobotCreateSerializer(serializers.ModelSerializer):
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
            "credential",
            "strategy",
            "created_at",
            "modified_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "modified_at",
        ]


class RobotUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Robot
        fields = [
            "id",
            "name",
        ]


class AssetRecordSnapSerializer(serializers.ModelSerializer):
    currency = serializers.CharField(source="asset_record.currency")

    class Meta:
        model = AssetRecordSnap
        fields = [
            "id",
            "total_principal",
            "total_balance",
            "period",
            "currency",
            "created_at",
        ]
