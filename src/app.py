#!tornado/bin/python
import argparse

import tornado.ioloop
import tornado.web

from db import get_db
from handlers.time_slots_handler import TimeSlotsHandler
from scraper import Scraper
from vertical_life_client import VerticalLifeClient


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", help="port to listen to", default=8888)
    parser.add_argument("--scrape", help="whether to scrape TimeSlots from VerticalLife", action='store_true')
    parser.add_argument("--debug", help="whether run in debug mode", action='store_true')
    return parser.parse_args()


def make_app(db, debug):
    return tornado.web.Application(
        [
            (r"/([^/]+)", TimeSlotsHandler),
        ],
        autoReload=debug,
        debug=debug,
        db=db
    )


if __name__ == "__main__":
    args = parse_args()

    db = get_db()
    db.Model.metadata.create_all(db.engine)

    if args.scrape:
        scraper = Scraper(db)

    app = make_app(db, args.debug)
    print(f'Listening on port {args.port}' + (' in debug mode' if args.debug else ''))
    app.listen(args.port)

    tornado.ioloop.IOLoop.current().start()
