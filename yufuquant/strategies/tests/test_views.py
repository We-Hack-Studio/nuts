import json

from test_plus.test import APITestCase
from users.models import User

from .factories import StrategyTemplateFactory


class StrategyTemplateViewSetTestCase(APITestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.user = User.objects.create_superuser(
            username="user", password="test", email="user@yufuquant.cc"
        )

    def test_list_strategy_template(self):
        StrategyTemplateFactory.create_batch(5)
        self.client.login(username=self.user.username, password="test")
        response = self.client.get(self.reverse("strategy-template-list"))
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
            "parameter_spec": json.dumps(parameter_spec),
        }
        self.client.login(username=self.user.username, password="test")
        response = self.client.post(
            self.reverse("strategy-template-list"), data=data, extra={"format": "json"},
        )
        self.response_201(response)
        # todo: assert response schema

    def test_create_invalid_strategy_template(self):
        data = {
            "code": "",
            "name": "",
            "description": "",
            "parameter_spec": "",
        }
        self.client.login(username=self.user.username, password="test")
        response = self.client.post(
            self.reverse("strategy-template-list"), data=data, extra={"format": "json"},
        )
        self.response_400(response)
