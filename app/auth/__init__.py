"""
This module creates flask Blueprint for flask routes of this package
"""

from flask import Blueprint
from app import oauth

# assigning type Blueprint because mypy don't recognize type
bp: Blueprint = Blueprint(
    "auth",
    __name__,
)

# todo hide secret values
google = oauth.register(
    name='google',
    client_id="325337173671-hs1abvm8183folfkv6pjm91nsntldll7.apps.googleusercontent.com",
    client_secret="NOTE7579Rve5LPFnMRqZQ7li",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
)

from app.auth.routes import *
