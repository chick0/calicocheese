from flask import Blueprint
from flask import request
from flask import jsonify

from app.models import Link

bp = Blueprint(
    name="api",
    import_name="api",
    url_prefix="/api",
)


@bp.get("/link")
def link():
    try:
        project_id = int(request.args.get("id", ""))
    except ValueError:
        return jsonify([])

    links = Link.query.filter_by(
        project_id=project_id
    ).limit(10).all()

    result = []

    for _ in links:
        result.append({
            "color": _.color,
            "text": _.text,
            "url": _.url,
        })

    return jsonify(result)
