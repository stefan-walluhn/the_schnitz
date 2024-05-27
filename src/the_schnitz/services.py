from the_schnitz.events import LocationFoundEvent, LocationReFoundEvent
from the_schnitz.schema import LocationEventSchema
from the_schnitz.location import LocationStatus


class LocationService:
    def __init__(self, config_repository, repository, producer):
        self.config_repository = config_repository
        self.repository = repository
        self.producer = producer
        self.location_event_schema = LocationEventSchema()

    def find_location(self, id):
        return (self.repository.find_location(id) or
                self.config_repository.find_location(id))

    def mark_as_found(self, location):
        event = None

        if location.status == LocationStatus.HIDDEN:
            location.status = LocationStatus.FOUND
            event = LocationFoundEvent(location=location)
        else:
            event = LocationReFoundEvent(location=location)

        assert event is not None

        self.producer.publish(self.location_event_schema.dump(event))
        self.repository.upsert_location(location)
