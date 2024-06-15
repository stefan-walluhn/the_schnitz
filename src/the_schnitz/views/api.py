import uuid

from flask import Blueprint, request, session
from werkzeug.exceptions import NotFound, Unauthorized

from the_schnitz.app import (authorization_service,
                             location_schema,
                             location_service)
from the_schnitz.decorators import login_required
from the_schnitz.location import Location, LocationStatus


bp = Blueprint('api', __name__, url_prefix='/api')


@bp.post('/login')
def login():
    password = request.json.get('password', None)

    if not authorization_service.is_authorized(password):
        raise Unauthorized()

    session['i_am_allowed_to_play'] = True
    return {'login': 'success'}


@bp.get('/logout')
def logout():
    session.pop('i_am_allowed_to_play', None)
    return {'logout': 'success'}


@bp.route('/discover/<uuid:location_id>', methods=('GET', 'POST'))
@login_required
def location(location_id):
    location = location_service.find_location(location_id)

    if not location:
        raise NotFound(description="You shall not guess!!!")

    if request.method == 'POST':
        location_service.mark_as_found(location)

    return location_schema.dump(location)


@bp.route('/discover/test_me', methods=('GET', 'POST'))
@login_required
def test():
    status = (LocationStatus.HIDDEN if request.method == 'GET'
              else LocationStatus.FOUND)

    location = Location(
        id=uuid.uuid4(),
        name="Boarding",
        description=("Du hast einen Fensterplatz im Flugzeug und " +
                     "freust dich auf die lange erwatete Reise in den " +
                     "Großstadtdschungel. Der Gurt ist angelegt, der " +
                     "Sitz in einer aufrechten Position. Sobald wir die " +
                     "Starterlaubnis vom Tower bekommen, kann es losgehen!"),
        status=status
    )

    return location_schema.dump(location)
