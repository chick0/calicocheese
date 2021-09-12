
from flask import Blueprint
from flask import abort
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template

from app import db
from app.models import Member
from app.models import Project
from app.models import Link
from app.utils import check_login
from app.utils import get_user_from_session


bp = Blueprint(
    name="link",
    import_name="link",
    url_prefix="/link",
)


@bp.get("/<int:project_id>")
def view(project_id: int):
    if not check_login():
        return redirect(url_for("manage.session.login"))

    user = get_user_from_session()

    project = Project.query.filter_by(
        id=project_id,
        owner=user.id
    ).first()

    if project is None:
        return abort(403)

    links = Link.query.filter_by(
        project_id=project_id
    ).all()

    return render_template(
        "manage/link/view.html",
        project_title=project.title,
        project_id=project.id,
        links=links
    )


@bp.get("/<int:project_id>/delete/<int:link_id>")
def delete(project_id: int, link_id: int):
    return "manage.link.delete"


@bp.post("/<int:project_id>/edit/<int:link_id>")
def edit_post(project_id: int, link_id: int):
    return "manage.link.edit_post"


@bp.post("/<int:project_id>/create")
def create_post(project_id: int):
    return "manage.link.create_post"
