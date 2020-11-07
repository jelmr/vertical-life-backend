import json
from datetime import datetime

from sqlalchemy.ext.declarative import DeclarativeMeta

from models.area import AreaName


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)

                if type(data) == datetime:
                    fields[field] = str(data) + "+00:00"
                elif type(data) == AreaName:
                    fields[field] = data.name
                else:
                    try:
                        json.dumps(data)
                        fields[field] = data
                    except TypeError:
                        fields[field] = None
            return fields
        return json.JSONEncoder.default(self, obj)
