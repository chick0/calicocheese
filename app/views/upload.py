
from flask import Blueprint


bp = Blueprint(
    name="upload",
    import_name="upload",
    url_prefix="/upload"
)


@bp.get("/form")
def form():
    return "upload.form"


@bp.post("/form")
def form_post():
    return "upload.form_post"
