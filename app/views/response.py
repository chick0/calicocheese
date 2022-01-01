from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for

from app import db
from app.models import Member
from app.models import Contact
from app.models import Response
from app.utils import get_user_from_session
from app.utils import check_login
from app.discord import send

bp = Blueprint(
    name="response",
    import_name="response",
    url_prefix="/response"
)


@bp.post("/write/<int:contact_id>")
def write_post(contact_id: int):
    if not check_login():
        return redirect(url_for("manage.session.login"))

    user = get_user_from_session()

    contact = Contact.query.filter_by(
        id=contact_id
    ).first()

    if contact is not None:
        response = Response()
        response.user_id = user.id
        response.contact_id = contact_id
        response.markdown = request.form.get("editor", "")

        db.session.add(response)
        db.session.commit()

        member = Member.query.filter_by(
            id=user.id
        ).first()

        send(
            title=f"[답변등록] {contact.title}",
            description=response.markdown[:100],
            email=member.email
        )

    return redirect(url_for("contact.detail", contact_id=contact_id))


@bp.get("/delete/<int:contact_id>")
def delete(contact_id: int):
    if not check_login():
        return redirect(url_for("manage.session.login"))

    contact = Contact.query.filter_by(
        id=contact_id
    ).first()

    if contact is None:
        return redirect(url_for("contact.select"))

    response = Response.query.filter_by(
        contact_id=contact.id
    ).first()

    if response is None:
        return redirect(url_for("contact.select"))

    db.session.delete(response)
    db.session.commit()

    member = Member.query.filter_by(
        id=response.user_id
    ).first()

    send(
        title=f"[답변삭제] {contact.title}",
        description=response.markdown[:100],
        email=member.email
    )

    return redirect(url_for("contact.detail", contact_id=response.contact_id))
