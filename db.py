from datetime import datetime

from sqlalchemy import Column, BigInteger, DateTime, Integer, Sequence, Enum
from tornado_sqlalchemy import SQLAlchemy, SessionMixin

from models.area import AreaName

db = SQLAlchemy('sqlite:///app.db', engine_options={'echo': False})

class TimeSlot(db.Model):
    __tablename__ = 'time_slots'
    id = Column(Integer, primary_key=True)
    area = Column(Enum(AreaName))
    check_in_at = Column(DateTime)
    free_spots = Column(Integer)
    bookings_count = Column(Integer)
    spots_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<date={self.check_in_at.date()} slots=[{self.spots_count}/{self.free_spots}]>'

db.Model.metadata.create_all(db.engine)

def get_db() -> SQLAlchemy:
    return db
