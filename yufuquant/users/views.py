from django.contrib.auth import user_logged_in, user_logged_out
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import LoginSerializer, TokenUserSerializer, UserSerializer


class UserViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    resource_name = "users"

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.all().filter(pk=user.pk)
        return queryset

    def get_instance(self):
        return self.request.user

    @swagger_auto_schema(
        operation_description="User basic profile.",
    )
    @action(
        ["GET"],
        detail=False,
        url_path="me",
        url_name="me",
        serializer_class=UserSerializer,
    )
    def me(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Login a user.",
        responses={200: TokenUserSerializer()},
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

    @swagger_auto_schema(
        operation_description="Logout the user.",
        responses={200: "Logout successfully."},
    )
    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        user_logged_out.send(
            sender=request.user.__class__, request=request, user=request.user
        )
        return Response(status=status.HTTP_200_OK)
