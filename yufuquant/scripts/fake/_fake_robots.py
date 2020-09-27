from credentials.tests.factories import CredentialFactory
from exchanges.models import Exchange
from robots.tests.factories import RobotFactory
from strategies.models import Strategy
from users.models import User

fake_data = [
    {
        "code": "bybit",
        "name": "Bybit",
        "name_zh": "Bybit",
        "pair": "BTCUSD",
        "market_type": "inverse_perpetual",
        "target_currency": "BTC",
    },
    {
        "code": "binance",
        "name": "Binance",
        "name_zh": "币安",
        "pair": "ETHUSDT",
        "market_type": "linear_perpetual",
        "target_currency": "USDT",
    },
    {
        "code": "huobi",
        "name": "Huobi",
        "name_zh": "火币",
        "pair": "BTC-USDT",
        "market_type": "spots",
        "target_currency": "USDT",
        "base_currency": "BTC",
        "quote_currency": "USDT",
    },
    {
        "code": "okex",
        "name": "OKEx",
        "name_zh": "OKEx",
        "pair": "EOS-USD-200925",
        "market_type": "inverse_delivery",
        "target_currency": "EOS",
    },
]


def run():
    user = User.objects.get(username="admin")
    strategy = Strategy.objects.get(name="演示策略")
    for entry in fake_data:
        exchange = Exchange.objects.get(code=entry["code"])
        credential = CredentialFactory(user=user, exchange=exchange)
        RobotFactory(credential=credential, strategy=strategy)
