from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ExchangesConfig(AppConfig):
    name = "exchanges"
    verbose_name = _("Exchanges")
