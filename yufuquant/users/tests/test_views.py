import pytest
from django.urls import reverse_lazy
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from test_plus.test import APITestCase
from users.models import User
from users.serializers import UserSerializer

from .factories import UserFactory


class UserViewSetTestCase(APITestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.api_request_factory = APIRequestFactory()

        self.admin_user = User.objects.create_superuser(
            username="admin", password="password", email="admin@yufuquant.cc"
        )
        self.normal_user = self.make_user(username="normal", password="password")

    def test_me_permission(self):
        # anonymous user
        response = self.get("api:user-me")
        self.response_401(response)

        # normal user
        self.login(username=self.normal_user.username, password="password")
        response = self.get("api:user-me")
        self.response_403(response)

    def test_me(self):
        self.login(username=self.admin_user.username, password="password")
        response = self.get("api:user-me")
        self.response_200(response)

        request = self.api_request_factory.get("/users/me")
        serializer = UserSerializer(
            instance=self.admin_user,
            context={"request": Request(request)},
        )
        self.assertEqual(response.data, serializer.data)


@pytest.mark.django_db
def test_login(api_client):
    user = UserFactory(username="user", password="password")
    login_url = reverse_lazy("api:login")
    response = api_client.post(
        login_url, data={"username": user.username, "password": "password"}
    )
    assert response.status_code == 200
    assert Token.objects.filter(user=user).count() == 1


@pytest.mark.django_db
def test_login_with_invalid_credential(api_client):
    login_url = reverse_lazy("api:login")
    response = api_client.post(
        login_url, data={"username": "user", "password": "password"}
    )
    assert response.status_code == 400
    assert "non_field_errors" in response.data


@pytest.mark.django_db
def test_logout(api_client):
    user = UserFactory(username="user", password="password")
    api_client.login(username=user.username, password="password")
    logout_url = reverse_lazy("api:logout")
    response = api_client.post(logout_url)
    assert response.status_code == 204
    assert Token.objects.filter(user=user).count() == 0
