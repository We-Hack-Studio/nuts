from django.conf import settings
from django.db import models
from django_cryptography.fields import encrypt
from model_utils.fields import AutoCreatedField, AutoLastModifiedField

from .managers import RobotManager


class Robot(models.Model):
    name = models.CharField("名字", max_length=20)
    pair = models.CharField("交易对", max_length=15)
    margin_currency = models.CharField("保证金币种", max_length=10)
    enabled = models.BooleanField("启用", default=True)
    start_time = models.DateTimeField("启动时间", null=True)
    ping_time = models.DateTimeField("心跳时间", null=True)
    order_sync_ts = models.BigIntegerField("订单同步时间戳", null=True)
    created_at = AutoCreatedField("创建于")
    modified_at = AutoLastModifiedField("修改于")
    credential = models.ForeignKey(
        "credentials.Credential",
        verbose_name="交易所凭证",
        on_delete=models.CASCADE,
        related_name="robots",
    )
    stream_key = encrypt(models.CharField("Websocket消息密钥", max_length=300))
    objects: RobotManager = RobotManager()

    class Meta:
        verbose_name = "机器人"
        verbose_name_plural = "机器人"

    @property
    def duration(self):
        if self.start_time and self.ping_time:
            return self.ping_time - self.start_time
