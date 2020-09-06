from scripts.db import _init_exchanges, _init_superuser


def run():
    _init_superuser.run()
    _init_exchanges.run()
    print("Database has been initialized!")
