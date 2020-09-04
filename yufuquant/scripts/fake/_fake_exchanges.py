import pathlib

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from exchanges.tests.factories import ExchangeFactory


def run():
    for exchange in ["Huobi", "Binance", "OKEx", "Bybit"]:
        code = exchange.lower()
        logo = pathlib.Path(str(settings.APPS_DIR)).joinpath(
            "scripts", "fake", "exchange-logos", f"{code}.jpg"
        )
        ExchangeFactory(
            code=code,
            name=exchange,
            logo=SimpleUploadedFile(name=f"{code}.jpg", content=logo.read_bytes()),
        )
    print("Exchanges were created.")
