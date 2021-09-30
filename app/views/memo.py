
from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template

from app import db
from app.models import Memo
from app.models import MemoGroup
from app.utils import get_user_from_session
from app.utils import check_login
from .group import bp as group_bp


bp = Blueprint(
    name="memo",
    import_name="memo",
    url_prefix="/memo",
)
bp.register_blueprint(group_bp)


# TODO:메모 목록 보여주기
@bp.get("")
def show_all():
    if not check_login():
        return redirect(url_for("manage.session.login"))

    return ""


# TODO:메모 쓰기
@bp.get("/write")
def write():
    return ""


@bp.post("/write")
def write_post():
    return redirect(url_for("manage.memo.edit", memo_id="a"))


# TODO:메모 수정
@bp.get("/<string:memo_id>")
def edit(memo_id: str):
    return ""


@bp.post("/<string:memo_id>")
def edit_post(memo_id: str):
    return redirect(url_for("manage.memo.edit", memo_id=memo_id))
