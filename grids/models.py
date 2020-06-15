from django.db import models
from model_utils.fields import AutoCreatedField, AutoLastModifiedField


class Grid(models.Model):
    entry_qty = models.FloatField("仓位数量")
    entry_price = models.FloatField("入场价格")
    exit_price = models.FloatField("出场价格")
    filled_qty = models.FloatField("已开仓数量")
    created_at = AutoCreatedField("创建于")
    modified_at = AutoLastModifiedField("修改于")
    index = models.IntegerField("索引")

    class Meta:
        verbose_name = "网格"
        verbose_name_plural = verbose_name

    @property
    def holding(self):
        return self.filled_qty > 0
