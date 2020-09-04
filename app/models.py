from app import db
from typing import Optional


class AddMixin:
    @classmethod
    def add(cls, db_object: db.Model) -> None:
        db.session.add(db_object)
        db.session.commit()


class DeleteByIdMixin:
    @classmethod
    def delete_by_id(cls, id_: str) -> None:
        if obj := cls.query.filter_by(id=id_).first():
            db.session.delete(obj)
            db.session.commit()


class User(AddMixin, DeleteByIdMixin, db.Model):
    __tablename__ = "users"

    # id type is String because it uses google user id returned from authorization which
    # does not fit into postgres BigInteger
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(60))
    email = db.Column(db.String(60))
    wishlists = db.relationship("Wishlist", backref="user", lazy="joined")

    @classmethod
    def find_by_id(cls, id_: str) -> Optional[db.Model]:
        return cls.query.filter_by(id=id_).first()


class Wishlist(AddMixin, DeleteByIdMixin, db.Model):
    __tablename__ = "wishlists"

    # id is generated from uuid4
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(60))
    add_date = db.Column(db.Date)
    user_id = db.Column(db.String(32), db.ForeignKey("users.id"))
    items = db.relationship("WishlistItem", backref="wishlist", lazy="joined")


class WishlistItem(AddMixin, db.Model):
    __tablename__ = "wishlist_items"

    # id is generated from uuid4
    id = db.Column(db.String(32), primary_key=True)
    text = db.Column(db.String(200))
    is_reserved = db.Column(db.Boolean, default=False)
    wishlists_id = db.Column(db.String(32), db.ForeignKey("wishlists.id"))
