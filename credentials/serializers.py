from rest_framework import serializers

from .models import Credential
from exchanges.serializers import ExchangeSerializer


class CredentialKeyField(serializers.CharField):
    def to_representation(self, value):
        head = value[:3]
        hidden = value[3:-4]
        tail = value[-4:]
        return head + "*" * len(hidden) + tail


class CredentialKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = [
            "id",
            "api_key",
            "secret",
            "passphrase",
        ]


class CredentialSerializer(serializers.ModelSerializer):
    api_key_masked = CredentialKeyField(source="api_key", read_only=True)
    secret_masked = CredentialKeyField(source="secret", read_only=True)
    exchange_info = ExchangeSerializer(source="exchange", read_only=True)

    class Meta:
        model = Credential
        fields = [
            "id",
            "note",
            "api_key",
            "secret",
            "api_key_masked",
            "secret_masked",
            "exchange",
            "exchange_info",
            "created_at",
        ]
        read_only_fields = [
            "created_at",
        ]
        extra_kwargs = {
            "exchange": {"write_only": True},
            "api_key": {"write_only": True},
            "secret": {"write_only": True},
        }
