from django.db import models
from django.utils.translation import gettext_lazy as _
from jsonfield import JSONField
from model_utils.choices import Choices

from core.models import TimeStampedModel

from .managers import RobotManager


class Robot(TimeStampedModel):
    MARKET_TYPE = Choices(("spots", _("spots")), ("futures", _("futures")))

    name = models.CharField(_("name"), max_length=20)
    pair = models.CharField(_("pair"), max_length=15)
    market_type = models.CharField(_("market type"), max_length=10, choices=MARKET_TYPE)
    enabled = models.BooleanField(_("enabled"), default=True)
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
    strategy_parameters = JSONField(_("strategy parameters"))
    target_currency = models.CharField(_("target currency"), max_length=10, blank=True)
    # for spots
    base_currency = models.CharField(_("base currency"), max_length=10, blank=True)
    quote_currency = models.CharField(_("quote currency"), max_length=10, blank=True)

    objects: RobotManager = RobotManager()

    class Meta:
        verbose_name = _("robot")
        verbose_name_plural = _("robots")

    class JSONAPIMeta:
        resource_name = "robots"
    @property
    def duration(self):
        if self.start_time and self.ping_time:
            return self.ping_time - self.start_time


class AssetRecord(TimeStampedModel):
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
