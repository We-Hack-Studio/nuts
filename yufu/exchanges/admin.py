from django.contrib import admin

from .models import Exchange


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "code",
        "name",
        "name_zh",
        "created_at",
        "modified_at",
    ]
