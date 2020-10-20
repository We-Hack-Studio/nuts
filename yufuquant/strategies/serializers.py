from rest_framework import serializers

from .models import Strategy


class StrategySerializer(serializers.ModelSerializer):
    specification = serializers.JSONField(binary=True)

    class Meta:
        model = Strategy
        fields = [
            "id",
            "name",
            "description",
            "specification",
            "created_at",
            "modified_at",
        ]

