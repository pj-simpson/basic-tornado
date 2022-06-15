import datetime
import requests

import tornado.ioloop
import tornado.options
import tornado.web
import json
from tornado.httpclient import AsyncHTTPClient

from tornado.options import define, options

define("port", default=8000, type=int)


# Is there any noticeable difference between using the requests package and Tornados own AsyncHttpClient?


class AsyncAnythingHandler(tornado.web.RequestHandler):
    async def get(self):
        http_client = AsyncHTTPClient()
        response = await http_client.fetch("https://httpbin.org/anything")
        http_client.close()
        response_dict = json.loads(response.body.decode("utf-8"))
        self.write(response_dict)


class RequestsAnythingHandler(tornado.web.RequestHandler):
    async def get(self):
        response = requests.get("https://httpbin.org/anything")
        response_dict = response.json()
        self.write(response_dict)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/async", AsyncAnythingHandler),
            (r"/requests", RequestsAnythingHandler),
        ]
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
