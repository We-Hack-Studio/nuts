from django.db.models import (
    Case,
    ExpressionWrapper,
    F,
    FloatField,
    Manager,
    QuerySet,
    Value,
    When,
)


class RobotQuerySet(QuerySet):
    def with_stats(self):
        return self.filter(
            # 资产
            credential__assets__credential_id=F("credential_id"),
            credential__assets__currency=F("margin_currency"),
        ).annotate(
            asset_balance=F("credential__assets__balance"),
            asset_principal=F("credential__assets__principal"),
            asset_profit=F("asset_balance") - F("asset_principal"),
            asset_profit_ratio=ExpressionWrapper(
                F("asset_balance") * 1.0 / F("asset_principal") - 1,
                output_field=FloatField(),
            ),
        )


class RobotManager(Manager.from_queryset(RobotQuerySet)):
    pass
