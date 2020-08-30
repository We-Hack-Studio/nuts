from django.contrib import admin

from .models import Strategy


@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "created_at",
        "modified_at",
    ]
