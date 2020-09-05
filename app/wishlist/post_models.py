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

