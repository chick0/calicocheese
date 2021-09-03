from os.path import join
from configparser import ConfigParser

from . import models
from app import CONFIG_DIR


def test_config() -> None:
    for section in models.__all__:
        filename = section.lower() + ".ini"

        tmp = ConfigParser()
        tmp.read(join(CONFIG_DIR, filename), encoding="utf-8")

        if not tmp.has_section(section):
            reset = ConfigParser()
            reset.add_section(section)

            for field in getattr(getattr(models, section), "_fields"):
                reset.set(
                    section=section,
                    option=field,
                    value="#"
                )

            with open(join(CONFIG_DIR, filename), mode="w", encoding="utf-8") as configInit:
                reset.write(configInit)


def get_config(model_name: str):
    if model_name not in models.__all__:
        raise KeyError("FailToLoadConfig: unregistered config model")

    filename = model_name.lower() + ".ini"

    config = ConfigParser()
    config.read(join(CONFIG_DIR, filename), encoding="utf-8")

    import_result = []
    for field in getattr(getattr(models, model_name), "_fields"):
        import_result.append(
            config.get(
                section=model_name,
                option=field,
                fallback="#"
            )
        )

    return getattr(models, model_name)(*import_result)


def update_config(model_name: str, model: object) -> bool:
    if model_name not in models.__all__:
        raise KeyError("FailToLoadConfig: unregistered config model")

    filename = model_name.lower() + ".ini"

    config = ConfigParser()
    config.add_section(model_name)

    for field in getattr(getattr(models, model_name), "_fields"):
        config.set(
            section=model_name,
            option=field,
            value=getattr(model, field)
        )

    with open(join(CONFIG_DIR, filename), mode="w", encoding="utf-8") as configUpdate:
        config.write(configUpdate)

    return True
