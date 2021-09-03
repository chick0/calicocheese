
from flask import Blueprint


bp = Blueprint(
    name="file",
    import_name="file",
    url_prefix="/file"
)


@bp.get("/<int:file_id>")
def get(file_id: int):
    return f"file.get : {file_id}"
