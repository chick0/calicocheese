from json import loads

from flask import session

from app.models import Member
from app.github import User
from .error import UserNotLogin


def get_user_from_session() -> User:
    session_user = session.get("session", {})
    user = session_user.get("user", None)

    if user is None:
        raise UserNotLogin

    user = User(*loads(user))
    return user


def check_login() -> bool:
    try:
        user = get_user_from_session()
    except UserNotLogin:
        return False

    member = Member.query.filter_by(
        id=user.id
    ).first()

    if member is None:
        return False

    return True
