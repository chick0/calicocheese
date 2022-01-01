from os.path import join
from hashlib import md5
from hashlib import sha1
from hashlib import sha256

from flask import Blueprint
from flask import request
from flask import current_app
from flask import redirect
from flask import url_for
from flask import render_template

from app import UPLOAD_DIR
from app import db
from app.models import File
from app.models import CheckSum
from app.utils import check_login
from app.utils import get_user_from_session
from app.error import FileIsEmpty
from app.error import FileIsTooBig

bp = Blueprint(
    name="files",
    import_name="files",
    url_prefix="/files"
)


@bp.get("")
def show_all():
    if not check_login():
        return redirect(url_for("manage.session.login"))

    user = get_user_from_session()

    files = File.query.filter_by(
        owner=user.id
    ).order_by(
        File.id.desc()
    ).all()

    return render_template(
        "manage/files/show_all.html",
        files=files
    )


@bp.get("/<int:file_id>")
def detail(file_id: int):
    if not check_login():
        return redirect(url_for("manage.session.login"))

    user = get_user_from_session()

    file = File.query.filter_by(
        id=file_id,
        owner=user.id
    ).first()

    if file is None:
        return redirect(url_for("manage.files.show_all"))

    checksum = CheckSum.query.filter_by(
        id=file_id
    ).first()

    return render_template(
        "manage/files/detail.html",
        file=file,
        checksum=checksum,
        max_size=current_app.config['MAX_CONTENT_LENGTH']
    )


@bp.post("/<int:file_id>/edit")
def edit_post(file_id: int):
    if not check_login():
        return redirect(url_for("manage.session.login"))

    user = get_user_from_session()

    file = File.query.filter_by(
        id=file_id,
        owner=user.id
    ).first()

    if file is None:
        return redirect(url_for("manage.files.show_all"))

    target = request.files.get("file", None)
    if target is None:
        raise FileIsEmpty

    blob = target.stream.read()
    size = len(blob)

    if size == 0:
        raise FileIsEmpty

    if size >= current_app.config['MAX_CONTENT_LENGTH']:
        raise FileIsTooBig

    with open(join(UPLOAD_DIR, str(file.id)), mode="wb") as tmp_writer:
        tmp_writer.write(blob)

    checksum = CheckSum.query.filter_by(
        id=file.id
    ).first()

    checksum.md5 = md5(blob).hexdigest()
    checksum.sha1 = sha1(blob).hexdigest()
    checksum.sha256 = sha256(blob).hexdigest()

    db.session.commit()

    return redirect(url_for("manage.files.detail", file_id=file_id))


@bp.get("/<int:file_id>/delete")
def delete(file_id: int):
    if not check_login():
        return redirect(url_for("manage.session.login"))

    user = get_user_from_session()

    File.query.filter_by(
        id=file_id,
        owner=user.id
    ).delete()

    CheckSum.query.filter_by(
        id=file_id
    ).delete()

    db.session.commit()

    return redirect(url_for("manage.files.show_all"))
