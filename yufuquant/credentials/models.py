from typing import Dict

from core.models import TimeStampedModel
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_cryptography.fields import encrypt


class Credential(TimeStampedModel):
    note = models.CharField(_("note"), max_length=30, blank=True)
    api_key = encrypt(models.CharField(_("API Key"), max_length=200))
    secret = encrypt(models.CharField(_("secret"), max_length=200))
    passphrase = encrypt(models.CharField(_("passphrase"), max_length=100, blank=True))
    test_net = models.BooleanField(_("test net"), default=False)
    exchange = models.ForeignKey(
        "exchanges.Exchange",
        verbose_name=_("exchange"),
        on_delete=models.CASCADE,
        related_name="credential_set",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="credential_set",
    )

    class Meta:
        verbose_name = _("credential")
        verbose_name_plural = _("credentials")

    class JSONAPIMeta:
        resource_name = "credentials"

    def __str__(self):
        return self.note

    @property
    def keys(self) -> Dict[str, str]:
        return {
            "api_key": self.api_key,
            "secret": self.secret,
            "passphrase": self.passphrase,
        }
