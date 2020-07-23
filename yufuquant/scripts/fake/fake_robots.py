from credentials.tests.factories import CredentialFactory
from exchanges.tests.factories import ExchangeFactory
from robots.tests.factories import RobotFactory
from users.models import User

fake_data = [
    {"code": "bybit", "name": "Bybit", "name_zh": "Bybit", "pair": "BTCUSD"},
    {"code": "binance", "name": "Binance", "name_zh": "币安", "pair": "BTCUSD"},
    {"code": "huobi", "name": "Huobi", "name_zh": "火币", "pair": "BTC-USD"},
    {"code": "okex", "name": "OKEx", "name_zh": "OKEx", "pair": "BTC-USD-200925"},
]


def run():
    user = User.objects.create_user(
        username="user", password="user123456", email="user@yufuquant.cc"
    )
    for entry in fake_data:
        # Todo: 生成资产时报错
        exchange = ExchangeFactory(
            code=entry["code"], name=entry["name"], name_zh=entry["name_zh"]
        )
        credential = CredentialFactory(user=user, exchange=exchange)
        RobotFactory(credential=credential)
