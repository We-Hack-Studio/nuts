import factory
from credentials.tests.factories import CredentialFactory
from factory import DjangoModelFactory
from robots.models import Robot
from strategies.tests.factories import StrategyFactory


class RobotFactory(DjangoModelFactory):
    name = factory.Faker("name")
    pair = "BTCUSDT"
    market_type = "spots"
    base_currency = "BTC"
    quote_currency = "USDT"
    target_currency = "USDT"
    credential = factory.SubFactory(CredentialFactory)
    strategy = factory.SubFactory(StrategyFactory)

    class Meta:
        model = Robot
