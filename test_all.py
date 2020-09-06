import json
import unittest
from config import TestingConfig

from app import create_app, db
from app.models import User


def add_user(id_):
    u = User(id=id_, name="test_name", email="test_email")
    db.session.add(u)
    db.session.commit()


def remove_user(id_):
    u = User.query.filter_by(id=id_).first()
    db.session.delete(u)
    db.session.commit()


# class TestWishlistApi(unittest.TestCase):
#     def setUp(self) -> None:
#         self.app = create_app(TestingConfig)
#         self.app_context = self.app.app_context()
#         self.app_context.push()
#         db.create_all()
#         add_user(self.app.config["TEST_USER_ID"])
#
#     def tearDown(self) -> None:
#         remove_user(self.app.config["TEST_USER_ID"])
#         self.app_context.pop()
#
#     def test_wishlist(self) -> None:
#         with self.app.test_client() as c:
#             data = {"name": "test_wishlist"}
#             response = c.post(
#                 "/api/wishlist",
#                 headers={'Content-Type': 'application/json'},
#                 data=json.dumps(data)
#             )
#
#             self.assertEqual(response.status_code, 201)
#             id_ = response.get_data().decode("utf-8").strip("\n").strip("\"")
#
#             response = c.get("/api/wishlist")
#             self.assertEqual(response.status_code, 200)
#
#             response = c.delete(
#                 f'/api/wishlist/{id_}',
#             )
#             self.assertEqual(response.status_code, 204)


class TestWishlistItemApi(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        add_user(self.app.config["TEST_USER_ID"])

    def tearDown(self) -> None:
        remove_user(self.app.config["TEST_USER_ID"])
        self.app_context.pop()

    def test_wishlist_item(self) -> None:
        with self.app.test_client() as c:
            data = {"name": "test_wishlist"}
            response = c.post(
                "/api/wishlist",
                headers={'Content-Type': 'application/json'},
                data=json.dumps(data)
            )

            self.assertEqual(response.status_code, 201)
            wishlist_id_ = response.get_data().decode("utf-8").strip("\n").strip("\"")

            data = {"text": "my first wish"}
            response = c.post(
                f"/api/wishlist_item?wishlist_id={wishlist_id_}",
                headers={'Content-Type': 'application/json'},
                data=json.dumps(data)
            )
            wishlist_item_id_ = response.get_data().decode("utf-8").strip("\n").strip("\"")
            self.assertEqual(response.status_code, 201)

            response = c.delete(
                f'/api/wishlist_item/{wishlist_item_id_}',
            )
            self.assertEqual(response.status_code, 204)

            response = c.delete(
                f'/api/wishlist/{wishlist_id_}',
            )
            self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main(verbosity=2)
