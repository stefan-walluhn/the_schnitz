import uuid

from dataclasses import dataclass
from enum import Enum


class LocationStatus(Enum):
    HIDDEN = 'hidden'
    FOUND = 'found'


@dataclass
class Location:
    id: uuid.UUID
    name: str
    description: str
    status: LocationStatus
    challenge: str = ''
