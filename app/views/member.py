
from flask import Blueprint

from .read import bp as read_bp
from .session import bp as session_bp


bp = Blueprint(
    name="member",
    import_name="member",
    url_prefix="/member"
)
bp.register_blueprint(read_bp)
bp.register_blueprint(session_bp)


@bp.get("/<string:user_name>")
def show(user_name: str):
    return f"member.show : {user_name}"
