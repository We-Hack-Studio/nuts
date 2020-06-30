from django.contrib import admin

from .models import Asset


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "principal",
        "balance",
        "currency",
    ]
    search_fields = [
        "credential__user__username",
        "credential__user__email",
        "credential__user__nickname",
    ]
    list_filter = ["currency"]
