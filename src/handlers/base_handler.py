import tornado.web
from sqlalchemy.testing.plugin.plugin_base import ABC
from tornado_sqlalchemy import SessionMixin


class BaseHandler(SessionMixin, tornado.web.RequestHandler, ABC):
    def set_default_headers(self) -> None:
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header("Content-Type", "application/json")
