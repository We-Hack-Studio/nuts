from django.contrib.auth import user_logged_in, user_logged_out
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import TokenCreateSerializer, TokenSerializer, UserSerializer


class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    resource_name = "users"

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.all().filter(pk=user.pk)
        return queryset

    def get_instance(self):
        return self.request.user

    @action(["GET"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)


class TokenCreateView(GenericAPIView):
    """
    Use this endpoint to obtain user authentication token.
    """

    serializer_class = TokenCreateSerializer
    permission_classes = [AllowAny]
    resource_name = "tokens"

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        user_logged_in.send(sender=user.__class__, request=request, user=user)
        return Response(
            data=TokenSerializer(instance=token).data, status=status.HTTP_200_OK
        )


class TokenDestroyView(APIView):
    """
    Use this endpoint to logout user (remove user authentication token).
    """

    permission_classes = [IsAuthenticated]
    resource_name = "auth_tokens"

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        user_logged_out.send(
            sender=request.user.__class__, request=request, user=request.user
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
