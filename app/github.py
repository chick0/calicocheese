from urllib.parse import urlencode

from .config import get_config
from .config.models import Github


def get_github() -> Github:
    return get_config("Github")


def build_url() -> str:
    github = get_github()

    payload = urlencode({
        "client_id": github.client_id,
        "scope": github.scope
    })

    return "https://github.com/login/oauth/authorize?" + payload
