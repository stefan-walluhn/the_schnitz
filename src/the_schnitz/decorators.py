from functools import wraps
from flask import session
from werkzeug.exceptions import Unauthorized


def login_required(f):
    @wraps(f)
    def ensure_login(*args, **kwargs):
        if not session.get('i_am_allowed_to_play', False):
            raise Unauthorized()

        return f(*args, **kwargs)

    return ensure_login
