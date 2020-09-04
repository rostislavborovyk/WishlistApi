"""
This module defines routes in current namespace
"""

from datetime import datetime
from werkzeug.exceptions import BadRequest
from flask_restx import Resource

from app.wishlist import ns


@ns.route('/wishlist')
class Timeline(Resource):

    @ns.doc("Wishlist endpoint")
    def get(self, **kwargs):
        return {'message': "ok"}
