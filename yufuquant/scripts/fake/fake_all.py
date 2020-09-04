from django.db import transaction

from . import (
    _clean_db,
    _fake_exchanges,
    _fake_robots,
    _fake_strategies,
    _fake_superuser,
)


def run():
    with transaction.atomic():
        _clean_db.run()
        _fake_superuser.run()
        _fake_exchanges.run()
        _fake_strategies.run()
        _fake_robots.run()
        print("Done!")
