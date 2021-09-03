from json import loads
from urllib.request import Request
from urllib.request import urlopen
from collections import namedtuple

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.database import get_url
from app.models import Member


User = namedtuple("User", "id name email blog avatar_url html_url two_factor_authentication is_admin bio")
Database = namedtuple("Database", "host port user password database")


def main():
    login = input("GitHub.com login id : ")
    request = Request(
        url=f"https://api.github.com/users/{login}",
        headers={
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "CalicoCheese.xyz (Github API)"
        }
    )

    response = urlopen(request)
    result = loads(response.read().decode())

    name = result.get("name")
    if name is None:
        name = result.get("login")

    print("\n".join([
        "="*30,
        f"ID : {result.get('id')}",
        f"Name : {name}",
        f"Github URL : {result.get('html_url')}",
        f"Bio : {result.get('bio')}",
        "=" * 30,
    ]))

    if input("are you sure? [Y/n] : ").lower() != "y":
        exit(-1)

    is_admin = True if input("is this user an admin? [Y/n] : ").lower() == "y" else False

    user = User(
        id=result.get("id"),
        name=name,
        email="",
        blog=result.get("blog"),
        avatar_url=result.get("avatar_url"),
        html_url=result.get("html_url"),
        two_factor_authentication=False,
        is_admin=is_admin,
        bio=result.get("bio") if result.get("bio") is not None else ""
    )

    engine = create_engine(get_url())
    session_base = sessionmaker(bind=engine)

    session = session_base()
    member = session.query(Member).filter_by(
        id=user.id
    ).first()

    if member is not None:
        print("this user is already registered!")
        exit(-2)

    del member

    member = Member()
    member.id = user.id
    member.name = user.name
    member.email = user.email
    member.blog = user.blog
    member.avatar_url = user.avatar_url
    member.html_url = user.html_url
    member.two_factor_authentication = user.two_factor_authentication
    member.is_admin = user.is_admin
    member.bio = user.bio

    session.add(member)
    session.commit()

    print("user added!")
    exit(0)


if __name__ == "__main__":
    main()
