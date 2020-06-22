import logging.config
import random
import string
import time
from datetime import datetime

import ccxt
import requests

from dingtalkchatbot.chatbot import DingtalkChatbot
import config


class HttpClient(object):
    headers = {"Authorization": f"Token {config.TOKEN}"}

    def __init__(self):
        self.base_url: str = config.SERVER_BASE_URL.rstrip("/")

    def fetch_grids(self):
        grids = self._request("GET", INTERNAL_GRIDS_REQ_PATH)
        return grids

    def fetch_robot_config(self):
        cfg = self._request("GET", INTERNAL_ROBOT_CONFIG_REQ_PATH)
        return cfg

    def update_grids(self, grids):
        self._request("PATCH", INTERNAL_GRIDS_REQ_PATH, json=grids)

    def update_robot(self, data):
        self._request("PATCH", INTERNAL_ROBOT_REQ_PATH, json=data)

    def create_log(self, msg):
        data = {"msg": msg, "robot_id": config.ROBOT_ID}
        self._request("POST", INTERNAL_ROBOT_LOG_REQ_PATH, json=data)

    def _request(
        self, method, req_path, headers=None, params=None, data=None, json=None
    ):
        url = self.base_url + req_path
        response = requests.request(
            method,
            url,
            headers=headers or self.headers,
            params=params,
            data=data,
            json=json,
        )
        response.raise_for_status()
        return response.json()


# 日志配置
class DingTalkHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self.ding_bot = DingtalkChatbot(
            config.DINGTALK_WEBHOOK, secret=config.DINGTALK_SECRET
        )

    def emit(self, record):
        try:
            msg = self.format(record)
            self.ding_bot.send_text(msg=msg)
        except Exception:
            self.handleError(record)


class RemoteHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self.client = HttpClient()

    def emit(self, record):
        try:
            self.client.create_log(msg=record.msg)
        except Exception:
            self.handleError(record)


logger = logging.getLogger("bot")
remote_logger = logging.getLogger("bot.remote")
full_logger = logging.getLogger("bot.full")
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
        "console": {
            "level": config.LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "dingtalk": {
            "level": logging.DEBUG,
            "class": "main.DingTalkHandler",
            "formatter": "simple",
        },
        "remote": {
            "level": logging.DEBUG,
            "class": "main.RemoteHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "bot": {"handlers": ["console"], "level": config.LOG_LEVEL},
        "bot.remote": {"handlers": ["console", "remote"], "level": logging.DEBUG},
        "bot.full": {
            "handlers": ["console", "remote", "dingtalk"],
            "level": logging.DEBUG,
        },
    },
}
logging.config.dictConfig(DEFAULT_LOGGING)

# API
INTERNAL_GRIDS_REQ_PATH = "/internal/grids/"
INTERNAL_ROBOT_LOG_REQ_PATH = "/internal/robots/logs/"
INTERNAL_ROBOT_CONFIG_REQ_PATH = "/internal/robots/{robot_id}/config/".format(
    robot_id=config.ROBOT_ID
)
INTERNAL_ROBOT_REQ_PATH = "/internal/robots/{robot_id}/".format(
    robot_id=config.ROBOT_ID
)


class GridBot(object):
    pass


class BybitGridBot(GridBot):
    id = "bybit"
    name = "Bybit"
    ccxt_symbols = {
        "BTCUSD": "BTC/USD",
        "ETHUSD": "ETH/USD",
        "EOSUSD": "EOS/USD",
    }
    ccxt_exchange_class = ccxt.bybit

    def __init__(self, pair):
        self.pair = pair
        self.ccxt_symbol: str = self.ccxt_symbols[self.pair]
        self.ccxt_exchange = self.ccxt_exchange_class(
            {
                "enableRateLimit": True,
                "options": {"adjustForTimeDifference": True, "recvWindow": 10 * 1000},
            }
        )
        self.client = HttpClient()
        self.grids = []
        self.position = {
            "dir": 0,
            "qty": 0.0,
            "avg_price": 0.0,
            "liq_price": 0.0,
            "unrealised_pnl": 0.0,
            "leverage": 0.0,
        }
        self.balance = 0.0
        self._api_key = ""
        self._secret = ""
        self._synced_order_set = set()
        self._grid_id_index_map = {}
        now = self.timestamp_millisecond()
        self._timestamp_markers = {
            "earliest_open_order": now,
            "reset_open_order": now,
        }
        self._order_sync_window = 1 * 60 * 60 * 1000
        self._open_orders_reset_interval = 30 * 60 * 1000

    def sync_config(self):
        cfg = self.client.fetch_robot_config()
        self._api_key = cfg["credential_keys"]["api_key"]
        self._secret = cfg["credential_keys"]["secret"]

    def load_grids(self):
        grids = self.client.fetch_grids()
        self.grids = grids
        for i, grid in enumerate(grids):
            self._grid_id_index_map[grid["id"]] = i

    def place_order(self, *, order_dir, qty, price, cid=""):
        dir_mapping = {
            -1: "sell",
            1: "buy",
        }
        self.ccxt_exchange.create_order(
            symbol=self.ccxt_symbol,
            type="limit",
            side=dir_mapping[order_dir],
            amount=qty,
            price=price,
            params={"time_in_force": "PostOnly", "order_link_id": cid},
        )

    def enable_test_net(self):
        self.ccxt_exchange.set_sandbox_mode(enabled=True)

    def place_orders_batch(self, orders):
        for order_args in orders:
            self.place_order(**order_args)

    def _find_grid_order(self, orders, grid_id):
        for order in orders:
            cid: str = order["info"]["order_link_id"]
            if "-" in cid and grid_id == int(cid.split("-", 1)[0]):
                return order

    def ensure_order(self):
        now = self.timestamp_millisecond()
        if (
            now
            > self._timestamp_markers["reset_open_order"]
            + self._open_orders_reset_interval
        ):
            self.ccxt_exchange.cancel_all_orders(symbol=self.ccxt_symbol)
            self._timestamp_markers["reset_open_order"] = now

        last_price = self.get_last_price()
        bid, ask = self.get_best_price()
        open_orders = self.ccxt_exchange.fetch_open_orders(
            symbol=self.ccxt_symbol, limit=50
        )
        order_args_list = []
        for grid in self.grids:
            grid_id = grid["id"]
            if self._find_grid_order(open_orders, grid_id):
                continue

            if grid["holding"]:
                order_args = {
                    "order_dir": 1,
                    "qty": grid["entry_qty"],
                    "price": min(
                        grid["exit_price"], ask - 0.5, self.position["avg_price"]
                    ),
                }
            else:
                if grid["entry_price"] <= last_price:
                    continue

                order_args = {
                    "order_dir": -1,
                    "qty": grid["entry_qty"],
                    "price": grid["entry_price"],
                }
            suffix = self._get_random_string(k=10)
            order_args["cid"] = f"{grid_id}-{suffix}"
            order_args_list.append(order_args)

        self.place_orders_batch(order_args_list)
        if len(order_args_list) > 0:
            open_orders = self.ccxt_exchange.fetch_open_orders(
                symbol=self.ccxt_symbol, limit=50
            )
            self._timestamp_markers["earliest_open_order"] = min(
                open_orders, key=lambda x: x["timestamp"]
            )["timestamp"]

    def sync_balance(self):
        result = self.ccxt_exchange.fetch_balance()
        self.balance = result["BTC"]["total"]

    def sync_position(self):
        res = self.ccxt_exchange.private_get_position_list({"symbol": self.pair})
        pos = {
            "dir": 0,
            "qty": 0.0,
            "avg_price": 0.0,
            "liq_price": 0.0,
            "unrealised_pnl": 0.0,
            "leverage": 0.0,
        }
        if res["result"]["side"] == "None":
            self.position.update(pos)
            return

        qty = res["result"]["size"]
        dir_mapping = {
            "buy": 1,
            "sell": -1,
        }
        pos_dir = dir_mapping[res["result"]["side"].lower()]
        avg_price = round(float(res["result"]["entry_price"]), 2)  # $
        liq_price = round(float(res["result"]["liq_price"]), 2)
        unrealised_pnl = res["result"]["unrealised_pnl"]
        leverage = res["result"]["effective_leverage"]
        self.position.update(
            {
                "dir": pos_dir,
                "qty": qty,
                "avg_price": avg_price,
                "liq_price": liq_price,
                "unrealised_pnl": unrealised_pnl,
                "leverage": leverage,
            }
        )

    def sync_grids(self):
        since = self._timestamp_markers["earliest_open_order"] - self._order_sync_window
        orders = self.ccxt_exchange.fetch_closed_orders(
            symbol=self.ccxt_symbol,
            since=since,
            limit=50,
            params={"order_status": "Filled"},
        )
        orders = sorted(orders, key=lambda x: x["timestamp"])
        for order in orders:
            if order["id"] in self._synced_order_set:
                continue

            cid: str = order["info"]["order_link_id"]
            if "-" not in cid:
                continue

            grid_id = int(cid.split("-", 1)[0])
            grid_index = self._grid_id_index_map.get(grid_id, -1)
            if grid_index < 0:
                continue

            grid = self.grids[grid_index]
            if order["side"] == "sell":
                grid["filled_qty"] = order["cost"]
                grid["holding"] = True

            if order["side"] == "buy":
                grid["filled_qty"] = 0
                grid["holding"] = False

            grid_state = "开" if grid["holding"] else "平"
            full_logger.info(
                "网格（%f@%d）状态已变更 -> %s", grid["entry_price"], grid_id, grid_state
            )
            self._synced_order_set.add(order["id"])

        self.client.update_grids(self.grids)

    def get_last_price(self):
        ticker = self.ccxt_exchange.fetch_ticker(symbol=self.ccxt_symbol)
        last_price = ticker["last"]
        return last_price

    def get_best_price(self):
        order_book = self.ccxt_exchange.fetch_l2_order_book(
            symbol=self.ccxt_symbol, limit=5
        )
        best_bid = order_book["bids"][0][0]
        best_ask = order_book["asks"][0][0]
        return best_ask, best_bid

    def pre_trade(self):
        if config.TEST_NET:
            self.enable_test_net()
        self.sync_config()
        self.auth()
        self.ccxt_exchange.load_markets()
        self.ccxt_exchange.cancel_all_orders(symbol=self.ccxt_symbol)
        self.sync_position()
        self.sync_balance()
        self.load_grids()

    def trade(self):
        full_logger.info("正在设置交易环境")
        self.pre_trade()
        cnt = 1
        while True:
            try:
                logger.info("开始第 %d 轮交易", cnt)
                self.sync_position()
                self.sync_balance()
                self.sync_grids()
                self.ensure_order()
                time.sleep(config.TRADE_INTERVAL)
                cnt += 1
            except Exception as e:
                logger.exception(e, exc_info=True)
                full_logger.exception(e)

    def auth(self):
        self.ccxt_exchange.apiKey = self._api_key
        self.ccxt_exchange.secret = self._secret

    @staticmethod
    def _get_random_string(k=10):
        letters = string.ascii_letters
        return "".join(random.choices(letters, k=k))

    @staticmethod
    def timestamp_millisecond(dt=None, delta=None):
        if not dt:
            dt = datetime.now()

        if delta is not None:
            dt = dt + delta

        return int(dt.timestamp() * 1000)


if __name__ == "__main__":
    bot = BybitGridBot(pair="BTCUSD")
    bot.trade()
