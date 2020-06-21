from rest_framework import serializers
from core.serializers import RoundedFloatField, PercentageField
from .models import Asset
from core.utils import round_value_by_currency


class RobotAssetSerializer(serializers.Serializer):
    pnl_24h_abs = serializers.FloatField(source="asset_pnl_24h_abs", read_only=True)
    pnl_24h_rel = serializers.FloatField(source="asset_pnl_24h_rel", read_only=True)
    pnl_24h_rel_ptg = PercentageField(source="asset_pnl_24h_rel", read_only=True)
    profit_ratio = RoundedFloatField(
        source="asset_profit_ratio", precision=4, read_only=True
    )
    profit_ratio_ptg = PercentageField(source="asset_profit_ratio", read_only=True)
    profit = serializers.FloatField(source="asset_profit", read_only=True)
    balance = serializers.FloatField(source="asset_balance", read_only=True)
    capital = serializers.FloatField(source="asset_capital", read_only=True)

    def to_representation(self, instance):
        result = super().to_representation(instance)
        for field in [
            "balance",
            "capital",
            "profit",
            "pnl_24h_abs",
        ]:
            result[field] = round_value_by_currency(
                value=result[field], currency=instance.margin_currency
            )

        return result


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = [
            "capital",
            "balance",
        ]
