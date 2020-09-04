from app import db


class User(db.Model):
    __tablename__ = "users"

    # id type is String because it uses google user id returned from authorization which
    # does not fit into postgres BigInteger
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(60))
    email = db.Column(db.String(60))


class Wishlist(db.Model):
    __tablename__ = "wishlists"

    # id is generated from uuid4
    id = db.Column(db.String(32), primary_key=True)
    add_date = db.Column(db.Date)


class UserWishlist(db.Model):
    __tablename__ = "user_wishlist"

    # id is generated from uuid4
    id = db.Column(db.String(32), primary_key=True)
    user_id = db.Column(db.String(32), db.ForeignKey("users.id"), nullable=False)
    wishlists_id = db.Column(db.String(32), db.ForeignKey("wishlists.id"), nullable=False)


class WishlistItem(db.Model):
    __tablename__ = "wishlist_items"

    # id is generated from uuid4
    id = db.Column(db.String(32), primary_key=True)
    text = db.Column(db.String(200))
    is_reserved = db.Column(db.Boolean, default=False)
    wishlists_id = db.Column(db.String(32), db.ForeignKey("wishlists.id"), nullable=False)
