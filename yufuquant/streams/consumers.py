import asyncio
import re
from typing import List

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework_api_key.models import APIKey

User = get_user_model()

public_topic_patterns: List[str] = []
private_topic_patterns = [
    r"robot#\d+\.ping",
    r"robot#\d+\.log",
    r"robot#\d+\.assetRecord",
    r"robot#\d+\.store",
    r"robot#\d+\.strategyParameters",
]
topic_patterns = public_topic_patterns + private_topic_patterns


def category_topics(topics: List[str]):
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


SUPPORTED_CMD = {"auth", "sub", "unsub", "broadcast"}


class _StreamContentSerializer(serializers.Serializer):
    cmd = serializers.CharField()


class AuthContentSerializer(_StreamContentSerializer):
    auth_token = serializers.CharField(required=False, allow_blank=True)
    api_key = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        validated_data = super(AuthContentSerializer, self).validate(attrs)

        auth_token = validated_data.get("auth_token", "")
        api_key = validated_data.get("api_key", "")
        if api_key == "" and auth_token == "":
            raise ValidationError("Missing auth_token or api_key.")
        return validated_data


class TopicContentSerializer(_StreamContentSerializer):
    topics = serializers.ListSerializer(
        child=serializers.CharField(), allow_empty=False
    )


class _BroadcastMessageSerializer(serializers.Serializer):
    category = serializers.CharField()
    data = serializers.DictField(allow_empty=False)  # type: ignore


class BroadcastContentSerializer(_StreamContentSerializer):
    message = _BroadcastMessageSerializer()


class StreamConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._topics = []
        self._ensure_sub_event = asyncio.Event()
        self._ensure_heartbeat_event = asyncio.Event()
        self._heartbeat_timestamp = 0
        self._authed = False

    async def connect(self):
        await super().connect()
        asyncio.get_event_loop().create_task(self.ensure_sub())
        asyncio.get_event_loop().create_task(self.heartbeat_task())

    async def receive_json(self, content, **kwargs):
        if "pong" in content:
            heartbeat_timestamp = content["pong"]
            if heartbeat_timestamp is None:
                return
            await self.handle_pong(heartbeat_timestamp)
            return

        if "cmd" not in content:
            await self.send_json(
                {
                    "code": 400,
                    "detail": _("Invalid stream content."),
                },
            )
            return

        # todo: validate the content
        cmd = content["cmd"]
        if cmd not in SUPPORTED_CMD:
            await self.send_json(
                {
                    "code": 405,
                    "detail": _("Unsupported cmd: {cmd}.".format(cmd=cmd)),
                },
            )
            return

        if cmd == "auth":
            serializer = AuthContentSerializer(data=content)
            if not serializer.is_valid(raise_exception=False):
                await self.send_json({"code": 400, "detail": _("Invalid auth stream.")})
                return

            if "api_key" in serializer.validated_data:
                api_key = serializer.validated_data["api_key"]
                await self.auth_by_api_key(api_key)
            else:
                auth_token = serializer.validated_data["auth_token"]
                await self.auth_by_auth_token(auth_token)

        elif cmd == "sub":
            serializer = TopicContentSerializer(data=content)  # type: ignore
            if not serializer.is_valid(raise_exception=False):
                await self.send_json({"code": 400, "detail": _("Invalid sub stream.")})
                return

            topics = serializer.validated_data["topics"]
            await self.sub(topics)

        elif cmd == "unsub":
            serializer = TopicContentSerializer(data=content)  # type: ignore
            if not serializer.is_valid(raise_exception=False):
                await self.send_json(
                    {"code": 400, "detail": _("Invalid unsub stream.")}
                )
                return

            topics = serializer.validated_data["topics"]
            await self.unsub(topics)

        elif cmd == "broadcast":
            serializer = BroadcastContentSerializer(data=content)  # type: ignore
            if not serializer.is_valid(raise_exception=False):
                await self.send_json(
                    {"code": 400, "detail": _("Invalid broadcast stream.")}
                )
                return
            message = serializer.validated_data["message"]
            await self.broadcast(message)

    async def auth_by_api_key(self, api_key: str):
        # Already authenticated
        if self._authed:
            return

        if not api_key:
            await self.send_json(
                {"code": 400, "detail": _("No api key provided")}, close=True
            )

        async_is_valid = database_sync_to_async(APIKey.objects.is_valid)
        result = await async_is_valid(api_key)
        if result:
            await self.send_json({"code": 200, "detail": _("ok")})
            self._authed = True
        else:
            await self.send_json(
                {"code": 400, "detail": _("Invalid api key")},
                close=True,
            )

    async def auth_by_auth_token(self, auth_token: str):
        """Authenticate by auth token."""
        # Already authenticated
        if self._authed:
            return

        async_token_get = database_sync_to_async(Token.objects.get)

        try:
            await async_token_get(key=auth_token)
        except Token.DoesNotExist:
            await self.send_json({"code": 401, "detail": _("Invalid auth token.")})
            return

        await self.send_json({"code": 200, "detail": _("Authenticated.")})
        self._authed = True

    async def sub(self, topics):
        public_topics, private_topics = category_topics(topics)
        if len(private_topics) > 0 and not self._authed:
            await self.send_json(
                {
                    "code": 401,
                    "detail": _(
                        "Authentication required for subscribing private topics."
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
            self._ensure_sub_event.set()

    async def unsub(self, topics):
        for topic in topics:
            group_name = topic.replace("#", "-")
            await self.channel_layer.group_discard(group_name, self.channel_name)
            self.groups.remove(group_name)
            self._topics.remove(topic)

    async def ensure_sub(self):
        timeout = 60
        try:
            await asyncio.wait_for(self._ensure_sub_event.wait(), timeout=timeout)
        except asyncio.TimeoutError:
            await self.send_json(
                {
                    "code": 400,
                    "detail": _(
                        "No subscription within {timeout} seconds.".format(
                            timeout=timeout
                        )
                    ),
                },
                close=True,
            )

    async def broadcast(self, message):
        if not self._authed:
            await self.send_json(
                {
                    "code": 403,
                    "detail": _("Authentication required for broadcasting message."),
                },
                close=True,
            )
            return

        category = message["category"]
        if category == "robotPing":
            ping_topic_groups = [g for g in self.groups if g.endswith("ping")]
            for group in ping_topic_groups:
                await self.channel_layer.group_send(
                    group, {"type": "robot.ping", "message": message}
                )
        elif category == "robotLog":
            log_topic_groups = [g for g in self.groups if g.endswith("log")]
            for group in log_topic_groups:
                await self.channel_layer.group_send(
                    group, {"type": "robot.log", "message": message}
                )
        elif category in {
            "robotPositionStore",
            "robotOrderStore",
            "robotStrategyStore",
        }:
            store_topic_groups = [g for g in self.groups if g.endswith("store")]
            for group in store_topic_groups:
                await self.channel_layer.group_send(
                    group, {"type": "robot.store", "message": message}
                )
        else:
            pass

    async def handle_pong(self, heartbeat_timestamp: int):
        # outdated pong
        if heartbeat_timestamp < self._heartbeat_timestamp:
            return

        if heartbeat_timestamp == self._heartbeat_timestamp:
            self._ensure_heartbeat_event.set()

    async def robot_log(self, event):
        message = event["message"]
        await self.send_json(message)

    async def robot_ping(self, event):
        message = event["message"]
        await self.send_json(message)

    async def robot_store(self, event):
        message = event["message"]
        await self.send_json(message)

    async def heartbeat_task(self):
        while True:
            await asyncio.sleep(30)
            self._heartbeat_timestamp = int(timezone.now().timestamp() * 1000)
            await self.send_json({"ping": self._heartbeat_timestamp})
            asyncio.get_event_loop().create_task(self.ensure_heartbeat())
            self._ensure_heartbeat_event.clear()

    async def ensure_heartbeat(self):
        """Disconnect if no pong received within 30 seconds."""
        try:
            await asyncio.wait_for(self._ensure_heartbeat_event.wait(), timeout=30)
        except asyncio.TimeoutError:
            await self.send_json(
                {"code": 400, "detail": _("Heartbeat timeout.")},
                close=True,
            )
