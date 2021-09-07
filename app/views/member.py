
from flask import Blueprint
from flask import abort
from flask import request
from flask import render_template

from app.models import Member
from app.models import Project
from .read import bp as read_bp
from .session import bp as session_bp


bp = Blueprint(
    name="member",
    import_name="member",
    url_prefix="/"
)
bp.register_blueprint(read_bp)
bp.register_blueprint(session_bp)


@bp.get("/<string:name>")
def show(name: str):
    member = Member.query.filter_by(
        name=name
    ).first()

    if member is None:
        return abort(404)

    try:
        page = int(request.args.get("page", "1"))

        if page <= 0:
            page = 1
    except ValueError:
        page = 1

    projects = Project.query.filter_by(
        owner=member.id
    ).order_by(
        Project.id.desc()
    ).paginate(page)

    return render_template(
        "member/show.html",
        member=member,
        projects=projects
    )
