from marshmallow import Schema, fields, post_load

from the_schnitz.location import Location, LocationStatus


class LocationSchema(Schema):
    id = fields.UUID()
    name = fields.Str()
    status = fields.Enum(enum=LocationStatus,
                         by_value=True,
                         load_default=LocationStatus.HIDDEN)

    @post_load
    def make_location(self, data, **kwargs):
        return Location(**data)
