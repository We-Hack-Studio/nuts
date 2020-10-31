from core.serializers import MaskedCharField
from exchanges.serializers import ExchangeSerializer
from rest_framework import serializers

from .models import Credential


class CredentialListSerializer(serializers.ModelSerializer):
    api_key = MaskedCharField(read_only=True, help_text="Partial masked API key.")
    secret = MaskedCharField(read_only=True, help_text="Partial masked secret key.")
    passphrase = MaskedCharField(
        read_only=True, mask_all=True, help_text="Completely masked passphrase."
    )
    exchange = ExchangeSerializer(read_only=True)

    class Meta:
        model = Credential
        fields = [
            "id",
            "note",
            "api_key",
            "secret",
            "passphrase",
            "test_net",
            "exchange",
            "created_at",
            "modified_at",
        ]

        extra_kwargs = {
            "test_net": {"help_text": "Is a credential of exchange test net or not."},
        }


class CredentialCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = [
            "id",
            "note",
            "api_key",
            "secret",
            "passphrase",
            "test_net",
            "exchange",
            "created_at",
            "modified_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "modified_at",
        ]
        extra_kwargs = {
            "exchange": {"write_only": True},
            "api_key": {"write_only": True},
            "secret": {"write_only": True},
            "passphrase": {"write_only": True},
        }


class CredentialUpdateSerializer(CredentialCreateSerializer):
    pass
