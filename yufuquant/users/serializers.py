from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User


class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.ImageField(source="avatar_thumbnail.url")

    class Meta:
        model = User
        fields = ["id", "username", "nickname", "avatar_url"]


class TokenCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"})

    default_error_messages = {
        "invalid_credentials": _("Unable to log in with provided credentials."),
    }

    def validate(self, attrs):
        password = attrs.get("password")
        params = {"username": attrs["username"]}
        user = authenticate(**params, password=password)
        if not user:
            self.fail("invalid_credentials")
        attrs["user"] = user
        return attrs


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source="key")

    class Meta:
        model = Token
        fields = ("auth_token",)
