from django.apps import AppConfig


class AssetsConfig(AppConfig):
    name = "assets"
    verbose_name = "资产"

    def ready(self):
        try:
            from . import signals
        except ImportError:
            pass
