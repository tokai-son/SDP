import json
import logging
import tornado.web
import tornado.websocket
import aioredis
from view.ws.message import Message, MessageType, MessageFromType, unmarshal_message

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

        # if there is an offer, send it to the client
        offer = await self.redis.get(f"{self.room_id}:offer")
        if offer:
            self.send_message_to_room(self.room_id, offer)

    def open(self):
        tornado.ioloop.IOLoop.current().add_callback(self.async_open)

    async def on_message(self, message:Message):
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
            logging.info(f"Received offer: {message}")
            description = json.dumps(message.description)
            await self.redis.set(f"{self.room_id}:offer", description)
        if message.type == MessageType.ANSWER:
            logging.info(f"Received answer: {message}")
            await self.redis.set(f"{self.room_id}:answer", json.dumps(message.description))
            self.send_message_to_room(self.room_id, message.description)
        if message.type == MessageType.CANDIDATE:
            if (message.sendFrom == MessageFromType.HOST):
                logging.info(f"Received candidate from HOST: {message}")
                await self.redis.lpush(f"{self.room_id}:hostCandidates", message.marshal())
            if (message.sendFrom == MessageFromType.CLIENT):
                logging.info(f"Received candidate from CLIENT: {message}")
                self.send_message_to_room(self.room_id, message.self_unmarshal())
        if message.type == MessageType.JOIN:
            logging.info(f"Received join: {message}")
            candidates = await self.redis.lrange(f"{self.room_id}:hostCandidates", 0, -1)
            for candidate in candidates:
                self.send_message_to_room(self.room_id, candidate)

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
