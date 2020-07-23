import ccxt

from . import ExchangeProxy


class BybitExchangeProxy(ExchangeProxy):
    id = "bybit"
    name = "Bybit"
    pairs = ["BTCUSD"]
    ccxt_symbols = {"BTCUSD": "BTC/USD"}
    ccxt_exchange_class: ccxt.bybit = ccxt.bybit
    default_ccxt_exchange_configs = {
        "enableRateLimit": True,
        "options": {"adjustForTimeDifference": True},
    }

    def fetch_balance(self, params=None):
        def extend(*args):
            if "coin" in args[0]:
                return {}
            return ccxt.Exchange.extend(*args)

        # Todo:
        # Bybit 已更新资产接口，不传任何参数将返回所有资产余额。ccxt 目前的处理方式是默认传递 coin=BTC 参数进行查询，
        # 这里我们对 extend 方法进行 monkey path，使查询参数变为空。
        self.ccxt_exchange.extend = extend
        return super().fetch_balance()
