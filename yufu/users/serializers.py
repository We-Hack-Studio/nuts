from rest_auth.serializers import TokenSerializer
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.ImageField(source="avatar_thumbnail.url")

    class Meta:
        model = User
        fields = ["id", "username", "nickname", "avatar_url"]


class UserDetailTokenSerializer(TokenSerializer):
    user = UserSerializer()

    class Meta(TokenSerializer.Meta):
        fields = ["user", "key"]
