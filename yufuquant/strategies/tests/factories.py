import factory
from factory import DjangoModelFactory
from strategies.models import StrategyTemplate


class StrategyTemplateFactory(DjangoModelFactory):
    code = factory.Faker("word")
    name = factory.LazyAttribute(lambda obj: obj.code.title())
    description = factory.Faker("paragraph")
    parameter_spec = factory.LazyFunction(
        lambda: {
            "version": "v0",
            "specVersion": "v1.0",
            "fields": [
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
        model = StrategyTemplate
