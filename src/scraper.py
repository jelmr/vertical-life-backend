import asyncio
import random
import threading
import time
from datetime import datetime, timedelta

from sqlalchemy.orm import sessionmaker

from models.area import AreaName
from vertical_life_client import VerticalLifeClient

LOOKAHEAD = 14


class Scraper(object):
    def __init__(self, db):
        self.vl_client = VerticalLifeClient()
        self.db = db
        thread = threading.Thread(target=self.run, args=())
        thread.start()

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.scrape())
        loop.close()

    async def scrape(self):
        while True:
            print('Scraper sleeping')
            time.sleep(60 * 60)

            print('Scraper scraping!')
            session = sessionmaker(bind=self.db.engine)()

            for area in AreaName:
                for days in range(LOOKAHEAD):
                    date = datetime.today() + timedelta(days=days)
                    print("Getting ", area.value, date.strftime('%Y/%m/%d'))
                    timeslots = await self.vl_client.get_time_slots(area, date)
                    session.add_all(timeslots)
                    time.sleep(random.randint(5, 10))

            session.commit()
            session.flush()
