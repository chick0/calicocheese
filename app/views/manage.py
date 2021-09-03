
from flask import Blueprint


bp = Blueprint(
    name="manage",
    import_name="manage",
    url_prefix="/manage"
)


@bp.get("")
def show_all():
    return "manage.show_all"


@bp.get("/write")
def write():
    return "manage.write"


@bp.post("/write")
def write_post():
    return "manage.write_post"


@bp.get("/edit")
def edit():
    return "edit.write"


@bp.post("/edit")
def edit_post():
    return "manage.edit_post"
