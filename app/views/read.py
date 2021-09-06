
from flask import Blueprint
from flask import render_template

from app import db
from app.models import Project
from app.models import Member
from app.utils import check_login


bp = Blueprint(
    name="read",
    import_name="read",
    url_prefix="/read"
)


@bp.get("/<int:project_id>")
def project(project_id):
    pj = Project.query.filter_by(
        id=project_id
    ).first()

    return render_template(
        "member/read/project.html",
        title=pj.title,
        html=pj.html
    )
