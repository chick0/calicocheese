from os import path
from os import mkdir

from flask import g
from flask import Flask
from flask import request
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
    app.config['MAX_CONTENT_LENGTH'] = 30 * 1000 * 1000

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

    from . import template_filter
    for filter_name in [x for x in dir(template_filter) if not x.startswith("__")]:
        app.add_template_filter(getattr(template_filter, filter_name), name=filter_name)

    from .error_map import error_map
    for code_or_exception in error_map.keys():
        app.register_error_handler(
            code_or_exception=code_or_exception,
            f=error_map[code_or_exception]
        )

    @app.before_request
    def set_metadata():
        g.title = "Calico Cheese"
        g.description = "칼리코 치즈는 프로그램을 개발하는 팀 입니다."
        g.canonical = request.scheme + "://" + request.host

    return app
