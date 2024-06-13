from marshmallow import Schema, fields, post_load

from the_schnitz.location import Location, LocationStatus


class LocationSchema(Schema):
    id = fields.UUID(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    challenge = fields.Str()
    status = fields.Enum(enum=LocationStatus,
                         by_value=True,
                         load_default=LocationStatus.HIDDEN)

    @post_load
    def make_location(self, data, **kwargs):
        return Location(**data)


class LocationEventSchema(Schema):
    type = fields.Method('get_type')
    location = fields.Nested(LocationSchema(only=('id', 'name')))

    def get_type(self, obj):
        return obj.__class__.__name__
