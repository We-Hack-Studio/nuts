from django.apps import AppConfig


class PositionsConfig(AppConfig):
    name = "positions"
    verbose_name = "仓位"

    def ready(self):
        try:
            from . import signals
        except ImportError:
            pass
