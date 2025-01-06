import logging
import tornado.web
import tornado.websocket
import aioredis

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

        logging.info(f"Connected to room: {self.room_id}")

    def open(self):
        tornado.ioloop.IOLoop.current().add_callback(self.async_open)

    def on_message(self, message):
        if not self.room_id:
            return
        message = message.replace('\n', '')
        logging.info(f"Received: {self.room_id} message: {message}")

    def on_close(self):
        logging.info(f"Disconnected from room: {self.room_id}")
