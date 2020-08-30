from django.contrib.auth import user_logged_in, user_logged_out
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import TokenCreateSerializer, TokenSerializer, UserSerializer


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class TokenCreateView(GenericAPIView):
    """
    Use this endpoint to obtain user authentication token.
    """

    serializer_class = TokenCreateSerializer
    permission_classes = [AllowAny]

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

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        user_logged_out.send(
            sender=request.user.__class__, request=request, user=request.user
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
