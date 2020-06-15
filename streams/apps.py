from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StreamsConfig(AppConfig):
    name = "streams"
    verbose_name = _("Streams")

    def ready(self):
        pass
