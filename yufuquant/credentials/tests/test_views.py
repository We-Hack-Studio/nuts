from unittest import mock

import pytest
from rest_framework.reverse import reverse

from core.proxies.bybit import BybitExchangeProxy
from core.proxies.exceptions import ExchangeProxyException
from credentials.models import Credential
from exchanges.tests.factories import ExchangeFactory


@mock.patch.object(
    BybitExchangeProxy, "fetch_balance", mock.Mock(side_effect=ExchangeProxyException())
)
@pytest.mark.django_db
def test_bind_credential_atomically(client, django_user_model):
    username = "yufuquant"
    password = "test123456"
    django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    url = reverse("credential-list")
    exchange = ExchangeFactory(name="Bybit")
    data = {
        "api_key": "api-key",
        "secret": "secret",
        "exchange": exchange.pk,
    }
    response = client.post(url, data=data)
    assert response.status_code == 400
    assert Credential.objects.count() == 0
