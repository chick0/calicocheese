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
    url_prefix="/session"
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
        return redirect(url_for("manage.session.login"))

    user = get_user(access_token)
    member = Member.query.filter_by(
        id=user.id
    ).first()

    if member is None:
        session['guest'] = True
        session['session'] = {
            "access_token": dumps(access_token),
            "user": dumps(user),
        }

        return redirect(url_for("contact.select"))

    session['guest'] = False
    session['session'] = {
        "access_token": dumps(access_token),
        "user": dumps(user),
    }

    if member.auto_update:
        for key in [
            "email",
            "blog",
            "bio",
        ]:
            value = getattr(user, key)
            if value is not None:
                setattr(member, key, value)

    member.two_factor_authentication = user.two_factor_authentication

    db.session.commit()

    return redirect(url_for("manage.me"))
