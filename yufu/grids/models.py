from django.db import models
from model_utils.fields import AutoCreatedField, AutoLastModifiedField

from core.models import TimeStampedModel


class GridStrategyParameter(TimeStampedModel):
    DEFAULTS = {
        "min_price": 0,
        "max_price": 0,
        "num_grids": 0,
        "max_leverage": 0,
        "principal": 0,
        "take_profit_range": 0,
    }
    min_price = models.FloatField("最低价格")
    max_price = models.FloatField("最高价格")
    num_grids = models.IntegerField("网格数量")
    max_leverage = models.FloatField("最大杠杆")
    principal = models.FloatField("投入本金")
    take_profit_range = models.FloatField("止盈间距")
    robot = models.OneToOneField(
        "robots.Robot",
        verbose_name="机器人",
        related_name="grid_strategy_parameter",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "网格策略参数"
        verbose_name_plural = verbose_name

    def reset_to_defaults(self):
        for field_name, default_value in self.DEFAULTS:
            setattr(self, field_name, default_value)
        self.save(update_fields=self.DEFAULTS.keys())


class Grid(models.Model):
    entry_qty = models.FloatField("仓位数量")
    entry_price = models.FloatField("入场价格")
    exit_price = models.FloatField("出场价格")
    filled_qty = models.FloatField("已开仓数量")
    created_at = AutoCreatedField("创建于")
    modified_at = AutoLastModifiedField("修改于")
    level = models.IntegerField("层")
    robot = models.ForeignKey(
        "robots.Robot",
        verbose_name="机器人",
        related_name="grids",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "网格"
        verbose_name_plural = verbose_name

    @property
    def holding(self):
        return self.filled_qty > 0
