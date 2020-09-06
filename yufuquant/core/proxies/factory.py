from . import ExchangeProxy
from .bybit import BybitExchangeProxy
from .binance import BinanceExchangeProxy

exchange_code_to_proxy_cls = {
    "bybit": BybitExchangeProxy,
    "binance": BinanceExchangeProxy,
}


def exchange_proxy_factory(
    *, exchange_code: str, pair: str = "", test_net: bool = False, credential=None,
) -> ExchangeProxy:

    proxy_class = exchange_code_to_proxy_cls[exchange_code]
    proxy = proxy_class(pair=pair)
    if test_net:
        proxy.enable_test_net()

    if credential is not None:
        proxy.auth(credential=credential)

    return proxy
