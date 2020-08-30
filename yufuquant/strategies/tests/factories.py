import factory
from factory import DjangoModelFactory
from strategies.models import Strategy


class StrategyFactory(DjangoModelFactory):
    name = factory.Faker("word")
    description = factory.Faker("paragraph")
    specification = factory.LazyFunction(
        lambda: {
            "version": "v0",
            "specVersion": "v1.0",
            "parameters": [
                {
                    "code": "code",
                    "name": "Code",
                    "type": "string",
                    "description": "",
                    "default": "",
                    "editable": True,
                }
            ],
        }
    )

    class Meta:
        model = Strategy
