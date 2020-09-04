from functools import wraps

from flask import session
from werkzeug.exceptions import BadRequest


def login_required(f):
    """
    Checks if user is logged in, if so, passes user_id to a view function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = dict(session).get('user_id')
        if user:
            return f(*args, **kwargs, user_id=user)
        raise BadRequest("you need to be logged in to access this route, try to login first: /auth/login")
    return decorated_function
