from rest_framework import serializers

from credentials.serializers import CredentialKeysSerializer

from .models import Robot


class RobotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Robot
        fields = [
            "id",
            "enable",
            "start_time",
            "ping_time",
            "created_at",
            "modified_at",
        ]


class RobotConfigSerializer(serializers.ModelSerializer):
    credential_keys = CredentialKeysSerializer(source="credential", read_only=True)

    class Meta:
        model = Robot
        fields = [
            "id",
            "name",
            "pair",
            "enable",
            "credential_keys",
        ]
