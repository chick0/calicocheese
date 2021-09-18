
from flask import Blueprint
from flask import g
from flask import abort
from flask import request
from flask import render_template

from app.models import Member
from app.models import Project
from .read import bp as read_bp


bp = Blueprint(
    name="member",
    import_name="member",
    url_prefix="/"
)
bp.register_blueprint(read_bp)


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

    g.title = name
    g.description = member.bio

    return render_template(
        "member/show.html",
        member=member,
        projects=projects,
        pages=pages
    )
