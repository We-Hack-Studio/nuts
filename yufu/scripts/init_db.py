from exchanges.models import Exchange


def run():
    Exchange.objects.get_or_create(code="bybit", name="Bybit")
    print("数据库初始化成功！")
