from django.apps import AppConfig


class CredentialsConfig(AppConfig):
    name = "credentials"
    verbose_name = "交易所凭证"

    def ready(self):
        try:
            from . import signals
        except ImportError:
            pass
