from django.db import models

from core.models import TimeStampedModel


class Asset(TimeStampedModel):
    principal = models.FloatField("本金", default=0)
    balance = models.FloatField("余额", default=0)
    currency = models.CharField("币种", max_length=10)
    credential = models.ForeignKey(
        "credentials.Credential",
        verbose_name="交易所凭证",
        on_delete=models.CASCADE,
        related_name="assets",
    )

    class Meta:
        verbose_name = "资产"
        verbose_name_plural = verbose_name
