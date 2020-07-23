from django.contrib import admin

from .models import Credential


@admin.register(Credential)
class CredentialAdmin(admin.ModelAdmin):
    fields = [
        "note",
    ]
    list_display = [
        "id",
        "note",
        "user",
        "created_at",
    ]
    list_select_related = ["user"]
