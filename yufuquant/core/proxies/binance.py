import ccxt

from . import ExchangeProxy


class BinanceExchangeProxy(ExchangeProxy):
    id = "binance"
    name = "Binance"
    pairs = ["BTCUSDT"]
    ccxt_symbols = {"BTCUSDT": "BTC/USDT"}
    ccxt_exchange_class: ccxt.binance = ccxt.binance
    default_ccxt_exchange_configs = {
        "enableRateLimit": True,
        "options": {"adjustForTimeDifference": True},
    }

    def set_market_type(self, market_type: str):
        m = {
            "spots": "spot",
            "futures": "future",
        }
        self.ccxt_exchange.options["defaultType"] = m[market_type]
