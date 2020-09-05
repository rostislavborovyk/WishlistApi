"""
This module defines event models used in @marshal_with decorator in routes module
"""

from flask_restx import fields

from app import api

wishlist_get_item_marshal_model = api.model('Wishlist item', {
    'id': fields.String,
    'text': fields.String,
    'is_reserved': fields.Boolean,
    'wishlists_id': fields.String,
})

wishlist_get_marshal_model = api.model('Wishlist', {
    'id': fields.String,
    'name': fields.String,
    'add_date': fields.Date,
    'user_ids': fields.String,
    'items': fields.List(fields.Nested(wishlist_get_item_marshal_model)),
})

wishlists_get_marshal_model = api.model('Wishlists get', {
    'wishlists': fields.List(fields.Nested(wishlist_get_marshal_model)),
})
