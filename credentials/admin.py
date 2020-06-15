from django.contrib import admin

from .models import Credential


@admin.register(Credential)
class CredentialAdmin(admin.ModelAdmin):
    fields = [
        "note",
    ]
    list_display = (
        "id",
        "note",
        "created_at",
    )
