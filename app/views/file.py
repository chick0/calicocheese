
from flask import Blueprint


bp = Blueprint(
    name="file",
    import_name="file",
    url_prefix="/file"
)


@bp.get("/<int:file_id>/<string:file_name>")
def get(file_id: int, file_name: str):
    return f"file.get : {file_id} / {file_name}"
