from json import dumps

from flask import Blueprint
from flask import session
from flask import request
from flask import redirect
from flask import url_for

from app import db
from app.models import Member
from app.github import build_url
from app.github import generate_access_token
from app.github import get_user


bp = Blueprint(
    name="session",
    import_name="session",
    url_prefix="/"
)


@bp.get("/logout")
def logout():
    for key in list(session.keys()):
        del session[key]

    return redirect(url_for("index.about"))


@bp.get("/login")
def login():
    return redirect(build_url())


@bp.get("/callback")
def callback():
    code = request.args.get("code", "#")

    access_token = generate_access_token(code=code)
    if access_token.token == "":
        return redirect(url_for("member.session.login"))

    user = get_user(access_token)
    member = Member.query.filter_by(
        id=user.id
    ).first()

    if member is None:
        return "You are not member of Calico Cheese!"

    session['session'] = {
        "access_token": dumps(access_token),
        "user": dumps(user),
    }

    if member.email != user.email:
        member.email = user.email

    if member.blog != user.blog:
        member.blog = user.blog

    if member.two_factor_authentication != user.two_factor_authentication:
        member.two_factor_authentication = user.two_factor_authentication

    if member.bio != user.bio:
        member.bio = user.bio

    db.session.commit()

    return redirect(url_for("manage.show_all"))
