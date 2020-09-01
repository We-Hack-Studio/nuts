from exchanges.models import Exchange


def run():
    print("初始化生成交易所数据...")
    Exchange.objects.get_or_create(code="bybit", name="Bybit")
