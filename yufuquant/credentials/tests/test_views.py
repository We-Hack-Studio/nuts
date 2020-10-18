import json

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
        content_json = json.loads(response.content)
        self.assertEqual(len(content_json["data"]), 3)

        request = self.api_request_factory.get(self.credential_list_url)
        serializer = CredentialListSerializer(
            Credential.objects.all().order_by("-created_at"),
            many=True,
            context={"request": request},
        )
        # here we compare the results before rendered
        self.assertEqual(response.data, serializer.data)

    def test_list_credential_include_exchange(self):
        exchange = ExchangeFactory(code="binance")
        CredentialFactory(exchange=exchange, user=self.admin_user)

        self.login(username="admin", password="password")
        response = self.get("api:credential-list", data={"include": "exchange"})
        self.response_200(response)
        content_json = json.loads(response.content)

        """
        "included": [
            {
                "type": "exchanges",
                "id": "1",
                "attributes": {
                    "code": "binance",
                    "name": "Binance",
                    "name_zh": "币安",
                    "logo_url": "http://127.0.0.1:8000/media/CACHE/images/exchanges/logos/binance/binance.png",
                    "active": true,
                    "rank": 0,
                    "created_at": "2020-10-18T11:34:24.960637+08:00",
                    "modified_at": "2020-10-18T11:34:24.960637+08:00"
                }
            }
        ]
        """
        self.assertIn("included", content_json)
        self.assertEqual(len(content_json["included"]), 1)
        self.assertEqual(content_json["included"][0]["type"], "exchanges")
        self.assertEqual(content_json["included"][0]["id"], str(exchange.pk))

    # Create
    def test_create_permission(self):
        # anonymous user
        response = self.post("api:credential-list")
        self.response_401(response)

    def test_create_invalid_credential(self):
        self.login(username=self.admin_user.username, password="password")
        data = {
            "data": {
                "type": "credentials",
                "attributes": {},
            }
        }
        response = self.post("api:credential-list", data=data)
        self.response_400(response)
        content_json = json.loads(response.content)
        self.assertIn("errors", content_json)

    @freeze_time("2020-10-18 03:21:34.456789")  # UTC
    def test_create_valid_credential(self):
        exchange = ExchangeFactory(code="binance")
        self.login(username=self.admin_user.username, password="password")
        data = {
            "data": {
                "type": "credentials",
                "attributes": {
                    "note": "Valid",
                    "api_key": "api-key",
                    "secret": "secret",
                    "passphrase": "passphrase",
                    "test_net": True,
                    "exchange": exchange.pk,
                },
            }
        }
        response = self.post(
            "api:credential-list",
            data=data,
        )
        self.response_201(response)
        content_json = json.loads(response.content)
        self.assertEqual(
            content_json,
            {
                "data": {
                    "type": "credentials",
                    "id": "1",
                    "attributes": {
                        "note": "Valid",
                        "test_net": True,
                        "created_at": "2020-10-18T11:21:34.456789+08:00",
                        "modified_at": "2020-10-18T11:21:34.456789+08:00",
                    },
                }
            },
        )

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
