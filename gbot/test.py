from pprint import pprint
from datetime import datetime, timedelta

import ccxt

# def timestamp_millisecond(dt=None, delta=None):
#     if not dt:
#         dt = datetime.now()
#
#     if delta is not None:
#         dt = dt + delta
#
#     return int(dt.timestamp() * 1000)
#
#
# bybit = ccxt.bybit(
#     {
#         "enableRateLimit": True,
#         "options": {"adjustForTimeDifference": True, "recvWindow": 10 * 1000},
#     }
# )
# bybit.set_sandbox_mode(enabled=True)
# bybit.apiKey = "MkFogsh7NCl9OOoAlP"
# bybit.secret = "Mqov7GGjV5apciGEb2VKDyAswESvXPUYgJU2"
# res = bybit.fetch_closed_orders(
#     symbol="BTC/USD",
#     # since=timestamp_millisecond(dt=datetime.now(), delta=timedelta(hours=-1)),
#     params={"order_status": "Filled"},
# )
# pprint(res)

from gbot.main import DingTalkHandler
import logging
import logging.config
from gbot import config

DEFAULT_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s %(levelname)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "dingtalk": {
            "level": logging.DEBUG,
            "class": "gbot.main.DingTalkHandler",
            "formatter": "simple",
        }
    },
    "loggers": {"test": {"handlers": ["dingtalk"], "level": logging.DEBUG}},
}
logging.config.dictConfig(DEFAULT_LOGGING)

logger = logging.getLogger("test")
logging.config.dictConfig(DEFAULT_LOGGING)

logger.info("钉钉日志推送测试")
