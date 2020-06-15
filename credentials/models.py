from django.db import models
from django_cryptography.fields import encrypt
from model_utils.fields import AutoCreatedField, AutoLastModifiedField
from django.conf import settings


class Credential(models.Model):
    note = models.CharField("备注", max_length=20, blank=True)
    api_key = encrypt(models.CharField("API密钥", max_length=50))
    secret = encrypt(models.CharField("密钥", max_length=50))
    passphrase = encrypt(models.CharField("密码", max_length=30, blank=True))
    created_at = AutoCreatedField("创建于")
    exchange = models.ForeignKey(
        "exchanges.Exchange",
        verbose_name="交易所",
        on_delete=models.CASCADE,
        related_name="credential_set",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="用户",
        on_delete=models.CASCADE,
        related_name="credential_set",
    )

    class Meta:
        verbose_name = "交易所凭据"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.note
