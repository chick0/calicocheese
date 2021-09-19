from json import dumps
from json import loads
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.database import get_url
from app.models import Member
from app.models import File
from app.models import CheckSum
from app.models import Project
from app.models import Link


def export():
    engine = create_engine(get_url())
    session_base = sessionmaker(bind=engine)

    session = session_base()
    from_database = dict()

    from_database['member'] = [
        {
            "index": x.index,
            "id": x.id,
            "name": x.name,
            "email": x.email,
            "blog": x.blog,
            "avatar_url": x.avatar_url,
            "html_url": x.html_url,
            "two_factor_authentication": x.two_factor_authentication,
            "is_admin": x.is_admin,
            "bio": x.bio,
            "auto_update": x.auto_update,
        } for x in session.query(Member).all()
    ]

    from_database['file'] = [
        {
            "id": x.id,
            "owner": x.owner,
            "name": x.name,
            "date": int(x.date.timestamp()),
        } for x in session.query(File).all()
    ]

    from_database['checksum'] = [
        {
            "id": x.id,
            "md5": x.md5,
            "sha1": x.sha1,
            "sha256": x.sha256,
        } for x in session.query(CheckSum).all()
    ]

    from_database['project'] = [
        {
            "id": x.id,
            "owner": x.owner,
            "title": x.title,
            "html": x.html,
            "public": x.public,
        } for x in session.query(Project).all()
    ]

    from_database['link'] = [
        {
            "id": x.id,
            "project_id": x.project_id,
            "color": x.color,
            "text": x.text,
            "url": x.url,
        } for x in session.query(Link).all()
    ]

    from_database = dumps(from_database, indent=4)
    with open("database.json", mode="w", encoding="utf-8") as database_writer:
        database_writer.write(from_database)


def import_():
    filename = input("select database json filename : ")
    with open(filename, mode="r", encoding="utf-8") as json_reader:
        to_database = loads(json_reader.read())

    engine = create_engine(get_url())
    session_base = sessionmaker(bind=engine)

    session = session_base()

    for member in to_database['member']:
        _ = Member()
        _.index = member.get("index")
        _.id = member.get("id")
        _.name = member.get("name")
        _.email = member.get("email")
        _.blog = member.get("blog")
        _.avatar_url = member.get("avatar_url")
        _.html_url = member.get("html_url")
        _.two_factor_authentication = member.get("two_factor_authentication")
        _.is_admin = member.get("is_admin")
        _.bio = member.get("bio")
        _.auto_update = member.get("auto_update")

        session.add(_)

    for file in to_database['file']:
        _ = File()
        _.id = file.get("id")
        _.owner = file.get("owner")
        _.name = file.get("name")
        _.date = datetime.fromtimestamp(file.get("date"))

        session.add(_)

    for checksum in to_database['checksum']:
        _ = CheckSum()
        _.id = checksum.get("id")
        _.md5 = checksum.get("md5")
        _.sha1 = checksum.get("sha1")
        _.sha256 = checksum.get("sha256")

        session.add(_)

    for project in to_database['project']:
        _ = Project()
        _.id = project.get("id")
        _.owner = project.get("owner")
        _.title = project.get("title")
        _.html = project.get("html")
        _.public = project.get("public")

        session.add(_)

    for link in to_database['link']:
        _ = Link()
        _.id = link.get("id")
        _.project_id = link.get("project_id")
        _.color = link.get("color")
        _.text = link.get("text")
        _.url = link.get("url")

        session.add(_)

    try:
        session.commit()
    except (IntegrityError, Exception):
        print("Fail to Import database!!!")


if __name__ == "__main__":
    print("Export or Import?")
    print("Yes to Export. No to Import.")
    work = input("(Y/N) : ").lower()

    if work == "y" or work == "yes":
        export()
    elif work == "n" or work == "no":
        import_()
    else:
        print("meowed")
