import os

import pytest

from ai_git_commit.config import (
    KnownError,
    get_config,
    locale,
    openai_key,
    read_config_file,
    set_configs,
)


@pytest.fixture
def cleanup_config():
    yield
    config_path = os.path.join(os.path.expanduser("~"), ".ai-git-commit")
    if os.path.exists(config_path):
        os.remove(config_path)


def test_openai_key_valid():
    key = "sk-abc123"
    assert openai_key(key) == key


def test_openai_key_invalid():
    key = "abc123"
    with pytest.raises(KnownError, match=r'Must start with "sk-"'):
        openai_key(key)


def test_locale_valid():
    locale_str = "en-"
    assert locale(locale_str) == locale_str


def test_locale_invalid():
    locale_str = "en-US"
    with pytest.raises(KnownError, match=r"Must be a valid locale"):
        locale(locale_str)


def test_read_config_file(cleanup_config):
    assert read_config_file() == {}

    config_path = os.path.join(os.path.expanduser("~"), ".ai-git-commit")
    with open(config_path, "w") as f:
        f.write("OPENAI_KEY=sk-abc123\n")

    expected = {"OPENAI_KEY": "sk-abc123"}
    assert read_config_file() == expected


def test_set_configs(cleanup_config):
    with pytest.raises(KnownError, match=r"Invalid config property: invalid_key"):
        set_configs((("invalid_key", "abc123"),))

    config_path = os.path.join(os.path.expanduser("~"), ".ai-git-commit")
    with open(config_path, "w") as f:
        f.write("OPENAI_KEY=sk-abc123\n")

    set_configs((("OPENAI_KEY", "sk-xyz456"),))

    expected = {"OPENAI_KEY": "sk-xyz456"}
    with open(config_path, "r") as f:
        assert f.read() == "OPENAI_KEY = sk-xyz456\n"


def test_get_config(cleanup_config):
    with pytest.raises(
        KnownError,
        match=r"Please set your OpenAI API key via `ai_git_commit config set OPENAI_KEY=<your token>",
    ):
        get_config()

    config_path = os.path.join(os.path.expanduser("~"), ".ai-git-commit")
    with open(config_path, "w") as f:
        f.write("OPENAI_KEY=sk-abc123\n")

    expected = {"OPENAI_KEY": "sk-abc123", "locale": "en"}
    assert get_config() == expected

    expected = {"OPENAI_KEY": "sk-xyz456", "locale": "en"}
    cli_config = {"OPENAI_KEY": "sk-xyz456"}
    assert get_config(cli_config) == expected
