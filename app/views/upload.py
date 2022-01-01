from os.path import join
from hashlib import md5
from hashlib import sha1
from hashlib import sha256

from flask import Blueprint
from flask import current_app
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from werkzeug.utils import secure_filename

from app import UPLOAD_DIR
from app import db
from app.models import File
from app.models import CheckSum
from app.utils import check_login
from app.utils import get_user_from_session
from app.error import FileIsEmpty
from app.error import FileIsTooBig

bp = Blueprint(
    name="upload",
    import_name="upload",
    url_prefix="/upload"
)


@bp.get("")
def form():
    if not check_login():
        return redirect(url_for("manage.session.login"))

    return render_template(
        "upload/form.html",
        max_size=current_app.config['MAX_CONTENT_LENGTH']
    )


@bp.post("")
def form_post():
    if not check_login():
        return redirect(url_for("manage.session.login"))

    user = get_user_from_session()

    target = request.files.get("file", None)
    if target is None:
        raise FileIsEmpty

    blob = target.stream.read()
    size = len(blob)

    if size == 0:
        raise FileIsEmpty

    if size >= current_app.config['MAX_CONTENT_LENGTH']:
        raise FileIsTooBig

    file = File()
    file.owner = user.id
    file.name = secure_filename(target.filename)

    db.session.add(file)
    db.session.commit()

    with open(join(UPLOAD_DIR, str(file.id)), mode="wb") as tmp_writer:
        tmp_writer.write(blob)

    checksum = CheckSum()
    checksum.id = file.id
    checksum.md5 = md5(blob).hexdigest()
    checksum.sha1 = sha1(blob).hexdigest()
    checksum.sha256 = sha256(blob).hexdigest()

    db.session.add(checksum)
    db.session.commit()

    return redirect(url_for("manage.files.detail", file_id=file.id))
