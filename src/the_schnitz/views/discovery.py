from flask import Blueprint, abort, current_app

from the_schnitz import get_redis_repository, get_location_schema
from the_schnitz.rabbitmq import get_rabbitmq_producer
from the_schnitz.location import LocationStatus


bp = Blueprint('discovery', __name__, url_prefix='/')


@bp.route('/<uuid:location_id>')
def discovery(location_id):
    if location_id not in current_app.config['LOCATIONS']:
        abort(404, description="You shell not guess!!!")

    schema = get_location_schema()
    repository = get_redis_repository()
    producer = get_rabbitmq_producer()

    location = repository.find_location(location_id)

    if not location:
        location = schema.load({
            'id': location_id,
            'status': LocationStatus.FOUND
        } | current_app.config['LOCATIONS'][location_id])

        producer.publish(schema.dump(location))
        repository.upsert_location(location)

    return schema.dump(location)
