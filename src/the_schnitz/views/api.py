from flask import Blueprint, request, session
from werkzeug.exceptions import Unauthorized

from the_schnitz.app import authorization_service


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
