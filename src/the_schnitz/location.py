import uuid

from dataclasses import dataclass
from enum import StrEnum, auto


class LocationStatus(StrEnum):
    HIDDEN = auto()
    FOUND = auto()


@dataclass
class Location:
    id: uuid.UUID
    name: str
    description: str
    status: LocationStatus
