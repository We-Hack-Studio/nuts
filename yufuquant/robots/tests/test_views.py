from credentials.tests.factories import CredentialFactory
from strategies.tests.factories import StrategyFactory
from test_plus import APITestCase
from users.models import User

from .factories import RobotFactory


class RobotViewSetTestCase(APITestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.admin_user = User.objects.create_superuser(
            username="admin", password="test", email="admin@yufuquant.cc"
        )
        self.admin_user_token = self.admin_user.auth_token
        self.user = User.objects.create_user(
            username="user", password="test", email="user@yufuquant.cc"
        )
        self.user_token = self.user.auth_token

    def test_list_robot_permission(self):
        url = self.reverse("api:robot-list")
        response = self.client.get(url)
        self.response_401(response)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        response = self.client.get(url)
        self.response_403(response)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_user_token.key)
        response = self.client.get(url)
        self.response_200(response)

    def test_list_robot(self):
        RobotFactory.create_batch(5)
        url = self.reverse("api:robot-list")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_user_token.key)
        response = self.client.get(url)
        self.response_200(response)
        self.assertEqual(len(response.data), 5)

    def test_create_robot_permission(self):
        url = self.reverse("api:robot-list")
        response = self.client.post(url)
        self.response_401(response)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        url = self.reverse("api:robot-list")
        response = self.client.post(url)
        self.response_403(response)

    def test_create_valid_robot(self):
        credential = CredentialFactory(user=self.admin_user)
        strategy = StrategyFactory()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_user_token.key)
        url = self.reverse("api:robot-list")
        data = {
            "data": {
                "type": "robots",
                "attributes": {
                    "name": "Robot-1",
                    "pair": "BTCUSDT",
                    "market_type": "futures",
                    "enabled": True,
                    "credential": {"type": "credentials", "id": credential.pk},
                    "strategy": {"type": "strategies", "id": strategy.pk},
                },
            }
        }
        response = self.client.post(url, data=data)
        self.response_201(response)

    def test_create_invalid_robot(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_user_token.key)
        url = self.reverse("api:robot-list")
        data = {
            "data": {
                "type": "robots",
                "attributes": {
                    "name": "Robot-1",
                    "pair": "BTCUSDT",
                    "market_type": "options",
                    "enabled": True,
                    "credential": {"type": "credentials", "id": 999},
                    "strategy": {"type": "strategies", "id": 999},
                },
            }
        }
        response = self.client.post(url, data=data)
        self.response_400(response)

    def test_retrieve_robot_permission(self):
        robot = RobotFactory()
        url = self.reverse("api:robot-detail", pk=robot.pk)

        response = self.client.get(url)
        self.response_401(response)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        response = self.client.get(url)
        self.response_403(response)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_user_token.key)
        response = self.client.get(url)
        self.response_200(response)

    def test_retrieve_robot(self):
        url = self.reverse("api:robot-detail", pk=9999)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_user_token.key)

        response = self.client.get(url)
        self.response_404(response)

        robot = RobotFactory()
        url = self.reverse("api:robot-detail", pk=robot.pk)
        response = self.client.get(url)
        self.response_200(response)

    def test_update_robot_permission(self):
        pass

    def test_update_valid_robot(self):
        pass

    def test_update_invalid_robot(self):
        pass

    def test_delete_robot_permission(self):
        pass

    def test_admin_user_can_delete_a_robot(self):
        robot = RobotFactory()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_user_token.key)
        url = self.reverse("api:robot-detail", pk=robot.pk)
        response = self.client.delete(url)
        self.response_204(response)

    def test_can_not_delete_a_nonexistent_robot(self):
        url = self.reverse("api:robot-detail", pk=999)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_user_token.key)
        response = self.client.delete(url)
        self.response_404(response)

    def test_retrieve_robot_config_permission(self):
        robot = RobotFactory()
        url = self.reverse("api:robot-config", pk=robot.pk)

        response = self.client.get(url)
        self.response_401(response)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        response = self.client.get(url)
        self.response_403(response)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_user_token.key)
        response = self.client.get(url)
        self.response_200(response)

    def test_retrieve_robot_config(self):
        url = self.reverse("api:robot-config", pk=9999)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_user_token.key)

        response = self.client.get(url)
        self.response_404(response)

        robot = RobotFactory()
        url = self.reverse("api:robot-config", pk=robot.pk)
        response = self.client.get(url)
        self.response_200(response)

    def test_ping_robot_permission(self):
        robot = RobotFactory()
        url = self.reverse("api:robot-ping", pk=robot.pk)

        response = self.client.post(url)
        self.response_401(response)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        response = self.client.post(url)
        self.response_403(response)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_user_token.key)
        response = self.client.post(url)
        self.response_200(response)

    def test_ping_robot(self):
        url = self.reverse("api:robot-ping", pk=9999)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_user_token.key)

        response = self.client.post(url)
        self.response_404(response)

        robot = RobotFactory()
        url = self.reverse("api:robot-ping", pk=robot.pk)
        response = self.client.post(url)
        self.response_200(response)
        self.assertEqual(response.data, {"detail": "pong"})

    def test_update_valid_robot_strategy_parameters(self):
        robot = RobotFactory()
        url = self.reverse("api:robot-strategy-parameters", pk=robot.pk)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_user_token.key)

        data = {
            "data": {
                "type": "robots",
                "id": robot.pk,
                "attributes": {"strategy_parameters": '{"code":"new value"}'},
            }
        }
        response = self.client.post(url, data=data)
        self.response_200(response)
        self.assertEqual(response.data, {"detail": "ok"})

        robot.refresh_from_db()
        self.assertEqual(
            robot.strategy_parameters,
            {"code": "new value"},
        )

    def test_partial_update_robot_asset_record(self):
        robot = RobotFactory()
        url = self.reverse("api:robot-asset-record", pk=robot.pk)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_user_token.key)

        data = {
            "data": {"type": "robots", "id": 1, "attributes": {"total_balance": 9999}}
        }

        response = self.client.patch(url, data=data)
        self.response_200(response)
        self.assertEqual(response.data, {"detail": "ok"})

        robot.refresh_from_db()
        self.assertEqual(
            robot.asset_record.total_principal,
            0,
        )
        self.assertEqual(
            robot.asset_record.total_balance,
            9999,
        )
