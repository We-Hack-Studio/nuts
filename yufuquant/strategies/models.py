from django.db import models
from django.utils.translation import gettext_lazy as _
from jsonfield import JSONField

from core.models import TimeStampedModel


class StrategyTemplate(TimeStampedModel):
    code = models.CharField(_("code"), max_length=20, unique=True)
    name = models.CharField(_("name"), max_length=20)
    description = models.TextField(_("description"), blank=True)
    parameter_spec = JSONField(_("parameter specification"), blank=True)

    class Meta:
        verbose_name = _("strategy template")
        verbose_name_plural = _("strategy templates")

    def __str__(self):
        return self.name


class Strategy(TimeStampedModel):
    template = models.ForeignKey(
        StrategyTemplate, verbose_name=_("template"), on_delete=models.CASCADE
    )
    parameters = JSONField(_("parameters"), blank=True)

    class Meta:
        verbose_name = _("strategy")
        verbose_name_plural = _("strategies")
