from io import BytesIO
from os.path import join

from flask import Blueprint
from flask import abort
from flask import Response
from flask import send_file

from app import UPLOAD_DIR
from app.models import File
from app.models import CheckSum


bp = Blueprint(
    name="file",
    import_name="file",
    url_prefix="/file"
)


@bp.get("/<int:file_id>/<string:file_name>")
def get(file_id: int, file_name: str):
    try:
        with open(join(UPLOAD_DIR, str(file_id)), mode="rb") as tmp_reader:
            blob = tmp_reader.read()
    except FileNotFoundError:
        return abort(404)

    file = File.query.filter_by(
        id=file_id
    ).first()

    if file is None:
        return abort(404)

    return send_file(
        BytesIO(blob),
        mimetype="application/octet-stream",
        as_attachment=True,
        attachment_filename=file.name
    )


@bp.get("/<int:file_id>/checksums.txt")
def checksums(file_id: int):
    file = File.query.filter_by(
        id=file_id
    ).first()

    if file is None:
        return abort(404)

    checksum = CheckSum.query.filter_by(
        id=file.id
    ).first()

    return Response(
        response="\n".join([
            file.name,
            f"md5sum {checksum.md5}",
            f"sha1sum {checksum.sha1}",
            f"sha256sum {checksum.sha256}",
        ]),
        mimetype="text/plain"
    )
