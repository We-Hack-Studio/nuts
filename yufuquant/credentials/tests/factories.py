from django.utils.crypto import get_random_string

import factory
from credentials.models import Credential
from factory import DjangoModelFactory, Faker
from exchanges.tests.factories import ExchangeFactory
from users.tests.factories import UserFactory


class CredentialFactory(DjangoModelFactory):

    api_key = factory.Faker("sha1", raw_output=False)
    secret = factory.Faker("sha256", raw_output=False)
    passphrase = factory.LazyFunction(lambda: get_random_string(8))
    exchange = factory.SubFactory(ExchangeFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Credential
