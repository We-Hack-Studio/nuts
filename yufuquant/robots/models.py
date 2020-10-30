from core.models import TimeStampedModel
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from jsonfield import JSONField
from model_utils.choices import Choices

from .managers import RobotManager


# Why inherit models.Model?
# see https://github.com/typeddjango/django-stubs/issues/68
class Robot(TimeStampedModel, models.Model):
    MARKET_TYPE = Choices(
        ("spots", _("Spots")),
        ("margin", _("Margin")),
        ("linear_delivery", _("Linear delivery contract")),
        ("linear_perpetual", _("Linear perpetual contract")),
        ("inverse_delivery", _("Inverse delivery contract")),
        ("inverse_perpetual", _("Inverse perpetual contract")),
    )

    name = models.CharField(_("name"), max_length=50)
    pair = models.CharField(_("pair"), max_length=30)
    market_type = models.CharField(_("market type"), max_length=30, choices=MARKET_TYPE)
    enabled = models.BooleanField(_("enabled"), default=False)
    start_time = models.DateTimeField(_("start time"), null=True, blank=True)
    ping_time = models.DateTimeField(_("ping time"), null=True, blank=True)
    credential = models.ForeignKey(
        "credentials.Credential",
        verbose_name=_("exchange credential"),
        on_delete=models.CASCADE,
        related_name="robots",
    )
    strategy = models.ForeignKey(
        "strategies.Strategy",
        verbose_name=_("strategy"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="robots",
    )
    strategy_parameters = JSONField(_("strategy parameters"), blank=True, default={})
    target_currency = models.CharField(_("target currency"), max_length=10, blank=True)
    # for spots
    base_currency = models.CharField(_("base currency"), max_length=10, blank=True)
    quote_currency = models.CharField(_("quote currency"), max_length=10, blank=True)

    objects: RobotManager = RobotManager()

    class Meta:
        verbose_name = _("robot")
        verbose_name_plural = _("robots")

    @cached_property
    def duration(self):
        if self.start_time and self.ping_time:
            return self.ping_time - self.start_time

    @property
    def duration_display(self) -> str:
        duration = self.duration
        if duration is None:
            return ""

        days = duration.days
        seconds = duration.seconds
        hours = seconds // 3600
        return _("{days}d {hours}h".format(days=days, hours=hours))

    @property
    def duration_in_second(self) -> int:
        duration = self.duration
        if duration is None:
            return -1

        return duration.seconds

    @property
    def strategy_spec_view(self):
        spec = self.strategy.specification
        parameters = self.strategy_parameters
        for parameter in spec["parameters"]:
            parameter["value"] = parameters[parameter["code"]]
        return spec


class AssetRecord(TimeStampedModel, models.Model):
    currency = models.CharField(_("currency"), max_length=10)
    total_principal = models.FloatField(_("total principal"), default=0)
    total_balance = models.FloatField(_("total balance"), default=0)
    total_principal_24h_ago = models.FloatField(
        _("total principal 24 hours ago"), default=0
    )
    total_balance_24h_ago = models.FloatField(
        _("total balance 24 hours ago"), default=0
    )
    robot = models.OneToOneField(
        Robot,
        verbose_name=_("robot"),
        on_delete=models.CASCADE,
        related_name="asset_record",
    )

    class Meta:
        verbose_name = _("asset record")
        verbose_name_plural = _("asset records")

    @property
    def total_pnl_abs(self):
        return self.total_balance - self.total_principal

    @property
    def total_pnl_rel(self):
        if not self.total_principal:
            return 0
        return self.total_pnl_abs / self.total_principal

    @property
    def total_pnl_abs_24h(self):
        return self.total_principal_24h_ago - self.total_balance_24h_ago

    @property
    def total_pnl_rel_24h(self):
        if not self.total_principal_24h_ago:
            return 0
        return self.total_pnl_abs_24h / self.total_principal_24h_ago


class AssetRecordSnap(TimeStampedModel, models.Model):
    PERIOD = Choices(
        ("1h", "h1", _("1 hour")),
        ("1d", "d1", _("1 day")),
    )

    total_principal = models.FloatField(_("total capital"))
    total_balance = models.FloatField(_("total balance"))
    period = models.CharField(_("period"), max_length=10, choices=PERIOD)
    asset_record = models.ForeignKey(
        AssetRecord,
        verbose_name=_("asset record"),
        related_name="snaps",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("asset record snap")
        verbose_name_plural = _("asset record snaps")
