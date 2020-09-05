"""
This module defines routes for wishlist item resources
"""

from uuid import uuid4

from werkzeug.exceptions import BadRequest
from flask_restx import Resource, marshal_with

from app.wishlist import ns
from app.auth.decorators import login_required
from app.wishlist.marshal_models import (
    wishlist_items_get_marshal_model,
    wishlist_item_get_marshal_model,
)
from app.wishlist.post_models import (
    wishlist_item_post_args,
    wishlist_item_put_args,
)
from app.wishlist.argument_parsers import (
    wishlist_item_id_parser,
    wishlist_item_args_parser,
)
from app.models import Wishlist, WishlistItem, db
from app.wishlist.dto import WishlistItemDto


@ns.route('/wishlist_item')
@ns.response(404, "Wishlist not found")
class WishlistItemListResource(Resource):

    @login_required
    @ns.expect(wishlist_item_id_parser)
    @marshal_with(wishlist_items_get_marshal_model)
    def get(self, **kwargs):
        """
        Returns all items in wishlist with specified id
        """
        # getting arguments from request body
        wishlist_id_args = wishlist_item_id_parser.parse_args()
        if not wishlist_id_args.get("wishlist_id"):
            raise BadRequest("wishlist_id argument is required")

        wishlist = Wishlist.query.filter_by(id=wishlist_id_args.get("wishlist_id")).first_or_404()

        resp_items = [
            WishlistItemDto(
                item.id,
                item.text,
                item.is_reserved,
                item.wishlist_id,
            )
            for item in wishlist.items
        ]
        return {"wishlist_items": resp_items}

    @login_required
    @ns.response(201, "Wishlist item successfully added")
    @ns.expect(wishlist_item_id_parser, wishlist_item_post_args)
    def post(self, **kwargs):
        """
        Adds wishlist item to current wishlist with specified id
        """

        # getting arguments from request body
        wishlist_id_args = wishlist_item_id_parser.parse_args()
        if not wishlist_id_args.get("wishlist_id"):
            raise BadRequest("wishlist_id argument is required")

        wishlist = Wishlist.query.filter_by(id=wishlist_id_args.get("wishlist_id")).first_or_404()

        item_args = wishlist_item_args_parser.parse_args()

        item = WishlistItem(id=uuid4().hex, text=item_args.get("text"))
        wishlist.items.append(item)

        db.session.commit()
        return item.id, 201


@ns.route('/wishlist_item/<string:id_>')
@ns.response(404, "Wishlist not found")
class WishlistItemResource(Resource):

    @login_required
    @marshal_with(wishlist_item_get_marshal_model)
    def get(self, id_: str, **kwargs):
        """
        Returns wishlist item with specified id
        """

        item = WishlistItem.query.filter_by(id=id_).first_or_404()

        return WishlistItemDto(
            id_,
            item.text,
            item.is_reserved,
            item.wishlist_id,
        )

    @login_required
    @ns.response(204, "Wishlist item successfully deleted")
    @ns.response(500, "Error with db")
    @ns.response(400, "Wishlist item is reserved")
    def delete(self, id_, **kwargs):
        """
        Deletes wishlist item with specified id
        """

        item = WishlistItem.query.filter_by(id=id_).first_or_404()
        if not item.is_reserved:
            db.session.delete(item)
        else:
            raise BadRequest("This item is reserved, you cant delete it")
        db.session.commit()
        return None, 204

    @login_required
    @ns.response(200, "Wishlist item updated")
    @ns.expect(wishlist_item_put_args)
    def put(self, id_, **kwargs):
        """
        Updates wishlist item with specified id
        """
        item = WishlistItem.query.filter_by(id=id_).first_or_404()

        args = wishlist_item_args_parser.parse_args()

        if name := args.get("name"):
            item.name = name

        if is_reserved := args.get("is_reserved"):
            item.is_reserved = bool(is_reserved)

        db.session.commit()
        return None, 200
