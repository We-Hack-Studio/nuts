import json
from datetime import datetime

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from core.utils import KeyHelper
from urllib.parse import parse_qs


class PrivateStreamConsumer(AsyncJsonWebsocketConsumer):
    async def receive_json(self, content, **kwargs):
        params = content.get("params")
        cmd = content.get("cmd")
        key = content.get("key")
        if not key:
            await self.close()

        data = KeyHelper.from_key(key=key)
        if not data:
            await self.close()

        group_name = data["channel_group_name"]
        if cmd == "sub":
            for group_name in params:
                await self.channel_layer.group_add(
                    group_name.lower(), self.channel_name
                )
                self.groups.append(group_name.lower())

        if cmd == "unsub":
            for group_name in params:
                await self.channel_layer.group_discard(
                    group_name.lower(), self.channel_name
                )
                self.groups.remove(group_name.lower())

    async def robot_stream(self, event):
        message = event["text"]
        await self.send_json(message)
