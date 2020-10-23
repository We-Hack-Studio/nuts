from django.contrib.auth import user_logged_in, user_logged_out
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import LoginSerializer, TokenUserSerializer, UserSerializer


class UserViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return User.objects.all()

    @extend_schema(
        summary="Get current user profile",
    )
    @action(
        ["GET"],
        detail=False,
        url_path="me",
        url_name="me",
        serializer_class=UserSerializer,
    )
    def me(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Login",
        description="Obtain an auth token by providing username and password.",
        responses={200: TokenUserSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        user_logged_in.send(sender=user.__class__, request=request, user=user)
        output_serializer = TokenUserSerializer(
            instance=token, context={"request": request}
        )
        return Response(
            data=output_serializer.data,
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Logout",
        description="Delete auth token from server.",
        responses={"204": None},
    )
    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        user_logged_out.send(
            sender=request.user.__class__, request=request, user=request.user
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
