from rest_framework import serializers

from .models import Credential


class CredentialKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = [
            "id",
            "api_key",
            "secret",
            "passphrase",
        ]
