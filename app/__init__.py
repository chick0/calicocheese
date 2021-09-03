from os import path
from os import mkdir

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
UPLOAD_DIR = path.join(BASE_DIR, "app", "upload")
CONFIG_DIR = path.join(BASE_DIR, "config")


def test_path():
    if not path.isdir(UPLOAD_DIR):
        mkdir(UPLOAD_DIR)

    if not path.isdir(CONFIG_DIR):
        mkdir(CONFIG_DIR)


def test_config():
    from .config import test_config
    test_config()


def create_app():
    test_path()
    test_config()

    app = Flask(__name__)

    from .secret_key import SECRET_KEY
    app.config['SECRET_KEY'] = SECRET_KEY

    from .database import get_url
    app.config['SQLALCHEMY_DATABASE_URI'] = get_url()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    __import__("app.models")
    db.init_app(app)
    migrate.init_app(app, db)

    from . import views
    for view in views.__all__:
        app.register_blueprint(getattr(getattr(views, view), "bp"))

    return app
