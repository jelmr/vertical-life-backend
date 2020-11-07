from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Enum
from tornado_sqlalchemy import SQLAlchemy

from models.area import AreaName

db = SQLAlchemy('sqlite:///app.db', engine_options={'echo': False})

class TimeSlot(db.Model):
    __tablename__ = 'time_slots'
    id = Column(Integer, primary_key=True)
    area = Column(Enum(AreaName))
    check_in_at = Column(DateTime)
    free_spots = Column(Integer)
    capacity = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<date={self.check_in_at} slots=[{self.free_spots}/{self.capacity}]>'

db.Model.metadata.create_all(db.engine)

def get_db() -> SQLAlchemy:
    return db
