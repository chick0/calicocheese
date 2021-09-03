
from app.config import get_config
from app.config.models import Database


def get_url() -> str:
    def t() -> Database:
        return get_config("Database")

    database = t()
    if "#" in [database.user, database.password, database.host, database.port, database.database]:
        return "#"

    return f"mysql://{database.user}:{database.password}@{database.host}:{database.port}/{database.database}"
