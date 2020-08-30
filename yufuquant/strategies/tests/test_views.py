import json

from test_plus.test import APITestCase
from users.models import User

from .factories import StrategyFactory


class StrategyTemplateViewSetTestCase(APITestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.user = User.objects.create_superuser(
            username="user", password="test", email="user@yufuquant.cc"
        )
        self.user_token = self.user.auth_token

    def test_list_strategy_template(self):
        StrategyFactory.create_batch(5)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        response = self.client.get(self.reverse("api:strategy-list"))
        self.response_200(response)
        self.assertEqual(len(response.data["results"]), 5)

    def test_create_valid_strategy_template(self):
        parameter_spec = {
            "version": "v0",
            "specVersion": "v1.0",
            "description": "",
            "fields": [
                {
                    "code": "code",
                    "name": "Code",
                    "type": "float",
                    "description": "",
                    "default": None,
                    "editable": True,
                },
            ],
        }
        data = {
            "code": "test",
            "name": "Test",
            "description": "A test strategy template",
            "specification": json.dumps(parameter_spec),
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        response = self.client.post(
            self.reverse("api:strategy-list"), data=data, extra={"format": "json"},
        )
        self.response_201(response)
        # todo: assert response schema

    def test_create_invalid_strategy_template(self):
        data = {
            "code": "",
            "name": "",
            "description": "",
            "specification": "",
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        response = self.client.post(
            self.reverse("api:strategy-list"), data=data, extra={"format": "json"},
        )
        self.response_400(response)
