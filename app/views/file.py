
from flask import Blueprint
from flask import abort
from flask import Response

from app.models import File
from app.models import CheckSum


bp = Blueprint(
    name="file",
    import_name="file",
    url_prefix="/file"
)


@bp.get("/<int:file_id>/<string:file_name>")
def get(file_id: int, file_name: str):
    return f"file.get : {file_id} / {file_name}"


@bp.get("/<int:file_id>/checksums.txt")
def checksums(file_id: int):
    file = File.query.filter_by(
        id=file_id
    ).first()

    checksum = CheckSum.query.filter_by(
        id=file_id
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
