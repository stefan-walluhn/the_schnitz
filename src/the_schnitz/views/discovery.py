from flask import Blueprint, abort, current_app

from the_schnitz.app import (get_config_repository,
                             get_redis_repository,
                             get_location_schema,
                             get_rabbitmq_producer)
from the_schnitz.location import LocationStatus


bp = Blueprint('discovery', __name__, url_prefix='/')


@bp.route('/<uuid:location_id>')
def discovery(location_id):
    schema = get_location_schema()
    config_repository = get_config_repository()
    redis_repository = get_redis_repository()
    producer = get_rabbitmq_producer()

    location = (redis_repository.find_location(location_id) or
                config_repository.find_location(location_id))

    if not location:
        abort(404, description="You shell not guess!!!")

    if location.status == LocationStatus.HIDDEN:
        location.status = LocationStatus.FOUND
        producer.publish(schema.dump(location))

    redis_repository.upsert_location(location)

    return schema.dump(location)
