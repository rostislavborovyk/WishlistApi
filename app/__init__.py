"""
This module initializes api object and defines create_app function
"""

from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth

from config import DevelopmentConfig

api = Api(
    ordered=True,
    title="api_v1",
    version='1.0',
    description='API v1',
    doc="/api/info/"
)
db = SQLAlchemy()
migrate = Migrate()
oauth = OAuth()


def _register_extensions(app: Flask) -> None:
    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    oauth.init_app(app)


def _add_namespaces(api: Api) -> None:
    from app.wishlist import ns as wishlist_ns
    api.add_namespace(wishlist_ns)


def _register_blueprints(app: Flask) -> None:
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")


def create_app(config=DevelopmentConfig) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    app.app_context().push()
    _register_extensions(app)
    _add_namespaces(api)
    _register_blueprints(app)
    return app

# todo add docs
