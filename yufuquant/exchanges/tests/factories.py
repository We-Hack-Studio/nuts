import random

import factory
from exchanges.models import Exchange
from factory import DjangoModelFactory

EXCHANGE_LIST = ["Huobi", "OKEx", "Binance", "Bybit"]


class ExchangeFactory(DjangoModelFactory):
    code = factory.lazy_attribute(lambda o: o.name.lower())
    name = factory.LazyFunction(lambda: random.choice(EXCHANGE_LIST))
    name_zh = factory.lazy_attribute(lambda o: o.name)
    logo = factory.django.ImageField()
    active = True
    rank = factory.Sequence(lambda n: n)

    class Meta:
        model = Exchange
