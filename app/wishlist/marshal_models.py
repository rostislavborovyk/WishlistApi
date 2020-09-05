"""
This module defines event models used in @marshal_with decorator in routes module
"""

from flask_restx import fields

from app import api

wishlist_item_get_marshal_model = api.model('Wishlist item', {
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
    'items': fields.List(fields.Nested(wishlist_item_get_marshal_model)),
})

wishlists_get_marshal_model = api.model('Wishlists get', {
    'wishlists': fields.List(fields.Nested(wishlist_get_marshal_model)),
})

wishlist_items_get_marshal_model = api.model('Wishlist items get', {
    'wishlist_items': fields.List(fields.Nested(wishlist_item_get_marshal_model)),
})
