from rest_framework import serializers

from .models import Exchange


class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = [
            "id",
            "code",
            "name",
            "name_zh",
        ]
