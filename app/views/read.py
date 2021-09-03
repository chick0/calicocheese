
from flask import Blueprint


bp = Blueprint(
    name="read",
    import_name="read",
    url_prefix="/read"
)


@bp.get("/<int:project_id>")
def project(project_id):
    return f"member.read.project : {project_id}"
