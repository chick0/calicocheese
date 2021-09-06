
from flask import Blueprint
from flask import request
from flask import render_template

from app.models import Project


bp = Blueprint(
    name="project",
    import_name="project",
    url_prefix="/project"
)


@bp.get("")
def show_all():
    try:
        page = int(request.args.get("page", "1"))

        if page <= 0:
            page = 1
    except ValueError:
        page = 1

    projects = Project.query.order_by(
        Project.id.desc()
    ).paginate(page)

    return render_template(
        "project/show_all.html",
        projects=projects
    )

