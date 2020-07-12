import random

from django.conf import settings

import factory
from factory import DjangoModelFactory
from exchanges.models import Exchange


class ExchangeFactory(DjangoModelFactory):

    code = factory.lazy_attribute(lambda o: o.name.lower())
    name = factory.LazyFunction(lambda: random.choice(settings.SUPPORTED_EXCHANGE_LIST))
    name_zh = factory.lazy_attribute(lambda o: o.name)
    logo = factory.django.ImageField()
    active = True
    rank = factory.Sequence(lambda n: n)

    class Meta:
        model = Exchange
