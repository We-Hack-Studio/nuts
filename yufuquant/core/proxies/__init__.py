import ccxt
from django.core.exceptions import ValidationError

from .exceptions import ExchangeProxyException


class ExchangeProxy:
    id = ""
    name = ""
    pairs = []
    ccxt_symbols = {}
    default_ccxt_exchange_configs = {
        "enableRateLimit": True,
    }
    ccxt_exchange_class = ccxt.Exchange

    def __init__(self, pair: str = ""):
        if pair:
            self.pair = pair
            self.ccxt_symbol = self.ccxt_symbols[pair]
        self.ccxt_exchange: ccxt.Exchange = self.ccxt_exchange_class(
            self.get_ccxt_exchange_configs()
        )

    def get_ccxt_exchange_configs(self):
        return self.default_ccxt_exchange_configs

    def enable_test_net(self):
        try:
            self.ccxt_exchange.set_sandbox_mode(enabled=True)
        except ccxt.NotSupported:
            pass

    def auth(self, credential):
        api_key = credential["api_key"]
        secret = credential["secret"]
        passphrase = credential.get("passphrase", "")
        self.ccxt_exchange.apiKey = api_key
        self.ccxt_exchange.secret = secret
        if passphrase:
            self.ccxt_exchange.password = passphrase

    def fetch_balance(self, params=None):
        try:
            result = self.ccxt_exchange.fetch_balance(params=params)
        except ccxt.AuthenticationError:
            raise ValidationError("无效的凭据")
        except (ccxt.ExchangeError, ccxt.NetworkError) as e:
            raise ExchangeProxyException(f"账户资产获取失败，请稍后重试。详细代理异常信息：{str(e)}")

        ret = {}
        for currency in ["BTC", "USDT", "EOS", "ETH"]:
            ret[currency] = result[currency]
        return ret
