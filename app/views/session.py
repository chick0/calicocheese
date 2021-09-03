
from flask import Blueprint
from flask import session
from flask import redirect
from flask import url_for


bp = Blueprint(
    name="session",
    import_name="session",
    url_prefix="/"
)


@bp.get("/logout")
def logout():
    for key in list(session.keys()):
        del session[key]

    return redirect(url_for("member.session.login"))


@bp.get("/login")
def login():
    return "member.session.login -> github oauth"


@bp.get("/callback")
def callback():
    return "member.session.callback <- github oauth"
