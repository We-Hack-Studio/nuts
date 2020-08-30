from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from rest_framework.authtoken.models import Token

from .models import User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (("User", {"fields": ("nickname",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["id", "username", "nickname", "is_superuser", "is_active"]
    search_fields = ["username", "nickname", "email"]


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
