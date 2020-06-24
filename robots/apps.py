from django.apps import AppConfig


class RobotsConfig(AppConfig):
    name = "robots"
    verbose_name = "机器人"

    def ready(self):
        try:
            from . import signals
        except ImportError:
            pass
