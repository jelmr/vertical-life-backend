import tornado.web
from sqlalchemy.testing.plugin.plugin_base import ABC
from tornado_sqlalchemy import SessionMixin

from vertical_life_client import VerticalLifeClient


class BaseHandler(SessionMixin, tornado.web.RequestHandler, ABC):
    def initialize(self, vl_client: VerticalLifeClient):
        self.vl_client = vl_client

    def prepare(self):
        self.set_header("Content-Type", "application/json")
