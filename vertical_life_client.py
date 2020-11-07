import json
from typing import List

from dateutil import parser as date_parser
from datetime import datetime

from cachetools import TTLCache
from tornado.httpclient import AsyncHTTPClient

from db import TimeSlot
from models.area import AreaName, Area
from models.gym import Gym

API_BASE = 'https://smcb.vertical-life.info/api/v1/gyms/74/checkins/'


class VerticalLifeClient:
    def __init__(self):
        self.cache = TTLCache(1024, 12 * 60 * 60)
        self.client = AsyncHTTPClient()

    async def get_gym(self) -> Gym:
        try:
            self.cache['gym'] = self.cache.pop('gym')
        except:
            self.cache['gym'] = await self.client.fetch(API_BASE + 'public')
            print("[Gym] Cache miss")
        return Gym(json.loads(self.cache['gym'].body))

    async def get_area(self, area_name: AreaName) -> Area:
        gym = await self.get_gym()
        return gym.area(area_name)

    async def get_time_slots(self, area_name: AreaName, date: datetime) -> List[TimeSlot]:
        area = await self.get_area(area_name)
        date_str = date.strftime('%Y/%m/%d')

        res = await self.client.fetch(API_BASE + f'public-slots/at/{area.id}/date/{date_str}')
        data = json.loads(res.body)

        return [
            TimeSlot(
                area=area_name,
                check_in_at=date_parser.parse(slot['slot']['check_in_at']),
                free_spots=slot['free_spots'],
                capacity=area.capacity
            )
            for slot
            in data['slots']
        ]
