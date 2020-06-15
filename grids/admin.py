from django.contrib import admin

from .models import Grid


@admin.register(Grid)
class GridAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "index",
        "entry_qty",
        "entry_price",
        "exit_price",
        "filled_qty",
        "created_at",
        "modified_at",
    ]
    ordering = ["index"]
