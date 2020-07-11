from . import init_exchanges, init_superuser


def run():
    print("正在初始化数据库...")
    init_exchanges.run()
    init_superuser.run()
    print("数据库初始化成功!")
