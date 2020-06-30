from django.db import models
from model_utils.fields import AutoCreatedField, AutoLastModifiedField


class TimeStampedModel(models.Model):
    created_at = AutoCreatedField("创建于")
    modified_at = AutoLastModifiedField("修改于")

    class Meta:
        abstract = True
