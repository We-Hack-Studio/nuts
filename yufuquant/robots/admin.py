from django.contrib import admin

from .models import AssetRecord, AssetRecordSnap, Robot


class AssetRecordInline(admin.TabularInline):
    model = AssetRecord

    fields = [
        "id",
        "currency",
        "total_principal",
        "total_balance",
        "total_principal_24h_ago",
        "total_balance_24h_ago",
    ]
    readonly_fields = [
        "id",
        "currency",
        "total_principal_24h_ago",
        "total_balance_24h_ago",
    ]


@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    inlines = [AssetRecordInline]
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


@admin.register(AssetRecordSnap)
class AssetRecordSnapAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "period",
        "total_principal",
        "total_balance",
        "created_at",
        "modified_at",
    ]
    list_select_related = ["asset_record", "asset_record__robot"]
    list_filter = ["period"]
