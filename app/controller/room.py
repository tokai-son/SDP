import json
import logging
import tornado
import aioredis
from view.room.post import view_request, view_response
from pkg.generate_room_id import generate_random_id

class RoomHandler(tornado.web.RequestHandler):
    def initialize(self, redis: aioredis.Redis):
        self.redis = redis

    async def post(self):
        logging.info("POST /room started")

        # View Request
        try:
            req_json = json.loads(self.request.body)
            req = view_request(req_json)
        except json.JSONDecodeError:
            logging.error("invalid json")
            self.set_status(400)
            self.write({"error": "invalid json"})
            return
        except ValueError as e:
            logging.error(str(e))
            self.set_status(400)
            self.write({"error": str(e)})
            return
        except Exception as e:
            logging.error(str(e))
            self.set_status(500)
            self.write({"error": "internal server error"})
            return

        # Generate a random roomID
        roomID = generate_random_id()

        # Store the value in Redis
        value = json.dumps(req)
        try:
            key = await self.redis.set(roomID, value, ex=300, nx=True)
            # Check duplication of roomID
            if not key:
                logging.error("roomID already exists")
                self.set_status(500)
                self.write({"error": "internal server error"})
                return
        except Exception as e:
            logging.error(str(e))
            self.set_status(500)
            self.write({"error": "internal server error"})
            return
        logging.info(f"stored {roomID} in redis")

        # View response
        try:
            res = view_response({"roomID": roomID})
        except ValueError as e:
            logging.error(str(e))
            self.set_status(500)
            self.write({"error": "internal server error"})
            return
        except Exception as e:
            logging.error(str(e))
            self.set_status(500)
            self.write({"error": "internal server error"})
            return

        self.write(res)
