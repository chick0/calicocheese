
from flask import Blueprint


bp = Blueprint(
    name="index",
    import_name="index",
    url_prefix="/"
)


@bp.get("")
def about():
    return "index.about"
