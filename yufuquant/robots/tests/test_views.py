from credentials.tests.factories import CredentialFactory
from django.contrib.auth import get_user_model
from django.db.models import F
from freezegun import freeze_time
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from robots.models import Robot
from robots.serializers import RobotListSerializer, RobotRetrieveSerializer
from strategies.tests.factories import StrategyFactory
from test_plus import APITestCase

from .factories import RobotFactory

User = get_user_model()


class RobotViewSetTestCase(APITestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.api_request_factory = APIRequestFactory()
        self.admin_user = User.objects.create_superuser(
            username="admin", password="password", email="admin@yufuquant.cc"
        )
        self.admin_user_credential = CredentialFactory(user=self.admin_user)
        self.normal_user = self.make_user(username="normal", password="password")
        self.robot_list_url = self.reverse("api:robot-list")
        self.nonexistent_robot_detail_url = self.reverse("api:robot-detail", pk=999999)

    # list
    def test_list_permission(self):
        # anonymous user
        response = self.get("api:robot-list")
        self.response_401(response)

        # normal user
        self.login(username=self.normal_user.username, password="password")
        response = self.get("api:robot-list")
        self.response_403(response)

    def test_list_robot(self):
        RobotFactory.create_batch(5, credential=self.admin_user_credential)
        self.login(username=self.admin_user.username, password="password")
        response = self.get("api:robot-list")
        self.response_200(response)
        self.assertEqual(len(response.data), 5)

        request = self.api_request_factory.get(self.robot_list_url)
        serializer = RobotListSerializer(
            instance=Robot.objects.all()
            .order_by("-created_at")
            .annotate(strategy_name=F("strategy__name")),
            many=True,
            context={"request": Request(request)},
        )
        self.assertEqual(response.data, serializer.data)

    # create
    def test_create_permission(self):
        # anonymous user
        response = self.post("api:robot-list")
        self.response_401(response)

        # normal user
        self.login(username=self.normal_user.username, password="password")
        response = self.post("api:robot-list")
        self.response_403(response)

    def test_create_invalid_robot(self):
        self.login(username=self.admin_user.username, password="password")

        data = {
            "name": "Invalid",
            "pair": "BTCUSDT",
            "market_type": "spots",
            "base_currency": "BTC",
            "quote_currency": "USDT",
            "target_currency": "USDT",
            # invalid data
            "credential": 999999,
            "strategy": 999999,
        }
        response = self.post("api:robot-list", data=data)
        self.response_400(response)
        self.assertIn("credential", response.data)
        self.assertIn("strategy", response.data)

    @freeze_time("2020-10-18 03:21:34.456789")  # UTC
    def test_create_valid_robot(self):
        credential = CredentialFactory(user=self.admin_user)
        strategy = StrategyFactory()
        self.login(username=self.admin_user.username, password="password")

        data = {
            "name": "Valid",
            "pair": "BTCUSDT",
            "market_type": "linear_perpetual",
            "target_currency": "USDT",
            "credential": credential.pk,
            "strategy": strategy.pk,
        }
        response = self.post("api:robot-list", data=data)
        self.response_201(response)

    # retrieve
    def test_retrieve_permission(self):
        robot = RobotFactory()

        # anonymous user
        response = self.get("api:robot-detail", pk=robot.pk)
        self.response_401(response)

        # normal user
        self.login(username=self.normal_user.username, password="password")
        response = self.get("api:robot-detail", pk=robot.pk)
        self.response_403(response)

    def test_retrieve_nonexistent_robot(self):
        self.login(username=self.admin_user.username, password="password")
        response = self.get(self.nonexistent_robot_detail_url)
        self.response_404(response)

    def test_retrieve_robot(self):
        robot = RobotFactory(credential=self.admin_user_credential)
        self.login(username=self.admin_user.username, password="password")
        response = self.get("api:robot-detail", pk=robot.pk)
        self.response_200(response)
        request = self.api_request_factory.get(self.nonexistent_robot_detail_url)
        robot = (
            Robot.objects.all()
            .annotate(test_net=F("credential__test_net"))
            .get(pk=robot.pk)
        )
        serializer = RobotRetrieveSerializer(
            instance=robot, context={"request": Request(request)}
        )
        self.assertDictEqual(response.data, serializer.data)

    # update
    def test_update_permission(self):
        robot = RobotFactory()

        # anonymous user
        response = self.patch("api:robot-detail", pk=robot.pk)
        self.response_401(response)

        # normal user
        self.login(username=self.normal_user.username, password="password")
        response = self.patch("api:robot-detail", pk=robot.pk)
        self.response_403(response)

    def test_update_robot(self):
        robot = RobotFactory(name="Old", credential=self.admin_user_credential)
        self.login(username=self.admin_user.username, password="password")
        data = {
            "name": "New",
        }
        response = self.patch("api:robot-detail", pk=robot.pk, data=data)
        self.response_200(response)
        robot.refresh_from_db()
        self.assertEqual(robot.name, "New")

    def test_update_nonexistent_robot(self):
        self.login(username=self.admin_user.username, password="password")
        response = self.patch(self.nonexistent_robot_detail_url)
        self.response_404(response)

    # delete
    def test_delete_permission(self):
        # anonymous user
        robot = RobotFactory()
        response = self.delete("api:robot-detail", pk=robot.pk)
        self.response_401(response)

        # normal user
        self.login(username=self.normal_user.username, password="password")
        response = self.delete("api:robot-detail", pk=robot.pk)
        self.response_403(response)

    def test_delete_nonexistent_robot(self):
        self.login(username=self.admin_user.username, password="password")
        response = self.delete(self.nonexistent_robot_detail_url)
        self.response_404(response)

    def test_delete_robot(self):
        robot = RobotFactory(credential=self.admin_user_credential)
        self.login(username=self.admin_user.username, password="password")
        response = self.delete("api:robot-detail", pk=robot.pk)
        self.response_204(response)

    # ping
    def test_ping_permission(self):
        robot = RobotFactory()

        # anonymous user
        response = self.post("api:robot-ping", pk=robot.pk)
        self.response_401(response)

        # normal user
        self.login(username=self.normal_user.username, password="password")
        response = self.post("api:robot-ping", pk=robot.pk)
        self.response_403(response)

    def test_ping_nonexistent_robot(self):
        self.login(username=self.admin_user.username, password="password")
        response = self.post("api:robot-ping", pk=999999)
        self.response_404(response)

    def test_ping(self):
        robot = RobotFactory(credential=self.admin_user_credential)
        self.login(username=self.admin_user.username, password="password")
        response = self.post("api:robot-ping", pk=robot.pk)
        self.response_200(response)
        self.assertIn("pong", response.data)

    # adjust strategy parameters
    def test_adjust_strategy_parameters_permission(self):
        robot = RobotFactory()

        # anonymous user
        response = self.patch("api:robot-strategy-parameters", pk=robot.pk)
        self.response_401(response)

        # normal user
        self.login(username=self.normal_user.username, password="password")
        response = self.patch("api:robot-strategy-parameters", pk=robot.pk)
        self.response_403(response)

    def test_adjust_nonexistent_robot_strategy_parameters(self):
        self.login(username=self.admin_user.username, password="password")
        response = self.patch("api:robot-strategy-parameters", pk=999999)
        self.response_404(response)

    def test_adjust_robot_strategy_parameters(self):
        strategy = StrategyFactory(
            specification={
                "specVersion": "v0.1.0",
                "parameters": [
                    {
                        "code": "code1",
                        "name": "Code1",
                        "type": "string",
                        "description": "",
                        "default": "old1",
                        "editable": True,
                    },
                    {
                        "code": "code2",
                        "name": "Code2",
                        "type": "string",
                        "description": "",
                        "default": "old2",
                        "editable": True,
                    },
                ],
            }
        )
        robot = RobotFactory(strategy=strategy, credential=self.admin_user_credential)
        self.login(username=self.admin_user.username, password="password")

        data = {
            "code1": "new1",
            "code2": "new2",
        }
        response = self.patch("api:robot-strategy-parameters", data=data, pk=robot.pk)
        self.response_200(response)
        robot.refresh_from_db()
        self.assertDictEqual(
            robot.strategy_parameters,
            {
                "code1": "new1",
                "code2": "new2",
            },
        )

    # retrieve strategy parameters
    def test_retrieve_strategy_parameters_permission(self):
        robot = RobotFactory()

        # anonymous user
        response = self.get("api:robot-strategy-parameters", pk=robot.pk)
        self.response_401(response)

        # normal user
        self.login(username=self.normal_user.username, password="password")
        response = self.get("api:robot-strategy-parameters", pk=robot.pk)
        self.response_403(response)

    def test_retrieve_nonexistent_robot_strategy_parameters(self):
        self.login(username=self.admin_user.username, password="password")
        response = self.get("api:robot-strategy-parameters", pk=999999)
        self.response_404(response)

    def test_retrieve_strategy_parameters(self):
        strategy = StrategyFactory(
            specification={
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
        )
        robot = RobotFactory(strategy=strategy, credential=self.admin_user_credential)
        self.login(username=self.admin_user.username, password="password")

        response = self.get("api:robot-strategy-parameters", pk=robot.pk)
        self.response_200(response)
        self.assertEqual(
            response.data,
            {
                "param1": "test1",
                "param2": "test2",
            },
        )

    # retrieve strategy spec view
    def test_retrieve_strategy_spec_view_permission(self):
        robot = RobotFactory()

        # anonymous user
        response = self.get("api:robot-strategy-spec-view", pk=robot.pk)
        self.response_401(response)

        # normal user
        self.login(username=self.normal_user.username, password="password")
        response = self.get("api:robot-strategy-spec-view", pk=robot.pk)
        self.response_403(response)

    def test_retrieve_nonexistent_robot_strategy_spec_view(self):
        self.login(username=self.admin_user.username, password="password")
        response = self.get("api:robot-strategy-spec-view", pk=999999)
        self.response_404(response)

    def test_retrieve_strategy_spec_view(self):
        strategy = StrategyFactory(
            specification={
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
        )
        robot = RobotFactory(strategy=strategy, credential=self.admin_user_credential)
        robot.strategy_parameters = {
            "param1": "new1",
            "param2": "new2",
        }
        robot.save(update_fields=["strategy_parameters"])
        self.login(username=self.admin_user.username, password="password")

        response = self.get("api:robot-strategy-spec-view", pk=robot.pk)
        self.response_200(response)
        self.assertEqual(
            response.data,
            {
                "specVersion": "v0.1.0",
                "parameters": [
                    {
                        "code": "param1",
                        "name": "Param1",
                        "type": "string",
                        "description": "",
                        "default": "test1",
                        "value": "new1",
                        "editable": True,
                    },
                    {
                        "code": "param2",
                        "name": "Param2",
                        "type": "string",
                        "description": "",
                        "default": "test2",
                        "value": "new2",
                        "editable": True,
                    },
                ],
            },
        )

    # partial update asset record
    def test_partial_update_asset_record_permission(self):
        robot = RobotFactory()

        # anonymous user
        response = self.patch("api:robot-asset-record", pk=robot.pk)
        self.response_401(response)

        # normal user
        self.login(username=self.normal_user.username, password="password")
        response = self.patch("api:robot-asset-record", pk=robot.pk)
        self.response_403(response)

    def test_partial_update_nonexistent_robot_asset_record(self):
        self.login(username=self.admin_user.username, password="password")
        response = self.patch("api:robot-asset-record", pk=999999)
        self.response_404(response)

    def test_partial_update_asset_record(self):
        robot = RobotFactory(credential=self.admin_user_credential)
        self.login(username=self.admin_user.username, password="password")

        data = {"total_balance": 6666}
        response = self.patch(
            "api:robot-asset-record",
            pk=robot.pk,
            data=data,
        )
        self.response_200(response)
        robot.refresh_from_db()
        self.assertEqual(
            robot.asset_record.total_principal,
            0,
        )
        self.assertEqual(
            robot.asset_record.total_balance,
            6666,
        )

    # retrieve credential key
    def test_retrieve_credential_key_permission(self):
        robot = RobotFactory()

        # anonymous user
        response = self.get("api:robot-credential-key", pk=robot.pk)
        self.response_401(response)

        # normal user
        self.login(username=self.normal_user.username, password="password")
        response = self.get("api:robot-credential-key", pk=robot.pk)
        self.response_403(response)

    def test_retrieve_nonexistent_robot_credential_key(self):
        self.login(username=self.admin_user.username, password="password")
        response = self.get("api:robot-credential-key", pk=999999)
        self.response_404(response)

    def test_retrieve_credential_key(self):
        robot = RobotFactory(credential=self.admin_user_credential)
        self.login(username=self.admin_user.username, password="password")
        response = self.get("api:robot-credential-key", pk=robot.pk)
        self.response_200(response)
        self.assertEqual(
            response.data,
            robot.credential.key,
        )

    # list asset record snaps
    def test_list_robot_asset_record_snap_permission(self):
        robot = RobotFactory(credential=self.admin_user_credential)

        # anonymous
        response = self.get("api:robot-asset-record-snap-list", pk=robot.pk)
        self.response_401(response)

        # normal user
        self.login(username=self.normal_user.username, password="password")
        response = self.get("api:robot-asset-record-snap-list", pk=robot.pk)
        self.response_403(response)

    def test_list_nonexistent_robot_asset_record_snap(self):
        self.login(username=self.admin_user.username, password="password")
        response = self.get("api:robot-asset-record-snap-list", pk=999999)
        self.response_404(response)

    def test_list_robot_asset_record_snap(self):
        robot = RobotFactory(credential=self.admin_user_credential)
        self.login(username=self.admin_user.username, password="password")
        response = self.get("api:robot-asset-record-snap-list", pk=robot.pk)
        self.response_200(response)
