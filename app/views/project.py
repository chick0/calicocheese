
from flask import Blueprint
from flask import abort
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template

from app.models import Member
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

    pages = []

    if projects.page < 3:
        for i in range(1, projects.pages + 1):
            if len(pages) == 5:
                break

            pages.append(i)
    else:
        for i in range(projects.page - 2, projects.pages + 1):
            if len(pages) == 5:
                break

            pages.append(i)

    return render_template(
        "project/show_all.html",
        projects=projects,
        pages=pages
    )


@bp.get("/warp/<int:project_id>")
def warp(project_id: int):
    project = Project.query.filter_by(
        id=project_id
    ).first()

    if project is None:
        return abort(404)

    member = Member.query.filter_by(
        id=project.owner
    ).first()

    if member is None:
        return abort(404)

    return redirect(
        url_for(
            "member.read.project",
            name=member.name,
            project_id=project.id,
            project_title=project.title
        )
    )
