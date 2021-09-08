
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
    name="files",
    import_name="files",
    url_prefix="/files"
)


@bp.get("")
def show_all():
    if not check_login():
        return redirect(url_for("manage.session.login"))

    return render_template(
        "manage/files/show_all.html"
    )


@bp.get("/<int:file_id>")
def detail(file_id: int):
    if not check_login():
        return redirect(url_for("manage.session.login"))

    return render_template(
        "manage/files/detail.html"
    )


@bp.get("/<int:file_id>/edit")
def edit(file_id: int):
    if not check_login():
        return redirect(url_for("manage.session.login"))

    return render_template(
        "manage/files/edit.html"
    )


@bp.post("/<int:file_id>/edit")
def edit_post(file_id: int):
    if not check_login():
        return redirect(url_for("manage.session.login"))

    return f"manage.files.edit : post : {file_id}"


@bp.get("/<int:file_id>/delete")
def delete(file_id: int):
    if not check_login():
        return redirect(url_for("manage.session.login"))

    return render_template(
        "manage/files/delete.html"
    )
