from scripts.db import _init_exchanges, _init_superuser


def run():
    print("正在初始化数据库...")
    _init_exchanges.run()
    _init_superuser.run()
    print("数据库初始化成功!")
