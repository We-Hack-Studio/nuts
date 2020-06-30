from datetime import datetime

from django.contrib import admin
from django.utils import timezone

from .models import Robot


@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "pair",
        "margin_currency",
        "enabled",
        "start_time",
        "ping_time",
        "order_sync_datetime",
        "created_at",
        "modified_at",
    ]
    readonly_fields = [
        "stream_key",
        "ping_time",
    ]

    def order_sync_datetime(self, obj):
        if obj.order_sync_ts is None:
            return
        tz = timezone.get_current_timezone()
        d = datetime.fromtimestamp(obj.order_sync_ts // 1000, tz=tz)
        return timezone.localtime(d)

    order_sync_datetime.short_description = "订单同步时间"
