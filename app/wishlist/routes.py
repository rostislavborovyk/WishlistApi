"""
This module defines routes in current namespace
"""

from datetime import date
from uuid import uuid4

from werkzeug.exceptions import BadRequest
from flask_restx import Resource, marshal_with

from app.wishlist import ns
from app.auth.decorators import login_required
from app.wishlist.marshal_models import (
    wishlists_get_marshal_model,
    wishlist_get_marshal_model,
    wishlist_items_get_marshal_model,
    wishlist_item_get_marshal_model,
)
from app.wishlist.post_models import (
    wishlist_post_args,
    wishlist_item_post_args,
    wishlist_item_put_args,
    share_wishlist_put_args
)
from app.wishlist.argument_parsers import (
    wishlist_parser,
    wishlist_item_id_parser,
    wishlist_item_args_parser,
    share_wishlist_args_parser
)
from app.models import Wishlist, User, UserWishlistAssociation, WishlistItem, db
from app.wishlist.dto import WishListDto, WishlistItemDto


@ns.route('/wishlist')
class WishlistListResource(Resource):
    @login_required
    @marshal_with(wishlists_get_marshal_model)
    def get(self, **kwargs):
        """
        Returns list of wishlists
        """

        user = User.query.filter_by(id=kwargs["user_id"]).first()

        # wishlist returns items with all details but probably wish list here should return
        # just number of items in it
        wishlists = [
            WishListDto(
                wishlist.wishlist.id,
                wishlist.wishlist.name,
                wishlist.wishlist.add_date,
                [user.user.id for user in wishlist.wishlist.users],  # returns ids of all users that have this wishlist
                [
                    WishlistItemDto(
                        item.id,
                        item.text,
                        item.is_reserved,
                        item.wishlist_id,
                    )
                    for item in wishlist.wishlist.items
                ]
            )
            for wishlist in user.wishlists
        ]
        return {"wishlists": wishlists}

    @login_required
    @ns.response(201, "Wishlist successfully added")
    @ns.expect(wishlist_post_args)
    def post(self, **kwargs):
        """
        Adds wishlist to current user's collection
        """

        # getting arguments from request body
        args = wishlist_parser.parse_args()
        if not args.get("name"):
            raise BadRequest("name argument is required")

        # adding wishlist and user_wishlist association to db
        user = User.find_by_id(kwargs["user_id"])
        a = UserWishlistAssociation()
        a.wishlist = Wishlist(
            id=uuid4().hex,
            name=args.get("name"),
            add_date=date.today(),
        )
        user.wishlists.append(a)
        db.session.commit()

        return None, 201


@ns.route('/wishlist/<string:id_>')
@ns.response(404, "Wishlist not found")
class WishlistResource(Resource):

    @login_required
    @marshal_with(wishlist_get_marshal_model)
    def get(self, id_: str, **kwargs):
        """
        Returns wishlist with specified id
        """

        wishlist = Wishlist.query.filter_by(id=id_).first_or_404()
        wishlist_response = WishListDto(
            wishlist.id,
            wishlist.name,
            wishlist.add_date,
            [user.user.id for user in wishlist.users],  # returns ids of all users that have this wishlist
            [
                WishlistItemDto(
                    item.id,
                    item.text,
                    item.is_reserved,
                    item.wishlist_id,
                )
                for item in wishlist.items
            ]
        )

        return wishlist_response

    @login_required
    @ns.response(204, "Wishlist successfully deleted")
    @ns.response(500, "Error with db")
    def delete(self, id_, **kwargs):
        """
        Deletes wishlist with specified id
        """

        # transaction to delete both user_wishlist and wishlist objects
        try:
            user = User.find_by_id(kwargs["user_id"])
            wishlist = Wishlist.query.filter_by(id=id_).first_or_404()
            a = UserWishlistAssociation.query.filter_by(user_id=user.id, wishlist_id=wishlist.id).first_or_404()
            db.session.delete(a)
            db.session.delete(wishlist)

            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return None, 500
        return None, 204

    @login_required
    @ns.response(200, "Wishlist updated")
    @ns.expect(wishlist_post_args)
    def put(self, id_, **kwargs):
        """
        Updates wishlist with specified id
        """
        wishlist = Wishlist.query.filter_by(id=id_).first_or_404()

        args = wishlist_parser.parse_args()
        if not args.get("name"):
            raise BadRequest("name argument is required")
        wishlist.name = args.get("name")
        db.session.commit()
        return None, 200


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

        wishlist.items.append(
            WishlistItem(
                id=uuid4().hex,
                text=item_args.get("text"),
            )
        )

        db.session.commit()
        return None, 201


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


@ns.route('/share_wishlist')
@ns.response(404, "Wishlist or user not found")
class ShareWishlistResource(Resource):

    @login_required
    @ns.expect(share_wishlist_put_args)
    @ns.response(200, "Wishlist successfully added to user")
    @ns.response(400, "Wishlist should belong to current logged in user")
    def put(self, **kwargs):
        """
        Share wish list which id you specified with user whose id you specified
        """

        args = share_wishlist_args_parser.parse_args()
        if (user_id := args.get("user_id")) and (wishlist_id := args.get("wishlist_id")):
            user = User.query.filter_by(id=user_id).first_or_404()
            wishlist = Wishlist.query.filter_by(id=wishlist_id).first_or_404()

            # check if wishlist belongs to current logged in user
            cur_logged_in_user = User.find_by_id(kwargs["user_id"])
            if cur_logged_in_user.id not in map(lambda x: x.user.id, wishlist.users):
                raise BadRequest("Wishlist should belong to current logged in user")

            # adding wishlist to a user and user_wishlist association to db
            a = UserWishlistAssociation()
            a.wishlist = wishlist
            a.user = user
            user.wishlists.append(a)
            db.session.commit()
        return None, 200
