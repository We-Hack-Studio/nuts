from . import ExchangeProxy
from .bybit import BybitExchangeProxy

exchange_code_to_proxy_cls = {
    "bybit": BybitExchangeProxy,
}


def exchange_proxy_factory(
    *, exchange_code: str, pair: str = "", test_net: bool = False
) -> ExchangeProxy:

    proxy_class = exchange_code_to_proxy_cls[exchange_code]
    proxy = proxy_class(pair=pair)
    if test_net:
        proxy.enable_test_net()

    return proxy
