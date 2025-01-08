import json
import logging
import tornado.web
import tornado.websocket
import aioredis
from view.ws.message import MessageType, unmarshal_message

connections = {}

class ConnectHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, redis: aioredis.Redis):
        self.redis = redis
        self.room_id = None

    def check_origin(self, origin: str) -> bool:
        allowed_origins = ["http://localhost:3000"]
        return origin in allowed_origins

    async def async_open(self):
        # roomID from query parameter
        self.room_id = self.get_argument("roomID", None)
        if not self.room_id:
            self.write_message("roomIDが必要です")
            self.close()
            return

        # check if the roomID exists
        value = await self.redis.get(self.room_id)
        if not value:
            self.room_id = None
            self.write_message("配信が存在しません")
            self.close()
            return

        if self.room_id not in connections:
            connections[self.room_id] = set()
        connections[self.room_id].add(self)

        logging.info(f"Connected to room: {self.room_id}")

    def open(self):
        tornado.ioloop.IOLoop.current().add_callback(self.async_open)

    async def on_message(self, message):
        if not self.room_id:
            return

        message = message.replace('\n', '')
        try:
            message = unmarshal_message(message)
        except ValueError:
            return

        if self.room_id != message.roomID:
            return

        # processes in any condition are the same but it should be changed if necessary.
        if message.type == MessageType.OFFER:
            description = json.dumps(message.description)
            await self.redis.set(f"{self.room_id}:offer", description)
            self.send_message_to_room(self.room_id, "your offer has been received :>")
        if message.type == MessageType.ANSWER:
            self.send_message_to_room(self.room_id, "your answer has been received :>")
        if message.type == MessageType.CANDIDATE:
            self.send_message_to_room(self.room_id, "your candidate has been received :>")


    def on_close(self):
        if self.room_id and self in connections.get(self.room_id, set()):
            connections[self.room_id].remove(self)
            if not connections[self.room_id]:
                del connections[self.room_id]
        logging.info(f"Disconnected from room: {self.room_id}")

    @classmethod
    def send_message_to_room(cls, room_id, message):
        if room_id in connections:
            for connection in connections[room_id]:
                connection.write_message(message)
