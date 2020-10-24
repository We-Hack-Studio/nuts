import asyncio
import re
from typing import List

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from django.utils.translation import gettext
from rest_framework_api_key.models import APIKey

User = get_user_model()

public_topic_patterns: List[str] = []
private_topic_patterns = [
    r"robot#\d+\.log",
    r"robot#\d+\.asset",
    r"robot#\d+\.order",
    r"robot#\d+\.strategyParameters",
]
topic_patterns = public_topic_patterns + private_topic_patterns


def _category_topics(topics):
    public = []
    private = []
    for topic in topics:
        if not any(re.match(pattern, topic) for pattern in topic_patterns):
            continue

        if any(re.match(pattern, topic) for pattern in public_topic_patterns):
            public.append(topic)
        elif any(re.match(pattern, topic) for pattern in private_topic_patterns):
            private.append(topic)

    return public, private


class StreamConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._topics = []
        self._event = asyncio.Event()
        self._authed = False

    async def connect(self):
        await super().connect()
        asyncio.get_event_loop().create_task(self.ensure_sub())

    async def receive_json(self, content, **kwargs):
        # todo: validate the content
        cmd = content["cmd"]
        if cmd == "auth":
            api_key = content["api_key"]
            await self.auth(api_key)
        elif cmd == "sub":
            topics = content["topics"]
            await self.sub(topics)
        elif cmd == "unsub":
            topics = content["topics"]
            await self.unsub(topics)
        elif cmd == "broadcast":
            message = content["message"]
            await self.broadcast(message)
        else:
            await self.send_json({"code": 405, "detail": f"不支持的指令 {cmd}"}, close=True)

    async def auth(self, api_key: str):
        # Already authenticated
        if self._authed:
            return

        if not api_key:
            await self.send_json(
                {"code": 400, "detail": gettext("No api key provided")}, close=True
            )

        async_is_valid = database_sync_to_async(APIKey.objects.is_valid)
        result = await async_is_valid(api_key)
        if result:
            self._authed = True
            await self.send_json({"code": 200, "detail": gettext("ok")})
        else:
            await self.send_json(
                {"code": 400, "detail": gettext("Invalid api key")},
                close=True,
            )

    async def sub(self, topics):
        public_topics, private_topics = _category_topics(topics)
        if len(private_topics) > 0 and not self._authed:
            await self.send_json(
                {
                    "code": 401,
                    "detail": gettext(
                        "Auth by api key is required when subscribe to private topics"
                    ),
                },
                close=True,
            )
            return

        for topic in public_topics + private_topics:
            group_name = topic.replace("#", "-")
            await self.channel_layer.group_add(group_name, self.channel_name)
            self.groups.append(group_name)
            self._topics.append(topic)

        if len(self._topics) > 0:
            self._event.set()

    async def unsub(self, topics):
        for topic in topics:
            group_name = topic.replace("#", "-")
            await self.channel_layer.group_discard(group_name, self.channel_name)
            self.groups.remove(group_name)
            self._topics.remove(topic)

    async def ensure_sub(self):
        try:
            await asyncio.wait_for(self._event.wait(), timeout=30)
        except asyncio.TimeoutError:
            await self.send_json({"code": 400, "detail": "1分钟内未订阅任何话题"}, close=True)

    async def broadcast(self, message):
        if not self._authed:
            await self.send_json({"code": 403, "detail": "认证后才可广播消息"}, close=True)
            return

        category = message["category"]
        if category == "robotPing":
            pass
        elif category == "robotLog":
            log_topic_groups = [g for g in self.groups if g.endswith("log")]
            for group in log_topic_groups:
                await self.channel_layer.group_send(
                    group, {"type": "robot.log", "message": message}
                )
        else:
            pass

    async def robot_log(self, event):
        message = event["message"]
        await self.send_json(message)
