"""
This module defines routes for share_wishlist resource
"""

from werkzeug.exceptions import BadRequest
from flask_restx import Resource

from app.wishlist import ns
from app.auth.decorators import login_required

from app.wishlist.post_models import (
    share_wishlist_put_args
)
from app.wishlist.argument_parsers import (
    share_wishlist_args_parser
)
from app.models import Wishlist, User, UserWishlistAssociation, db


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
