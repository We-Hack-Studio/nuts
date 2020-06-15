import json

from channels.generic.http import AsyncHttpConsumer


class RobotLogConsumer(AsyncHttpConsumer):
    async def handle(self, body):
        body_str = body.decode("urf8")
        data = json.loads(body_str)
        event = {
            "type": "robot.stream",
            "text": data,
        }
        robot_id = data["robot_id"]
        group_name = f"robot.{robot_id}"
        # await self.channel_layer.group_send(
        #     group_name, event,
        # )
        await self.send_response(
            200, b"Your response bytes", headers=[(b"Content-Type", b"text/plain"),]
        )
