from django.contrib import admin

from .models import Position


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "direction",
        "qty",
        "direction",
        "avg_price",
        "unrealized_pnl",
        "liq_price",
        "leverage",
    ]
    search_fields = [
        "robot__user__username",
        "robot__user__email",
        "robot__user__nickname",
    ]
