import pathlib

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from exchanges.models import Exchange
from exchanges.tests.factories import ExchangeFactory


def run():
    print("Creating exchanges")
    exchange_list = [
        ("Huobi", "火币"),
        ("Binance", "币安"),
        ("OKEx", "OKEx"),
        ("Bybit", "Bybit"),
    ]
    for i, (name, name_zh) in enumerate(exchange_list):
        code = name.lower()
        logo = pathlib.Path(str(settings.APPS_DIR)).joinpath(
            "scripts", "fake", "exchange-logos", f"{code}.jpg"
        )
        Exchange.objects.create(
            code=code,
            name=name,
            name_zh=name_zh,
            logo=SimpleUploadedFile(name=f"{code}.jpg", content=logo.read_bytes()),
            active=True,
            rank=i,
        )
