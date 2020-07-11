from django.contrib import admin

from .models import Grid, GridStrategyParameter


@admin.register(GridStrategyParameter)
class GridStrategyParameterAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "min_price",
        "max_price",
        "num_grids",
        "max_leverage",
        "principal",
        "take_profit_range",
        "created_at",
        "modified_at",
    ]


@admin.register(Grid)
class GridAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "level",
        "entry_price",
        "exit_price",
        "filled_qty",
        "entry_qty",
        "associated_order_id",
        "locked",
        "created_at",
        "modified_at",
    ]
    ordering = ["level"]
