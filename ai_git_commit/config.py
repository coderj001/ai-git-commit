import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import ini


def file_exists(path: str) -> bool:
    """Check is file exists or not"""
    return Path(path).is_file()


class KnownError(Exception):
    pass


def parse_assert(name: str, condition: bool, message: str):
    if not condition:
        raise KnownError(f"Invalid config property {name}: {message}")


def openai_key(key: Optional[str]) -> str:
    if not key:
        raise KnownError(
            "Please set your OpenAI API key via `ai_git_commit config set OPENAI_KEY=<your token>"
        )
    parse_assert("OPENAI_KEY", key.startswith("sk-"), 'Must start with "sk-"')
    return key


def locale(locale: Optional[str]) -> str:
    if not locale:
        return "en"
    parse_assert(
        "locale",
        bool(re.match("^[a-z-]+$", locale)),
        "Must be a valid locale (letters and dashes/underscores). You can consult the list of codes in: https://wikipedia.org/wiki/List_of_ISO_639-1_codes",
    )
    return locale


config_parsers = {"OPENAI_KEY": openai_key, "locale": locale}

ConfigKeys = Tuple[str, ...]


class RawConfig(Dict[str, Optional[str]]):
    pass


class ValidConfig(Dict[str, str]):
    pass


def read_config_file() -> RawConfig:
    """
    The read_config_file function reads the configuration file and returns a RawConfig object.

    The config_path is set to ~/.ai-git-commit if there is no .env file in the current directory, otherwise it's set to ./env. If there isn't a config_path, an empty RawConfig object is returned. Otherwise, we open the config_path for reading and parse it with ini (which returns a dictionary). We then return that dictionary as part of our RawConfig object.

    :return: A rawconfig object.

    :doc-author: coderj001
    """
    config_path = (
        os.path.join(os.path.expanduser("~"), ".ai-git-commit")
        if not file_exists(".env")
        else os.path.join(os.getcwd(), ".env")
    )
    if not file_exists(config_path):
        return RawConfig()
    with open(config_path, "r") as f:
        raw_config = ini.parse(f.read())
        return RawConfig(raw_config)


def set_configs(key_values: Tuple[Tuple[str, str], ...]):
    """
    The set_configs function takes a list of tuples, where each tuple is a key-value pair.
    The keys are the names of config properties, and the values are strings that will be parsed
    into whatever type is appropriate for that property. The function then writes these new values
    to the user's config file.

    :param key_values:Tuple[Tuple[str: Used to Specify the type of the key_values parameter.
    :param str]: Used to Specify the type of the value.
    :param ...]: Used to Indicate that the function can take any number of arguments.
    :return: A string.

    :doc-author: coderj001
    """
    config = read_config_file()
    for key, value in key_values:
        if key not in config_parsers:
            raise KnownError(f"Invalid config property: {key}")
        parsed = config_parsers[key](value)
        config[key] = parsed
    config_path = os.path.join(os.path.expanduser("~"), ".ai-git-commit")
    with open(config_path, "w") as f:
        f.write(ini.stringify(config))


def get_config(cli_config: Optional[RawConfig] = None) -> ValidConfig:
    """
    The get_config function is responsible for reading the configuration file and
    parsing it into a dictionary of values. It also takes in an optional cli_config
    parameter, which is used to override any config values that are passed in via the CLI.
    The function returns a ValidConfig object, which is just a namedtuple containing all of the parsed config values.

    :param cli_config:Optional[RawConfig]=None: Used to Pass in the config.
    :return: A dictionary with the keys and values from the config file.

    :doc-author: coderj001
    """
    config = read_config_file()
    parsed_config = {}
    for key, parser in config_parsers.items():
        value = (
            cli_config.get(key) if cli_config and key in cli_config else config.get(key)
        )
        parsed_config[key] = parser(value)
    return ValidConfig(parsed_config)


class ICommitMessage(Dict):
    id: int
    subject: str
    body: List[str | None]
