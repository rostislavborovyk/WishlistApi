"""
This module defines routes in current namespace
"""

from datetime import datetime
from werkzeug.exceptions import BadRequest
from flask_restx import Resource

from app.wishlist import ns
from app.models import *


@ns.route('/wishlist')
class Wishlist(Resource):

    @ns.doc("Wishlist endpoint")
    def get(self, **kwargs):
        return {'message': "ok"}
