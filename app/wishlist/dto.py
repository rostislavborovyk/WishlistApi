"""
This module defines data access object classes used for creating response data
"""


class WishlistItemDto:
    """
    Class for storing the attributes date and value
    """
    __slots__ = ["id", "text", "is_reserved", "wishlists_id"]  # for faster creation of objects

    def __init__(self, id_: str, text: str, is_reserved: bool, wishlists_id: str):
        self.id = id_
        self.text = text
        self.is_reserved = is_reserved
        self.wishlists_id = wishlists_id


class WishListDto:
    """
    Class for storing the attributes date and value
    """
    __slots__ = ["id", "name", "add_date", "user_id", "items"]  # for faster creation of objects

    def __init__(self, id_: str, name: str, add_date: bool, user_id: str, items: list):
        self.id = id_
        self.name = name
        self.add_date = add_date
        self.user_id = user_id
        self.items = items
