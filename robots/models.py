from django.conf import settings
from django.db import models
from model_utils.fields import AutoCreatedField, AutoLastModifiedField


class Robot(models.Model):
    name = models.CharField("名字", max_length=20)
    pair = models.CharField("交易对", max_length=15)
    enable = models.BooleanField("启用", default=True)
    start_time = models.DateTimeField("启动时间", null=True)
    ping_time = models.DateTimeField("心跳时间", null=True)
    created_at = AutoCreatedField("创建于")
    modified_at = AutoLastModifiedField("修改于")
    credential = models.ForeignKey(
        "credentials.Credential",
        verbose_name="交易所凭据",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="robots",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="用户",
        on_delete=models.CASCADE,
        related_name="robots",
    )

    class Meta:
        verbose_name = "机器人"
        verbose_name_plural = "机器人"
