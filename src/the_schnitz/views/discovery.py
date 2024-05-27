from flask import Blueprint
from werkzeug.exceptions import NotFound

from the_schnitz.app import location_schema, location_service


bp = Blueprint('discovery', __name__, url_prefix='/')


@bp.route('/<uuid:location_id>')
def discovery(location_id):
    location = location_service.find_location(location_id)

    if not location:
        raise NotFound(description="You shall not guess!!!")

    location_service.mark_as_found(location)

    return location_schema.dump(location)
