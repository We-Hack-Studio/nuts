import json

from django.contrib.auth import get_user_model
from strategies.models import Strategy
from strategies.tests.factories import StrategyFactory
from test_plus.test import APITestCase

User = get_user_model()


class StrategyViewSetTestCase(APITestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.admin_user = User.objects.create_superuser(
            username="admin", password="password", email="admin@yufuquant.cc"
        )
        self.normal_user = self.make_user(username="normal", password="password")
        self.strategy_list_url = self.reverse("api:strategy-list")
        self.nonexistent_strategy_detail_url = self.reverse(
            "api:strategy-detail", pk=9999999
        )

    # list robot
    def test_list_permission(self):
        # anonymous
        response = self.get(self.strategy_list_url)
        self.response_401(response)

        # normal user
        self.login(username=self.normal_user.username, password="password")
        response = self.get("api:strategy-list")
        self.response_403(response)

    def test_list_strategy(self):
        StrategyFactory.create_batch(5)
        self.login(username=self.admin_user.username, password="password")
        response = self.get(self.strategy_list_url)
        self.response_200(response)
        self.assertEqual(len(response.data["results"]), 5)

    # retrieve
    def test_retrieve_permission(self):
        strategy = StrategyFactory()

        # anonymous user
        response = self.get("api:strategy-detail", pk=strategy.pk)
        self.response_401(response)

        # normal user
        self.login(username=self.normal_user.username, password="password")
        response = self.get("api:strategy-detail", pk=strategy.pk)
        self.response_403(response)

    def test_retrieve_nonexistent_strategy(self):
        self.login(username=self.admin_user.username, password="password")
        response = self.get(self.nonexistent_strategy_detail_url)
        self.response_404(response)

    def test_retrieve_strategy(self):
        strategy = StrategyFactory()
        self.login(username=self.admin_user.username, password="password")
        response = self.get("api:strategy-detail", pk=strategy.pk)
        self.response_200(response)

    # create
    def test_create_permission(self):
        # anonymous
        response = self.post(self.strategy_list_url)
        self.response_401(response)

        # normal user
        self.login(username=self.normal_user.username, password="password")
        response = self.post("api:strategy-list")
        self.response_403(response)

    def test_create_strategy(self):
        specification = {
            "specVersion": "v0.1.0",
            "parameters": [
                {
                    "code": "param1",
                    "name": "Param1",
                    "type": "string",
                    "description": "",
                    "default": "test1",
                    "editable": True,
                },
                {
                    "code": "param2",
                    "name": "Param2",
                    "type": "string",
                    "description": "",
                    "default": "test2",
                    "editable": True,
                },
            ],
        }
        data = {
            "name": "Test",
            "description": "A test strategy",
            "specification": json.dumps(specification),
        }
        self.login(username=self.admin_user.username, password="password")
        response = self.post(
            self.strategy_list_url,
            data=data,
        )
        self.response_201(response)
        self.assertEqual(Strategy.objects.count(), 1)

    def test_create_strategy_with_invalid_data(self):
        data = {
            "name": "",
            "specification": "",
        }
        self.login(username=self.admin_user.username, password="password")
        response = self.post(
            self.strategy_list_url,
            data=data,
        )
        self.response_400(response)
        self.assertIn("name", response.data)
        self.assertIn("specification", response.data)
