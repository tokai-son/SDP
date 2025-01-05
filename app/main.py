import os
import logging
import asyncio
import tornado
import aioredis
from controller.room import RoomHandler
from controller.connect import ConnectHandler

def make_app(redis):
    return tornado.web.Application(
        [
            (r"/room", RoomHandler, dict(redis=redis)),
            (r"/connect", ConnectHandler, dict(redis=redis)),
        ],
        None,
        None,
        debug=True,
        autoreload=True,
    )

async def main():
    # ロギングの設定
    logging.basicConfig(level=logging.INFO)

    # Redisの接続
    redisHost = os.getenv("REDIS_HOST")
    redisPort = os.getenv("REDIS_PORT")
    if redisHost is None or redisPort is None:
        logging.error("REDIS_HOST and REDIS_PORT must be set")
        return
    redis = await aioredis.from_url(f"redis://{redisHost}:{redisPort}")
    if redis is None:
        logging.error("failed to connect to redis")
        return

    logging.info("starting server")
    app = make_app(redis=redis)
    app.listen(9999)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
