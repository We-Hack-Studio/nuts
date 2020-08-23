import factory
from credentials.tests.factories import CredentialFactory
from django.utils import timezone
from django.utils.crypto import get_random_string
from factory import DjangoModelFactory
from robots.models import Robot


class RobotFactory(DjangoModelFactory):
    name = factory.Faker("name")
    pair = "BTCUSD"
    margin_currency = "BTC"
    start_time = factory.LazyFunction(lambda: timezone.now)
    ping_time = factory.LazyFunction(lambda: timezone.now)
    credential = factory.SubFactory(CredentialFactory)
    stream_key = factory.LazyFunction(lambda: get_random_string(30))

    class Meta:
        model = Robot
