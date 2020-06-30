from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from model_utils.fields import AutoCreatedField, AutoLastModifiedField


class Exchange(models.Model):
    code = models.CharField("代码", max_length=20)
    name = models.CharField("名字", max_length=20)
    name_zh = models.CharField("中文名", max_length=20, blank=True)
    created_at = AutoCreatedField("创建于")
    modified_at = AutoLastModifiedField("修改于")
    logo = models.ImageField(upload_to="exchanges/logos", blank=True)
    logo_thumbnail = ImageSpecField(
        source="logo",
        processors=[ResizeToFill(32, 32)],
        format="png",
        options={"quality": 100},
    )
    active = models.BooleanField("启用", default=False)
    rank = models.SmallIntegerField("排序", default=0)

    class Meta:
        verbose_name = "交易所"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name_zh:
            self.name_zh = self.name
        super().save(*args, **kwargs)
