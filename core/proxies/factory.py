from credentials.models import Credential

from .bybit import BybitExchangeProxy


def exchange_proxy_factory(
    *, exchange_code: str, pair: str = "", test_net: bool = False
):
    exchange_proxy_map = {
        "bybit": BybitExchangeProxy,
    }

    proxy_class = exchange_proxy_map[exchange_code]
    proxy = proxy_class(pair=pair)
    if test_net:
        proxy.enable_test_net()

    return proxy
