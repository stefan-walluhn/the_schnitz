from dataclasses import dataclass

from the_schnitz.location import Location


@dataclass
class LocationEvent:
    location: Location


class LocationFoundEvent(LocationEvent):
    pass


class LocationReFoundEvent(LocationEvent):
    pass
