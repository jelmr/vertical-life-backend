from typing import List

from models.area import Area, AreaName


class Gym:
    def __init__(self, data):
        self.data = data

    def areas(self) -> List[Area]:
        return [
            Area(**{
                key: area[key]
                for key
                in ['id', 'name', 'capacity']
            })
            for area
            in self.data['slot_areas']
        ]

    def area(self, name: AreaName):
        return next(area for area in self.areas() if area.name == name.value)
