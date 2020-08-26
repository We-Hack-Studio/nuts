import asyncio
import re

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from users.models import User

public_topic_patterns = []
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

    async def connect(self):
        await super().connect()
        asyncio.get_event_loop().create_task(self.ensure_sub())

    async def receive_json(self, content, **kwargs):
        # todo: validate the content
        cmd = content["cmd"]
        if cmd == "auth":
            token = content["params"]
            await self.auth(token)
        elif cmd == "sub":
            topics = content["params"]
            await self.sub(topics)
        elif cmd == "unsub":
            topics = content["params"]
            await self.unsub(topics)
        else:
            await self.send_json({"code": 405, "detail": f"不支持的指令 {cmd}"}, close=True)

    async def auth(self, token: str):
        # Already authenticated
        if self.scope.get("user"):
            return

        async_user_get = database_sync_to_async(User.objects.get)
        try:
            user = await async_user_get(auth_token__key=token)
            self.scope["user"] = user
            await self.send_json({"code": 200, "detail": "认证成功"})
        except User.DoesNotExist:
            await self.send_json({"code": 400, "detail": "认证失败"}, close=True)

    async def sub(self, topics):
        public_topics, private_topics = _category_topics(topics)
        if len(private_topics) > 0 and not self.scope.get("user"):
            await self.send_json({"code": 401, "detail": "包含认证后才可订阅的话题"}, close=True)
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

    async def robot_stream(self, event):
        message = event["text"]
        await self.send_json(message)
