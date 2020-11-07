#!tornado/bin/python
import argparse
import json

import tornado.ioloop
import tornado.web
from sqlalchemy import func, and_

from alchemy_encoder import AlchemyEncoder
from db import get_db, TimeSlot
from handlers.base_handler import BaseHandler
from models.area import AreaName
from scraper import Scraper
from vertical_life_client import VerticalLifeClient


class GymInfoHandler(BaseHandler):
    async def get(self):
        gym = await self.vl_client.get_gym()
        self.write(gym.data)


class TimeSlotsHandler(BaseHandler):
    async def get(self, area_name_raw):
        area_name = AreaName[area_name_raw]
        with self.make_session() as session:
            most_recent_time_slots = (
                session
                    .query(TimeSlot.id, func.max(TimeSlot.created_at).label("max_created_at"))
                    .filter(TimeSlot.area == area_name)
                    .group_by(TimeSlot.area, TimeSlot.check_in_at)
                    .subquery()
            )

            time_slots = (
                session.query(TimeSlot)
                    .join(most_recent_time_slots,
                          and_(TimeSlot.id == most_recent_time_slots.c.id,
                               TimeSlot.created_at == most_recent_time_slots.c.max_created_at))
            )

            self.write(json.dumps(time_slots.all(), cls=AlchemyEncoder))


def make_app():
    params = dict(vl_client=(VerticalLifeClient()))
    return tornado.web.Application(
        [
            (r"/", GymInfoHandler, params),
            (r"/([^/]+)", TimeSlotsHandler, params),
        ],
        autoReload=True,
        debug=True,
        db=get_db()
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", help="port to listen to", default=8888)
    parser.add_argument("--scrape", help="whether to scrape TimeSlots from VerticalLife", type=bool)
    args = parser.parse_args()

    if args.scrape:
        scraper = Scraper()

    app = make_app()
    port = args.port
    print(f'Listening on port {port}')
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
