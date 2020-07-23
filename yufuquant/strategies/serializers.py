from rest_framework import serializers

from .models import Strategy, StrategyTemplate


class StrategyTemplateSerializer(serializers.ModelSerializer):
    parameters_spec = serializers.JSONField()

    class Meta:
        model = StrategyTemplate
        fields = [
            "id",
            "code",
            "name",
            "description",
            "parameters_spec",
            "created_at",
            "modified_at",
        ]


class StrategySerializer(serializers.ModelSerializer):
    code = serializers.CharField(source="template.code")
    name = serializers.CharField(source="template.name")
    parameters = serializers.JSONField()

    class Meta:
        model = Strategy
        fields = [
            "id",
            "code",
            "name",
            "parameters",
            "created_at",
            "modified_at",
        ]
