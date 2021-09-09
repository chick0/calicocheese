
from flask import Blueprint
from flask import abort
from flask import render_template

from app.models import Member
from app.models import Project
from app.utils import get_user_from_session
from app.error import UserNotLogin
from app.error import PrivateProject


bp = Blueprint(
    name="read",
    import_name="read",
    url_prefix="/"
)


@bp.get("/<string:name>/<int:project_id>")
def project(name: str, project_id: int):
    member = Member.query.filter_by(
        name=name
    ).first()

    if member is None:
        return abort(404)

    pj = Project.query.filter_by(
        id=project_id,
        owner=member.id
    ).first()

    if pj is None:
        return abort(404)

    try:
        user = get_user_from_session()
        is_owner = pj.owner == user.id
    except UserNotLogin:
        user = None
        is_owner = False

    if not pj.public:
        if user is None:
            raise PrivateProject

    return render_template(
        "member/read/project.html",
        title=pj.title,
        html=pj.html,
        project_id=pj.id,
        is_owner=is_owner
    )
