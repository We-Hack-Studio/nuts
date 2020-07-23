from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_cryptography.fields import encrypt

from core.models import TimeStampedModel


class Credential(TimeStampedModel):
    note = models.CharField(_("note"), max_length=20, blank=True)
    api_key = encrypt(models.CharField(_("API Key"), max_length=50))
    secret = encrypt(models.CharField(_("secret"), max_length=50))
    passphrase = encrypt(models.CharField(_("passphrase"), max_length=30, blank=True))
    is_test_net = models.BooleanField(_("is test net"), default=False)
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

    def __str__(self):
        return self.note
