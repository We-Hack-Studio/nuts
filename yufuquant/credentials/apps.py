from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CredentialsConfig(AppConfig):
    name = "credentials"
    verbose_name = _("Credentials")

    def ready(self):
        pass
