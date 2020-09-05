from flask_restx.reqparse import RequestParser

wishlist_parser = RequestParser()  # parses from request body args

wishlist_parser.add_argument(
    "name",
    type=str
)

wishlist_item_id_parser = RequestParser()  # parses from request query args

wishlist_item_id_parser.add_argument(
    "wishlist_id",
    type=str
)

wishlist_item_args_parser = RequestParser()  # parses from request body args

wishlist_item_args_parser.add_argument(
    "text",
    type=str
)

wishlist_item_args_parser.add_argument(
    "is_reserved",
    type=str
)

