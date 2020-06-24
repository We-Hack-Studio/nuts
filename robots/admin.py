from django.contrib import admin

from .models import Robot


@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "enabled",
        "start_time",
        "ping_time",
        "created_at",
        "modified_at",
    ]
