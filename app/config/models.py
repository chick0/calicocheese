from collections import namedtuple


Database = namedtuple(
    "Database",
    "host port user password database"
)


Github = namedtuple(
    "Github",
    "client_id client_secret"
)


##############################################
del namedtuple
__all__ = [model for model in dir() if not model.startswith("__")]
