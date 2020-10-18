import json

from credentials.tests.factories import CredentialFactory
from django.db.models import F
from exchanges.tests.factories import ExchangeFactory
from freezegun import freeze_time
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from robots.models import Robot
from robots.serializers import RobotListSerializer, RobotRetrieveSerializer
from strategies.tests.factories import StrategyFactory
from test_plus import APITestCase
from users.models import User

from .factories import RobotFactory


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
        content_json = json.loads(response.content)
        self.assertEqual(len(content_json["data"]), 5)

        request = self.api_request_factory.get(self.robot_list_url)
        serializer = RobotListSerializer(
            instance=Robot.objects.all()
            .order_by("-created_at")
            .annotate(strategy_name=F("strategy__name")),
            many=True,
            context={"request": Request(request)},
        )
        print(response.data)
        print(serializer.data)
        self.assertEqual(response.data, serializer.data)

    def test_list_robot_include_asset_record(self):
        robot = RobotFactory(credential=self.admin_user_credential)
        self.login(username=self.admin_user.username, password="password")
        response = self.get("api:robot-list", data={"include": "asset_record"})
        self.response_200(response)
        content_json = json.loads(response.content)

        """
        "included": [
            {
                "type": "asset_records",
                "id": "1",
                "attributes": {
                    "currency": "USDT",
                    "total_principal": 0.0,
                    "total_balance": 0.0,
                    "total_pnl_abs": 0.0,
                    "total_pnl_abs_24h": 0.0,
                    "total_pnl_rel_ptg": "0.00%",
                    "total_pnl_rel_ptg_24h": "0.00%"
                }
            }
        ]
        """
        self.assertIn("included", content_json)
        self.assertEqual(len(content_json["included"]), 1)
        self.assertEqual(content_json["included"][0]["type"], "asset_records")
        self.assertEqual(content_json["included"][0]["id"], str(robot.asset_record.pk))

    def test_list_robot_include_credential_exchange(self):
        exchange = ExchangeFactory(code="binance")
        credential = CredentialFactory(exchange=exchange, user=self.admin_user)
        RobotFactory(credential=credential)
        self.login(username=self.admin_user.username, password="password")
        response = self.get("api:robot-list", data={"include": "credential.exchange"})
        self.response_200(response)
        content_json = json.loads(response.content)

        """
        "included": [
            {
                "type": "exchanges",
                "id": "4",
                "attributes": {
                    "code": "binance",
                    "name": "Binance",
                    "name_zh": "币安",
                    "logo_url": "http://127.0.0.1:8000/media/CACHE/images/exchanges/logos/binance/binance.png",
                    "active": true,
                    "rank": 3,
                    "created_at": "2020-10-18T11:34:24.972063+08:00",
                    "modified_at": "2020-10-18T11:34:24.972063+08:00"
                }
            }
        ]
        """
        self.assertIn("included", content_json)
        self.assertEqual(len(content_json["included"]), 2)
        self.assertEqual(content_json["included"][0]["type"], "credentials")
        self.assertEqual(content_json["included"][0]["id"], str(credential.pk))
        self.assertEqual(content_json["included"][1]["type"], "exchanges")
        self.assertEqual(content_json["included"][1]["id"], str(exchange.pk))

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
            "data": {
                "type": "robots",
                "attributes": {
                    "name": "Invalid",
                    "pair": "BTCUSDT",
                    "market_type": "spots",
                    "base_currency": "BTC",
                    "quote_currency": "USDT",
                    "target_currency": "USDT",
                    # invalid data
                    "credential": {
                        "type": "credentials",
                        "id": 999999,
                    },
                    "strategy": {
                        "type": "strategies",
                        "id": 999999,
                    },
                },
            }
        }
        response = self.post("api:robot-list", data=data)
        self.response_400(response)
        content_json = json.loads(response.content)
        self.assertIn("errors", content_json)
        error_sources = []
        for error in content_json["errors"]:
            error_sources.append(error["source"])
        self.assertEqual(
            error_sources,
            [
                {"pointer": "/data/attributes/credential"},
                {"pointer": "/data/attributes/strategy"},
            ],
        )

    @freeze_time("2020-10-18 03:21:34.456789")  # UTC
    def test_create_valid_robot(self):
        credential = CredentialFactory(user=self.admin_user)
        strategy = StrategyFactory()
        self.login(username=self.admin_user.username, password="password")
        data = {
            "data": {
                "type": "robots",
                "attributes": {
                    "name": "Valid",
                    "pair": "BTCUSDT",
                    "market_type": "linear_perpetual",
                    "target_currency": "USDT",
                    "credential": {
                        "type": "credentials",
                        "id": credential.pk,
                    },
                    "strategy": {
                        "type": "strategies",
                        "id": strategy.pk,
                    },
                },
            }
        }
        response = self.post("api:robot-list", data=data)
        self.response_201(response)
        content_json = json.loads(response.content)
        self.assertEqual(
            content_json,
            {
                "data": {
                    "type": "robots",
                    "id": "1",
                    "attributes": {
                        "name": "Valid",
                        "pair": "BTCUSDT",
                        "market_type": "linear_perpetual",
                        "target_currency": "USDT",
                        "base_currency": "",
                        "quote_currency": "",
                        "created_at": "2020-10-18T11:21:34.456789+08:00",
                        "modified_at": "2020-10-18T11:21:34.456789+08:00",
                    },
                    "relationships": {
                        "credential": {
                            "data": {"type": "credentials", "id": "2"},
                        },
                        "strategy": {
                            "data": {"type": "strategies", "id": "1"},
                        },
                    },
                }
            },
        )

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
        serializer = RobotRetrieveSerializer(instance=robot)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_robot_include_asset_record(self):
        robot = RobotFactory(credential=self.admin_user_credential)
        self.login(username=self.admin_user.username, password="password")
        response = self.get(
            "api:robot-detail",
            pk=robot.pk,
            data={"include": "asset_record"},
        )
        self.response_200(response)
        content_json = json.loads(response.content)

        """
        "included": [
            {
                "type": "asset_records",
                "id": "1",
                "attributes": {
                    "currency": "USDT",
                    "total_principal": 0.0,
                    "total_balance": 0.0,
                    "total_pnl_abs": 0.0,
                    "total_pnl_abs_24h": 0.0,
                    "total_pnl_rel_ptg": "0.00%",
                    "total_pnl_rel_ptg_24h": "0.00%"
                }
            }
        ]
        """
        self.assertIn("included", content_json)
        self.assertEqual(len(content_json["included"]), 1)
        self.assertEqual(content_json["included"][0]["type"], "asset_records")
        self.assertEqual(content_json["included"][0]["id"], str(robot.asset_record.pk))

    def test_retrieve_robot_include_credential_exchange(self):
        exchange = ExchangeFactory(code="binance")
        credential = CredentialFactory(exchange=exchange, user=self.admin_user)
        robot = RobotFactory(credential=credential)
        self.login(username=self.admin_user.username, password="password")
        response = self.get(
            "api:robot-detail",
            pk=robot.pk,
            data={"include": "credential.exchange"},
        )
        self.response_200(response)
        content_json = json.loads(response.content)

        """
        "included": [
            {
                "type": "credentials",
                "id": "2",
                "attributes": {
                    "note": "Note",
                    "api_key": "a550************ed0c",
                    "secret": "897a*************************17a2",
                    "passphrase": "********",
                    "test_net": false,
                    "created_at": "2020-10-18T11:34:25.059003+08:00",
                    "modified_at": "2020-10-18T11:34:25.059003+08:00"
                },
                "relationships": {
                    "exchange": {
                        "data": {
                            "type": "exchanges",
                            "id": "2"
                        }
                    }
                }
            },
            {
                "type": "exchanges",
                "id": "2",
                "attributes": {
                    "code": "binance",
                    "name": "Binance",
                    "name_zh": "币安",
                    "logo_url": "http://127.0.0.1:8000/media/CACHE/images/exchanges/logos/binance/binance.png",
                    "active": true,
                    "rank": 1,
                    "created_at": "2020-10-18T11:34:24.966024+08:00",
                    "modified_at": "2020-10-18T11:34:24.966024+08:00"
                }
            }
        ]
        """
        self.assertIn("included", content_json)
        self.assertEqual(len(content_json["included"]), 2)

        self.assertEqual(content_json["included"][0]["type"], "credentials")
        self.assertEqual(content_json["included"][0]["id"], str(credential.pk))

        self.assertEqual(content_json["included"][1]["type"], "exchanges")
        self.assertEqual(content_json["included"][1]["id"], str(exchange.pk))

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
            "data": {
                "type": "robots",
                "id": robot.pk,
                "attributes": {
                    "name": "New",
                },
            }
        }
        response = self.patch("api:robot-detail", pk=robot.pk, data=data)
        self.response_200(response)
        content_json = json.loads(response.content)
        self.assertEqual(
            content_json,
            {
                "data": {
                    "type": "robots",
                    "id": str(robot.pk),
                    "attributes": {"name": "New"},
                },
            },
        )

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
        content_json = json.loads(response.content)
        self.assertEqual(content_json, {"data": {"detail": "pong"}})

    # adjust strategy parameters
    def test_adjust_strategy_parameters_permission(self):
        robot = RobotFactory()

        # anonymous user
        response = self.post("api:robot-strategy-parameters", pk=robot.pk)
        self.response_401(response)

        # normal user
        self.login(username=self.normal_user.username, password="password")
        response = self.post("api:robot-strategy-parameters", pk=robot.pk)
        self.response_403(response)

    def test_adjust_nonexistent_robot_strategy_parameters(self):
        self.login(username=self.admin_user.username, password="password")
        response = self.post("api:robot-strategy-parameters", pk=999999)
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
            "data": {
                "type": "robots",
                "id": robot.pk,
                "attributes": {
                    "code1": "new1",
                    "code2": "new2",
                },
            }
        }
        response = self.post("api:robot-strategy-parameters", pk=robot.pk, data=data)
        self.response_200(response)
        content_json = json.loads(response.content)
        self.assertEqual(content_json, {"data": {"detail": "ok"}})
        robot.refresh_from_db()
        self.assertDictEqual(
            robot.strategy_parameters,
            {
                "code1": "new1",
                "code2": "new2",
            },
        )

    # strategy parameters
    def test_strategy_parameters_permission(self):
        robot = RobotFactory()

        # anonymous user
        response = self.get("api:robot-strategy-parameters", pk=robot.pk)
        self.response_401(response)

        # normal user
        self.login(username=self.normal_user.username, password="password")
        response = self.get("api:robot-strategy-parameters", pk=robot.pk)
        self.response_403(response)

    def test_nonexistent_robot_strategy_parameters(self):
        self.login(username=self.admin_user.username, password="password")
        response = self.get("api:robot-strategy-parameters", pk=999999)
        self.response_404(response)

    def test_strategy_parameters(self):
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
        content_json = json.loads(response.content)
        self.assertEqual(
            content_json,
            {
                "data": {
                    "param1": "test1",
                    "param2": "test2",
                },
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
        content_json = json.loads(response.content)
        self.assertEqual(
            content_json,
            {
                "data": {
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
                }
            },
        )

    # update asset record
    def test_update_asset_record_permission(self):
        robot = RobotFactory()

        # anonymous user
        response = self.patch("api:robot-asset-record", pk=robot.pk)
        self.response_401(response)

        # normal user
        self.login(username=self.normal_user.username, password="password")
        response = self.patch("api:robot-asset-record", pk=robot.pk)
        self.response_403(response)

    def test_update_nonexistent_robot_asset_record(self):
        self.login(username=self.admin_user.username, password="password")
        response = self.patch("api:robot-asset-record", pk=999999)
        self.response_404(response)

    def test_update_asset_record(self):
        robot = RobotFactory(credential=self.admin_user_credential)
        self.login(username=self.admin_user.username, password="password")

        data = {
            "data": {
                "type": "robots",
                "id": robot.pk,
                "attributes": {"total_balance": 6666},
            }
        }
        response = self.patch(
            "api:robot-asset-record",
            pk=robot.pk,
            data=data,
        )
        self.response_200(response)
        content_json = json.loads(response.content)
        self.assertEqual(content_json, {"data": {"detail": "ok"}})

        robot.refresh_from_db()
        self.assertEqual(
            robot.asset_record.total_principal,
            0,
        )
        self.assertEqual(
            robot.asset_record.total_balance,
            6666,
        )

    # retrieve credential keys
    def test_retrieve_credential_keys_permission(self):
        robot = RobotFactory()

        # anonymous user
        response = self.get("api:robot-credential-keys", pk=robot.pk)
        self.response_401(response)

        # normal user
        self.login(username=self.normal_user.username, password="password")
        response = self.get("api:robot-credential-keys", pk=robot.pk)
        self.response_403(response)

    def test_retrieve_nonexistent_robot_credential_keys(self):
        self.login(username=self.admin_user.username, password="password")
        response = self.get("api:robot-credential-keys", pk=999999)
        self.response_404(response)

    def test_retrieve_credential_keys(self):
        robot = RobotFactory(credential=self.admin_user_credential)
        self.login(username=self.admin_user.username, password="password")
        response = self.get("api:robot-credential-keys", pk=robot.pk)
        self.response_200(response)
        content_json = json.loads(response.content)
        self.assertEqual(
            content_json,
            {"data": robot.credential.keys},
        )
