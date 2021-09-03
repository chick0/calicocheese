
from sqlalchemy import func

from app import db


class Member(db.Model):
    id = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
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
