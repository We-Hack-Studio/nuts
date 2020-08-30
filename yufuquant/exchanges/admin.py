from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from .models import Exchange


@admin.register(Exchange)
class ExchangeAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = [
        "id",
        "rank",
        "code",
        "name",
        "name_zh",
        "created_at",
        "modified_at",
    ]
