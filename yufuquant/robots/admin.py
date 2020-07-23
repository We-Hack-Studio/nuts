from django.contrib import admin

from .models import Robot


@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "pair",
        "market_type",
        "target_currency",
        "enabled",
        "start_time",
        "ping_time",
        "created_at",
        "modified_at",
    ]
    readonly_fields = [
        "ping_time",
    ]
