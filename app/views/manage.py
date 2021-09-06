
from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template

from app import db
from app.models import Project
from app.utils import check_login
from app.utils import get_user_from_session


bp = Blueprint(
    name="manage",
    import_name="manage",
    url_prefix="/manage"
)


@bp.get("")
def show_all():
    if not check_login():
        return redirect(url_for("member.session.login"))

    return "manage.show_all"


@bp.get("/write")
def write():
    if not check_login():
        return redirect(url_for("member.session.login"))

    return render_template(
        "manage/write.html"
    )


@bp.post("/write")
def write_post():
    if not check_login():
        return redirect(url_for("member.session.login"))

    user = get_user_from_session()

    project = Project()
    project.owner = user.id
    project.title = request.form.get("title", "제목없는 프로젝트")
    project.html = request.form.get("editor", "")
    project.public = True if request.form.get("public", "false") == "true" else False

    db.session.add(project)
    db.session.commit()

    return redirect(url_for("member.read.project", project_id=project.id))


@bp.get("/edit")
def edit():
    if not check_login():
        return redirect(url_for("member.session.login"))

    return "edit.write"


@bp.post("/edit")
def edit_post():
    if not check_login():
        return redirect(url_for("member.session.login"))

    return "manage.edit_post"
