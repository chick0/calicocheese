
from flask import Blueprint
from flask import render_template

from app.models import Member

bp = Blueprint(
    name="index",
    import_name="index",
    url_prefix="/"
)


@bp.get("")
def about():
    members = Member.query.limit(10).all()
    return render_template(
        "index/about.html",
        members=members
    )
