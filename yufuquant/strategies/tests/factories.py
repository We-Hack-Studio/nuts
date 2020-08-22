import factory
from factory import DjangoModelFactory
from strategies.models import StrategyTemplate


class StrategyTemplateFactory(DjangoModelFactory):
    code = factory.Faker("word")
    name = factory.LazyAttribute(lambda obj: obj.code.title())
    description = factory.Faker("paragraph")
    parameter_spec = '{"key":"value"}'

    class Meta:
        model = StrategyTemplate
