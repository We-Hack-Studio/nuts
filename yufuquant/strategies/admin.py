from django.contrib import admin

from .models import StrategyTemplate


@admin.register(StrategyTemplate)
class StrategyTemplateAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "code",
        "name",
        "created_at",
        "modified_at",
    ]
