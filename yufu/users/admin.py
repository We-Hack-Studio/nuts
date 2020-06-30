from django.contrib import admin
from rest_framework.authtoken.models import Token

admin.site.unregister(Token)


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ("user", "key", "created")
    fields = ("user",)
    ordering = ("-created",)
    search_fields = (
        "user__username",
        "user__nickname",
        "user__email",
    )
    list_select_related = ["user"]
