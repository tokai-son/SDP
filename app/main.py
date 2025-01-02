import logging
import asyncio
import tornado

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello world")

def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
        ],
        None,
        None,
        debug=True,
        autoreload=True,
    )

async def main():
    # ロギングの設定
    logging.basicConfig(level=logging.INFO)

    logging.info("starting server")
    app = make_app()
    app.listen(9999)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
