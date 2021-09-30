
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


bp = Blueprint(
    name="group",
    import_name="group",
    url_prefix="/group",
)


@bp.get("")
def show_all():
    return


# TODO:메모 그룹 생성
@bp.get("/create")
def create():
    return ""


@bp.post("/create")
def create_post():
    return ""


# TODO:메모 그룹 수정
@bp.get("/edit/<string:group_id>")
def edit(group_id: str):
    return ""


@bp.post("/edit/<string:group_id>")
def edit_post(group_id: str):
    return ""


# TODO:메모 그룹 삭제
@bp.get("/delete/<string:group_id>")
def delete(group_id: str):
    return ""
