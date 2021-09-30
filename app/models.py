
from sqlalchemy import func

from app import db


class Member(db.Model):
    index = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    id = db.Column(
        db.Integer,
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(39),
        nullable=False
    )

    email = db.Column(
        db.String(255),
        nullable=False
    )

    blog = db.Column(
        db.String(255),
        nullable=False
    )

    avatar_url = db.Column(
        db.String(60),
        nullable=False
    )

    html_url = db.Column(
        db.String(60),
        nullable=False
    )

    two_factor_authentication = db.Column(
        db.Boolean,
        nullable=False
    )

    is_admin = db.Column(
        db.Boolean,
        nullable=False
    )

    bio = db.Column(
        db.Text,
        nullable=False
    )

    auto_update = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    def __repr__(self):
        return f"<Member id={self.id}, name={self.name!r}>"


class File(db.Model):
    id = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    owner = db.Column(
        db.Integer,
        nullable=False
    )

    name = db.Column(
        db.String(256),
        nullable=False
    )

    date = db.Column(
        db.DateTime,
        nullable=False,
        default=func.now()
    )

    def __repr__(self):
        return f"<File id={self.id}, name={self.name!r}>"


class CheckSum(db.Model):
    id = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    md5 = db.Column(
        db.String(32),
        nullable=False
    )

    sha1 = db.Column(
        db.String(40),
        nullable=False
    )

    sha256 = db.Column(
        db.String(64),
        nullable=False
    )

    def __repr__(self):
        return f"<CheckSum id={self.id}>"


class Project(db.Model):
    id = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    owner = db.Column(
        db.Integer,
        nullable=False
    )

    title = db.Column(
        db.String(60),
        nullable=False
    )

    html = db.Column(
        db.Text,
        nullable=False
    )

    public = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    def __repr__(self):
        return f"<Project id={self.id}, owner={self.owner}>"


class Link(db.Model):
    id = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    project_id = db.Column(
        db.Integer,
        nullable=False
    )

    color = db.Column(
        db.String(60),
        nullable=False
    )

    text = db.Column(
        db.String(100),
        nullable=False
    )

    url = db.Column(
        db.String(256),
        nullable=False
    )

    def __repr__(self):
        return f"<Link id={self.id}, project_id={self.project_id}>"


class Contact(db.Model):
    id = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        nullable=False
    )

    email = db.Column(
        db.String(255)
    )

    title = db.Column(
        db.String(60),
        nullable=False
    )

    markdown = db.Column(
        db.Text,
        nullable=False
    )

    date = db.Column(
        db.DateTime,
        nullable=False,
        default=func.now()
    )

    def __repr__(self):
        return f"<Contact id={self.id}, user_id={self.user_id}>"


class Response(db.Model):
    id = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        nullable=False
    )

    contact_id = db.Column(
        db.Integer,
        unique=True,
        nullable=False
    )

    markdown = db.Column(
        db.Text,
        nullable=False
    )

    date = db.Column(
        db.DateTime,
        nullable=False,
        default=func.now()
    )

    def __repr__(self):
        return f"<Response id={self.id}, contact_id={self.contact_id}>"


class Memo(db.Model):
    id = db.Column(
        db.String(36),
        unique=True,
        primary_key=True,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        nullable=False
    )

    title = db.Column(
        db.String(60)
    )

    html = db.Column(
        db.Text,
        nullable=False
    )

    last_edit = db.Column(
        db.DateTime,
        nullable=False,
        default=func.now()
    )

    deleted = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    public = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    group_id = db.Column(
        db.String(36),
        nullable=False
    )

    def __repr__(self):
        return f"<Memo id={self.id}, user_id={self.user_id}>"


class MemoGroup(db.Model):
    id = db.Column(
        db.String(36),
        unique=True,
        primary_key=True,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        nullable=False
    )

    name = db.Column(
        db.String(120),
        nullable=False
    )

    public = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    def __repr__(self):
        return f"<MemoGroup id={self.id}, user_id={self.user_id}>"
