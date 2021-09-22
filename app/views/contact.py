
from flask import Blueprint
from flask import abort
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template

from app import db
from app.models import Contact
from app.utils import check_login
from app.utils import get_user_from_session
from app.error import UserNotLogin


bp = Blueprint(
    name="contact",
    import_name="contact",
    url_prefix="/contact"
)


@bp.get("")
def select():
    try:
        user = get_user_from_session()
    except UserNotLogin:
        return redirect(url_for("manage.session.login"))

    if check_login():
        contacts = Contact.query.order_by(
            Contact.id.desc()
        ).paginate(1)
    else:
        contacts = Contact.query.filter_by(
            user_id=user.id
        ).order_by(
            Contact.id.desc()
        ).paginate(1)

    return render_template(
        "contact/select.html",
        user=user,
        email_is_none=user.email is None,
        contacts=contacts
    )


@bp.get("/write")
def write():
    return render_template(
        "contact/write.html"
    )


@bp.post("/write")
def write_post():
    try:
        user = get_user_from_session()
    except UserNotLogin:
        return redirect(url_for("manage.session.login"))

    contact = Contact()
    contact.user_id = user.id
    contact.email = user.email
    contact.title = request.form.get("title", "제목 없음")[:60]
    contact.markdown = request.form.get("editor", "")[:20000]

    db.session.add(contact)
    db.session.commit()

    return redirect(url_for("contact.detail", contact_id=contact.id))


@bp.get("/detail/<int:contact_id>")
def detail(contact_id: int):
    try:
        user = get_user_from_session()
    except UserNotLogin:
        return redirect(url_for("manage.session.login"))

    contact = Contact.query.filter_by(
        id=contact_id
    ).first()

    if contact is None:
        return abort(404)

    if contact.user_id != user.id:
        if not check_login():
            return abort(403)

    return render_template(
        "contact/detail.html",
        contact=contact
    )


@bp.get("/delete/<int:contact_id>")
def delete(contact_id: int):
    if check_login():
        Contact.query.filter_by(
            id=contact_id
        ).delete()

        db.session.commit()

    return redirect(url_for("contact.select"))
