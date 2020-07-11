from urllib.parse import parse_qs

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from core.utils import KeyHelper


class RobotStreamConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        query_string = parse_qs(self.scope["query_string"].decode("utf8"))
        key = query_string.get("stream_key")
        if not key:
            await self.close()
            return

        data = KeyHelper.from_key(key=key[0])
        if not data:
            await self.close()
            return

        robot_id = self.scope["url_route"]["kwargs"]["pk"]
        if int(robot_id) != data["robot_id"]:
            await self.close()
            return

        group = f"robot.{robot_id}"
        self.group_name = group
        await self.channel_layer.group_add(group, self.channel_name)
        self.groups.append(group)
        await super().connect()

    async def receive_json(self, content, **kwargs):
        await self.channel_layer.group_send(
            self.group_name, {"type": "robot_stream", "text": content}
        )

    async def robot_stream(self, event):
        message = event["text"]
        await self.send_json(message)
