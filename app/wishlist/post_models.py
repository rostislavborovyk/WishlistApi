"""
Module defines models of json body in post requests
"""

from flask_restx import fields, model

from app import api

wishlist_post_args = api.model("Wishlist", {
    "name": fields.String(description="Wishlist name")
})

wishlist_item_post_args = api.model("Wishlist item", {
    "text": fields.String(description="Wishlist item text")
})

wishlist_item_put_args = api.inherit("Wishlist item put", wishlist_item_post_args, {
    "is_reserved": fields.Boolean(description="if is_reserved is set to True you can't delete this item"),
})
