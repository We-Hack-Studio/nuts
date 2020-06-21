from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.choices import Choices

from core.models import TimeStampedModel


class Position(TimeStampedModel):
    DIRECTION = Choices((-1, "short", "空"), (0, "no_position", "无"), (1, "long", "多"),)
    direction = models.SmallIntegerField(
        "方向", choices=DIRECTION, default=DIRECTION.no_position
    )
    qty = models.FloatField("数量", default=0)
    avg_price = models.FloatField("均价", default=0)
    unrealized_pnl = models.FloatField("未结盈亏", default=0)
    liq_price = models.FloatField("强平价", default=0)
    leverage = models.FloatField("杠杆", default=0)
    robot = models.OneToOneField(
        "robots.Robot", verbose_name="机器人", on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "仓位"
        verbose_name_plural = verbose_name
