from rest_framework import serializers

from .models import Exchange


class SimpleExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        resource_name = "exchanges"
        fields = [
            "id",
            "code",
            "name",
            "name_zh",
        ]


class ExchangeSerializer(serializers.ModelSerializer):
    logo_url = serializers.ImageField(source="logo_thumbnail")

    class Meta:
        model = Exchange
        resource_name = "exchanges"
        fields = [
            "id",
            "code",
            "name",
            "name_zh",
            "logo_url",
            "active",
            "rank",
            "created_at",
            "modified_at",
        ]

    class JSONAPIMeta:
        resource_name = "exchanges"