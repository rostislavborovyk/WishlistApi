"""
Module defines models of json body in post requests
"""

from flask_restx import fields

from app import api

wishlist_post = api.model("Wishlist", {
    "name": fields.String(description="Name of the wishlist")
})
