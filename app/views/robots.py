
from flask import Blueprint
from flask import Response
from flask import send_file


bp = Blueprint(
    name="robots",
    import_name="robots",
    url_prefix="/",
)


@bp.get("robots.txt")
def robots():
    return Response(
        response="\n".join([
            "User-agent: *",
            "Allow: /$",
            "Allow: /static",
            "Allow: /project",
            "Disallow: /file",
            "Disallow: /manage",
        ]),
        mimetype="text/plain"
    )


@bp.route("/favicon.ico")
def favicon():
    return send_file(
        "static/favicon.ico",
        mimetype="image/x-icon"
    )
