from flask import Blueprint, abort, current_app

from the_schnitz.rabbitmq import get_rabbitmq_producer


bp = Blueprint('discovery', __name__, url_prefix='/')


@bp.route('/<uuid:location_id>')
def discovery(location_id):
    if location_id not in current_app.config['LOCATIONS']:
        abort(404, description="You shell not guess!!!")

    data = {'discovery': {'location': str(location_id)}}  # XXX serializer
    producer = get_rabbitmq_producer()
    producer.publish(data)

    return "<p>Hello, World!</p>"
