import json
import pathlib

from django.conf import settings
from strategies.tests.factories import StrategyFactory


def run():
    name = "演示策略"
    spec = (
        pathlib.Path(str(settings.APPS_DIR))
        .joinpath("scripts", "fake", "strategy-specification.json")
        .read_text(encoding="utf-8")
    )
    StrategyFactory(
        name=name,
        specification=json.loads(spec),
    )
    print("Demo strategy was created.")
