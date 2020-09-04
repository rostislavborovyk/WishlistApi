from flask_restx.reqparse import RequestParser

wishlist_parser = RequestParser()

wishlist_parser.add_argument("name")
