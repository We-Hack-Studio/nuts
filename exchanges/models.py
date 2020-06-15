from django.db import models
from model_utils.fields import AutoCreatedField, AutoLastModifiedField


class Exchange(models.Model):
    code = models.CharField("代码", max_length=20)
    name = models.CharField("名字", max_length=20)
    name_zh = models.CharField("中文名", max_length=20, blank=True)
    created_at = AutoCreatedField("创建于")
    modified_at = AutoLastModifiedField("修改于")

    class Meta:
        verbose_name = "交易所"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name_zh:
            self.name_zh = self.name
        super().save(*args, **kwargs)
