import ccxt

from . import ExchangeProxy
from .exceptions import ExchangeProxyException


class BybitExchangeProxy(ExchangeProxy):
    id = "bybit"
    name = "Bybit"
    pairs = ["BTCUSD"]
    ccxt_symbols = {"BTCUSD": "BTC/USD"}
    ccxt_exchange_class = ccxt.bybit
    default_ccxt_exchange_configs = {
        "enableRateLimit": True,
        "options": {"adjustForTimeDifference": True},
    }

    def fetch_balance(self, params=None):
        try:
            btc_balance = self.ccxt_exchange.fetch_balance(params={"coin": "BTC"})
            usdt_balance = self.ccxt_exchange.fetch_balance(params={"coin": "USDT"})
            eth_balance = self.ccxt_exchange.fetch_balance(params={"coin": "ETH"})
            eos_balance = self.ccxt_exchange.fetch_balance(params={"coin": "EOS"})
        except ccxt.ExchangeError as e:
            raise ExchangeProxyException(str(e))

        ret = {
            "BTC": btc_balance["BTC"],
            "USDT": usdt_balance["USDT"],
            "ETH": eth_balance["ETH"],
            "EOS": eos_balance["EOS"],
        }
        return ret
