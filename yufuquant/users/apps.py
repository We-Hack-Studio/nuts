from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "users"
    verbose_name = "用户"

    def ready(self):
        try:
            from . import signals
        except ImportError:
            pass
