from flask import Blueprint, abort

from the_schnitz.app import (config_repository,
                             redis_repository,
                             location_schema,
                             rabbitmq_producer)
from the_schnitz.location import LocationStatus


bp = Blueprint('discovery', __name__, url_prefix='/')


@bp.route('/<uuid:location_id>')
def discovery(location_id):
    location = (redis_repository.find_location(location_id) or
                config_repository.find_location(location_id))

    if not location:
        abort(404, description="You shell not guess!!!")

    if location.status == LocationStatus.HIDDEN:
        location.status = LocationStatus.FOUND
        rabbitmq_producer.publish(location_schema.dump(location))

    redis_repository.upsert_location(location)

    return location_schema.dump(location)
