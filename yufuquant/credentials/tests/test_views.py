# from unittest import mock
#
# import pytest
# from rest_framework.reverse import reverse
#
# from core.proxies.bybit import BybitExchangeProxy
# from core.proxies.exceptions import ExchangeProxyException
# from credentials.models import Credential
# from exchanges.tests.factories import ExchangeFactory
#
#
# @mock.patch.object(
#     BybitExchangeProxy,
#     "fetch_balance",
#     mock.Mock(
#         return_value={
#             "BTC": {"free": 1, "used": 0.0, "total": 1},
#             "USDT": {"free": 1000, "used": 0.0, "total": 1000},
#             "EOS": {"free": 100, "used": 0.0, "total": 100},
#             "ETH": {"free": 10, "used": 0.0, "total": 10},
#         }
#     ),
# )
# @pytest.mark.django_db
# def test_bind_credential_then_make_assets(client, django_user_model):
#     username = "yufuquant"
#     password = "test123456"
#     django_user_model.objects.create_user(username=username, password=password)
#     client.login(username=username, password=password)
#     url = reverse("credential-list")
#     exchange = ExchangeFactory(name="Bybit")
#     data = {
#         "api_key": "api-key",
#         "secret": "secret",
#         "exchange": exchange.pk,
#     }
#     response = client.post(url, data=data)
#     assert response.status_code == 201
#     assert Credential.objects.count() == 1
#     assert Asset.objects.count() == 4
#
#     asset_btc = Asset.objects.get(currency="BTC")
#     assert asset_btc.principal == 1
#     assert asset_btc.balance == 1
#
#     asset_usdt = Asset.objects.get(currency="USDT")
#     assert asset_usdt.principal == 1000
#     assert asset_usdt.balance == 1000
#
#     asset_eos = Asset.objects.get(currency="EOS")
#     assert asset_eos.principal == 100
#     assert asset_eos.balance == 100
#
#     asset_eth = Asset.objects.get(currency="ETH")
#     assert asset_eth.principal == 10
#     assert asset_eth.balance == 10
#
#
# @mock.patch.object(
#     BybitExchangeProxy, "fetch_balance", mock.Mock(side_effect=ExchangeProxyException())
# )
# @pytest.mark.django_db
# def test_bind_credential_atomically(client, django_user_model):
#     username = "yufuquant"
#     password = "test123456"
#     django_user_model.objects.create_user(username=username, password=password)
#     client.login(username=username, password=password)
#     url = reverse("credential-list")
#     exchange = ExchangeFactory(name="Bybit")
#     data = {
#         "api_key": "api-key",
#         "secret": "secret",
#         "exchange": exchange.pk,
#     }
#     response = client.post(url, data=data)
#     assert response.status_code == 400
#     assert Credential.objects.count() == 0
