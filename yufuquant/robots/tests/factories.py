import factory
from credentials.tests.factories import CredentialFactory
from django.utils import timezone
from factory import DjangoModelFactory
from robots.models import Robot
from strategies.tests.factories import StrategyFactory


class RobotFactory(DjangoModelFactory):
    name = factory.Faker("name")
    pair = "BTCUSD"
    market_type = "futures"
    target_currency = "BTC"
    credential = factory.SubFactory(CredentialFactory)
    strategy = factory.SubFactory(StrategyFactory)

    class Meta:
        model = Robot
