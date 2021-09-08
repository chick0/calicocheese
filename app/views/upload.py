
from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template

from app import db
from app.models import File
from app.utils import check_login
from app.utils import get_user_from_session


bp = Blueprint(
    name="upload",
    import_name="upload",
    url_prefix="/upload"
)


@bp.get("")
def form():
    if not check_login():
        return redirect(url_for("manage.session.login"))

    return render_template(
        "upload/form.html"
    )


@bp.post("")
def form_post():
    if not check_login():
        return redirect(url_for("manage.session.login"))

    return "upload.form_post"
