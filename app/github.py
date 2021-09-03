from json import loads
from urllib.parse import urlencode
from urllib.request import Request
from urllib.request import urlopen
from collections import namedtuple

from .config import get_config
from .config.models import Github


SCOPE = "read:user,user:email"

AccessToken = namedtuple("AccessToken", "token type")

User = namedtuple("User", "id name email blog avatar_url html_url two_factor_authentication")


def get_github() -> Github:
    return get_config("Github")


def build_url() -> str:
    github = get_github()

    payload = urlencode({
        "client_id": github.client_id,
        "scope": SCOPE
    })

    return "https://github.com/login/oauth/authorize?" + payload


def generate_access_token(code: str) -> AccessToken:
    github = get_github()
    request = Request(
        url="https://github.com/login/oauth/access_token",
        data=urlencode({
            "client_id": github.client_id,
            "client_secret": github.client_secret,
            "code": code
        }).encode(),
        headers={
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "CalicoCheese.xyz (Github OAuth)"
        },
        method="POST"
    )

    response = urlopen(request)
    result = loads(response.read().decode())

    access_token = result.get("access_token", "")
    token_type = result.get("token_type", "bearer")

    scope = result.get("scope", "")
    if scope != SCOPE:
        return AccessToken(token="", type=token_type)

    return AccessToken(token=access_token, type=token_type)


def get_user(access_token: AccessToken) -> User:
    request = Request(
        url="https://api.github.com/user",
        headers={
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"{access_token.type} {access_token.token}",
            "User-Agent": "CalicoCheese.xyz (Github OAuth)"
        }
    )

    response = urlopen(request)
    result = loads(response.read().decode())

    name = result.get("name")
    if name is None:
        name = result.get("login")

    return User(
        id=result.get("id"),
        name=name,
        email=result.get("email"),
        blog=result.get("blog"),
        avatar_url=result.get("avatar_url"),
        html_url=result.get("html_url"),
        two_factor_authentication=result.get("two_factor_authentication"),
    )
