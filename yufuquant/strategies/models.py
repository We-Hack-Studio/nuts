from core.models import TimeStampedModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from jsonfield import JSONField


class Strategy(TimeStampedModel, models.Model):
    name = models.CharField(_("name"), max_length=100, unique=True)
    description = models.TextField(_("description"), blank=True)
    specification = JSONField(_("specification"), blank=True, default={})

    class Meta:
        verbose_name = _("strategy")
        verbose_name_plural = _("strategies")

    def __str__(self):
        return self.name
