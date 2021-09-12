from json import loads
from json import dumps

from flask import Blueprint
from flask import session
from flask import request
from flask import redirect
from flask import url_for

from app import db
from app.models import Member
from app.utils import check_login
from app.utils import get_user_from_session
from app.github import AccessToken
from app.github import get_user


bp = Blueprint(
    name="me",
    import_name="me",
    url_prefix="/me"
)


@bp.post("/update")
def update_post():
    if not check_login():
        return redirect(url_for("manage.session.login"))

    user = get_user_from_session()

    member = Member.query.filter_by(
        id=user.id
    ).first()

    member.auto_update = True if request.form.get("update", "false") == "true" else False

    db.session.commit()

    return redirect(url_for("manage.me"))


@bp.post("/member")
def member_post():
    if not check_login():
        return redirect(url_for("manage.session.login"))

    user = get_user_from_session()

    member = Member.query.filter_by(
        id=user.id
    ).first()

    member.blog = request.form.get("blog", member.blog)[:255]
    member.bio = request.form.get("bio", member.bio)

    db.session.commit()

    return redirect(url_for("manage.me"))


@bp.get("/github")
def github():
    if not check_login():
        return redirect(url_for("manage.session.login"))

    at = session.get("session", {}).get("access_token")
    if len(at) <= 0:
        return redirect(url_for("manage.me"))

    access_token = AccessToken(*loads(at))

    user = get_user(access_token=access_token)

    member = Member.query.filter_by(
        id=user.id
    ).first()

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

    return redirect(url_for("manage.me"))
