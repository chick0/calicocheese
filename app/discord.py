from json import dumps
from urllib.request import Request
from urllib.request import urlopen

from app.config import get_config
from app.config.models import Discord


def get_discord() -> Discord:
    return get_config("Discord")


def send(
        title: str,
        description: str or None = None,
        url: str or None = None,
        user_id: int or None = None,
        email: str or None = None,
        color: int = 16763981,
        username: str = "Calico Cheese",
        avatar_url: str = "https://avatars.githubusercontent.com/u/73421520?s=200&v=4",
):
    discord = get_discord()

    payload = {
        "username": username,
        "avatar_url": avatar_url,
        "embeds": [
            {
                "title": title,
                "fields": [],
                "color": color,
                "image": {
                    "url": None
                },
            }
        ],
        "files": [],
    }

    if url is not None and isinstance(url, str):
        payload['embeds'][0].update({
            "url": url
        })

    if user_id is not None and isinstance(user_id, int):
        payload['embeds'][0]['fields'].append(
            {
                "name": "유저 아이디",
                "value": f"{user_id}",
                "inline": False,
            }
        )

    if email is not None and isinstance(email, str):
        payload['embeds'][0]['fields'].append(
            {
                "name": "이메일 주소",
                "value": email.strip(),
                "inline": False,
            }
        )

    if description is not None and isinstance(description, str):
        payload['embeds'][0]['fields'].append(
            {
                "name": "미리보기",
                "value": description[:200].strip(),
                "inline": False,
            }
        )

    request = Request(
        url=discord.webhook_url,
        method="POST",
        data=dumps(payload).encode("utf-8")
    )

    request.add_header("User-Agent", "CalicoCheese")
    request.add_header("Content-Type", "application/json")
    urlopen(request)
