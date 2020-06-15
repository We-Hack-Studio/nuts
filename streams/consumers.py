import json
from datetime import datetime

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class StreamConsumer(AsyncJsonWebsocketConsumer):
    async def receive_json(self, content, **kwargs):
        params = content.get("params")
        cmd = content.get("cmd")

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
