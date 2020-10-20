from core.models import TimeStampedModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Exchange(TimeStampedModel):
    code = models.CharField(_("code"), max_length=50)
    name = models.CharField(_("name"), max_length=50)
    name_zh = models.CharField(_("chinese name"), max_length=100, blank=True)
    logo = models.ImageField(_("logo"), upload_to="exchanges/logos", blank=True)
    logo_thumbnail = ImageSpecField(
        source="logo",
        processors=[ResizeToFill(32, 32)],
        format="png",
        options={"quality": 100},
    )
    active = models.BooleanField(_("active"), default=False)
    rank = models.SmallIntegerField(_("rank"), default=0)

    class Meta:
        verbose_name = _("exchange")
        verbose_name_plural = _("exchanges")
        ordering = ["rank", "-created_at"]


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name_zh:
            self.name_zh = self.name
        super().save(*args, **kwargs)
