import datetime
import requests

import tornado.ioloop
import tornado.options
import tornado.web
import json
from tornado.httpclient import AsyncHTTPClient

from tornado.options import define, options

define("port", default=8000, type=int)


class DomainsHandler(tornado.web.RequestHandler):
    async def get(self, word):
        http_client = AsyncHTTPClient()
        response = await http_client.fetch(
            f"https://api.domainsdb.info/v1/domains/search?page=1&limit=10&domain={word}",
            # connect_timeout=20.0,
            # request_timeout=20.0,
        )
        http_client.close()
        response_dict = json.loads(response.body.decode("utf-8"))
        await self.render("domains.html", search_word=word, **response_dict)


class DomainModule(tornado.web.UIModule):
    def render(self, dom):
        name = dom["domain"]
        created = datetime.datetime.fromisoformat(dom["create_date"])
        updated = datetime.datetime.fromisoformat(dom["update_date"])
        return self.render_string(
            "modules/domain.html", name=name, created=created, updated=updated
        )

    def css_files(self):
        return "domain-detail.css"


class SubHeadingModule(tornado.web.UIModule):
    def render(self, word):
        self.word = word

    def embedded_javascript(self):
        return f'window.alert("The word searched was: " + "{self.word}");'


if __name__ == "__main__":
    tornado.options.parse_command_line()
    settings = {
        "template_path": "templates",
        "static_path": "static",
        "ui_modules": {"Domain": DomainModule, "SubHeading": SubHeadingModule},
    }
    app = tornado.web.Application(
        handlers=[
            (r"/domains/(\w+)", DomainsHandler),
        ],
        **settings,
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
