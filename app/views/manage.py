
from flask import Blueprint
from flask import abort
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template

from app import db
from app.models import Member
from app.models import Project
from app.utils import check_login
from app.utils import get_user_from_session
from .upload import bp as upload_bp
from .session import bp as session_bp
from .files import bp as files_bp
from .me import bp as me_bp
from .link import bp as link_bp


bp = Blueprint(
    name="manage",
    import_name="manage",
    url_prefix="/manage"
)
bp.register_blueprint(upload_bp)
bp.register_blueprint(session_bp)
bp.register_blueprint(files_bp)
bp.register_blueprint(me_bp)
bp.register_blueprint(link_bp)


@bp.get("/me")
def me():
    if not check_login():
        return redirect(url_for("manage.session.login"))

    user = get_user_from_session()

    member = Member.query.filter_by(
        id=user.id
    ).first()

    private_project = Project.query.filter_by(
        owner=member.id,
        public=False
    ).count()

    return render_template(
        "manage/me.html",
        member=member,
        private_project=private_project
    )


@bp.get("/write")
def write():
    if not check_login():
        return redirect(url_for("manage.session.login"))

    return render_template(
        "manage/write.html"
    )


@bp.post("/write")
def write_post():
    if not check_login():
        return redirect(url_for("manage.session.login"))

    user = get_user_from_session()

    project = Project()
    project.owner = user.id
    project.title = request.form.get("title", "제목없는 프로젝트")
    project.html = request.form.get("editor", "")
    project.public = True if request.form.get("public", "false") == "true" else False

    db.session.add(project)
    db.session.commit()

    return redirect(url_for("project.warp", project_id=project.id))


@bp.get("/edit/<int:project_id>")
def edit(project_id: int):
    if not check_login():
        return redirect(url_for("manage.session.login"))

    project = Project.query.filter_by(
        id=project_id
    ).first()

    if project is None:
        return abort(404)

    user = get_user_from_session()

    member = Member.query.filter_by(
        id=user.id
    ).first()

    if member.id == project.owner or member.is_admin:
        pass
    else:
        return abort(403)

    return render_template(
        "manage/edit.html",
        title=project.title,
        html=project.html
    )


@bp.post("/edit/<int:project_id>")
def edit_post(project_id: int):
    if not check_login():
        return redirect(url_for("manage.session.login"))

    project = Project.query.filter_by(
        id=project_id
    ).first()

    if project is None:
        return abort(404)

    user = get_user_from_session()

    member = Member.query.filter_by(
        id=user.id
    ).first()

    if member.id == project.owner or member.is_admin:
        pass
    else:
        return abort(403)

    project.title = request.form.get("title", project.title)
    project.html = request.form.get("editor", project.html)
    project.public = True if request.form.get("public", "false") == "true" else False

    db.session.commit()

    return redirect(url_for("project.warp", project_id=project_id))


@bp.get("/delete/<int:project_id>")
def delete(project_id: int):
    if not check_login():
        return redirect(url_for("manage.session.login"))

    user = get_user_from_session()

    project = Project.query.filter_by(
        id=project_id,
        owner=user.id
    ).first()

    if project is None:
        return abort(403)

    db.session.delete(project)
    db.session.commit()

    return redirect(url_for("project.show_all"))
