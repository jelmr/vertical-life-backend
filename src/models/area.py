from dataclasses import dataclass
from enum import Enum


class AreaName(Enum):
    sport = "Klimhal"
    boulder = "Boulder"
    outside = "Buiten klimmen"


@dataclass
class Area:
    id: int
    name: AreaName
    capacity: int
