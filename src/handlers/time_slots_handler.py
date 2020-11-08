import json
from datetime import datetime

from sqlalchemy import func, and_

from alchemy_encoder import AlchemyEncoder
from handlers.base_handler import BaseHandler
from models.area import AreaName
from models.time_slot import TimeSlot


class TimeSlotsHandler(BaseHandler):
    async def get(self, area_name_raw):
        now = datetime.utcnow()
        area_name = AreaName[area_name_raw]
        with self.make_session() as session:
            most_recent_time_slots = (
                session
                    .query(TimeSlot.id, func.max(TimeSlot.created_at).label("max_created_at"))
                    .filter(TimeSlot.area == area_name)
                    .filter(TimeSlot.check_in_at > now)
                    .group_by(TimeSlot.area, TimeSlot.check_in_at)
                    .subquery()
            )

            time_slots = (
                session.query(TimeSlot)
                    .join(most_recent_time_slots,
                          and_(TimeSlot.id == most_recent_time_slots.c.id,
                               TimeSlot.created_at == most_recent_time_slots.c.max_created_at))
            ).all()

            self.write(json.dumps(time_slots, cls=AlchemyEncoder))

