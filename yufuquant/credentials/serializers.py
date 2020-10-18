from core.serializers import MaskedCharField
from exchanges.serializers import ExchangeSerializer
from rest_framework import serializers

from .models import Credential


class CredentialListSerializer(serializers.ModelSerializer):
    included_serializers = {
        "exchange": ExchangeSerializer,
    }
    api_key = MaskedCharField(read_only=True)
    secret = MaskedCharField(read_only=True)
    passphrase = MaskedCharField(read_only=True, mask_all=True)

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

    class JSONAPIMeta:
        resource_name = "credentials"


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

    class JSONAPIMeta:
        resource_name = "credentials"
