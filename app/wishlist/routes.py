"""
This module defines routes in current namespace
"""

from datetime import date
from uuid import uuid4

from werkzeug.exceptions import BadRequest
from flask_restx import Resource, marshal_with

from app.wishlist import ns
from app.auth.decorators import login_required
from app.wishlist.marshal_models import wishlists_model
from app.wishlist.post_models import wishlist_post
from app.wishlist.argument_parsers import wishlist_parser
from app.models import Wishlist, User
from app.wishlist.dto import WishListDto, WishlistItemDto


@ns.route('/wishlist')
class WishlistListResource(Resource):

    @login_required
    @marshal_with(wishlists_model)
    def get(self, **kwargs):
        """
        Returns list of wishlists
        """

        user = User.query.filter_by(id=kwargs["user_id"]).first()

        wishlists = [
            WishListDto(
                wishlist.id,
                wishlist.name,
                wishlist.add_date,
                wishlist.user_id,
                [
                    WishlistItemDto(
                        item.id,
                        item.text,
                        item.is_reserved,
                        item.wishlists_id,
                    )
                    for item in wishlist.items
                ]
            )
            for wishlist in user.wishlists
        ]
        return {"wishlists": wishlists}

    @login_required
    @ns.expect(wishlist_post)
    def post(self, **kwargs):
        wishlist_id_ = uuid4().hex

        # getting arguments from request body
        args = wishlist_parser.parse_args()
        if not args.get("name"):
            raise BadRequest("name argument is required")

        Wishlist.add(Wishlist(
            id=wishlist_id_,
            name=args.get("name"),
            add_date=date.today(),
            user_id=kwargs["user_id"]
        ))

        return {"message": "success", "wishlist_id": wishlist_id_}
