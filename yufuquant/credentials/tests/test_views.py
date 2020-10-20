from credentials.models import Credential
from credentials.serializers import CredentialListSerializer
from django.contrib.auth import get_user_model
from exchanges.tests.factories import ExchangeFactory
from freezegun import freeze_time
from rest_framework.test import APIRequestFactory
from test_plus.test import APITestCase

from .factories import CredentialFactory

User = get_user_model()


class CredentialViewSetTestCase(APITestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.api_request_factory = APIRequestFactory()
        self.admin_user = User.objects.create_superuser(
            username="admin", password="password"
        )
        self.normal_user = self.make_user(username="normal", password="password")
        self.credential_list_url = self.reverse("api:credential-list")
        self.nonexistent_credential_detail_url = self.reverse(
            "api:credential-detail", pk=999999
        )

    # list
    def test_list_permission(self):
        # anonymous user
        response = self.get("api:credential-list")
        self.response_401(response)

    def test_list_credential(self):
        CredentialFactory.create_batch(3, user=self.admin_user)

        self.login(username="admin", password="password")
        response = self.get("api:credential-list")
        self.response_200(response)
        self.assertEqual(len(response.data), 3)

        request = self.api_request_factory.get(self.credential_list_url)
        serializer = CredentialListSerializer(
            Credential.objects.all().order_by("-created_at"),
            many=True,
            context={"request": request},
        )
        self.assertEqual(response.data, serializer.data)

    # Create
    def test_create_permission(self):
        # anonymous user
        response = self.post("api:credential-list")
        self.response_401(response)

    def test_create_invalid_credential(self):
        self.login(username=self.admin_user.username, password="password")
        data = {
            "note": "Valid",
            "api_key": "api-key",
            "secret": "secret",
            "passphrase": "passphrase",
            "test_net": True,
            # invalid
            "exchange": 999999,
        }
        response = self.post("api:credential-list", data=data)
        self.response_400(response)
        self.assertIn("exchange", response.data)

    @freeze_time("2020-10-18 03:21:34.456789")  # UTC
    def test_create_valid_credential(self):
        exchange = ExchangeFactory(code="binance")
        self.login(username=self.admin_user.username, password="password")
        data = {
            "note": "Valid",
            "api_key": "api-key",
            "secret": "secret",
            "passphrase": "passphrase",
            "test_net": True,
            "exchange": exchange.pk,
        }
        response = self.post(
            "api:credential-list",
            data=data,
        )
        self.response_201(response)
        self.assertEqual(Credential.objects.count(), 1)

    # Delete
    def test_delete_permission(self):
        # anonymous user
        credential = CredentialFactory(user=self.admin_user)
        response = self.delete("api:credential-detail", pk=credential.pk)
        self.response_401(response)

    def test_delete_nonexistent_credential(self):
        self.login(username=self.admin_user.username, password="password")
        response = self.delete(self.nonexistent_credential_detail_url)
        self.response_404(response)

    def test_delete_credential(self):
        credential = CredentialFactory(user=self.admin_user)
        self.login(username=self.admin_user.username, password="password")
        response = self.delete("api:credential-detail", pk=credential.pk)
        self.response_204(response)
        self.assertEqual(Credential.objects.count(), 0)
