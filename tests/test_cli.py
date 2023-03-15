from unittest.mock import patch

from click.testing import CliRunner
from dotenv import load_dotenv

from ai_git_commit import get, main, set


def test_main() -> None:
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0


def test_example() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["example"])
    assert result.exit_code == 0


def test_set_valid_key() -> None:
    runner = CliRunner()
    with patch("ai_git_commit.set_configs") as mock_set_configs:
        result = runner.invoke(set, ["OPENAI_KEY=sk-abc123"])
        assert result.exit_code == 0
        mock_set_configs.assert_called_once_with(
            key_values=(("OPENAI_KEY", "sk-abc123"),)
        )


def test_set_invalid_key() -> None:
    runner = CliRunner()
    with patch("ai_git_commit.set_configs") as mock_set_configs:
        result = runner.invoke(set, ["INVALID_KEY=abc123"])
        assert result.exit_code == 2
        assert "Invalid key format" in result.output
        mock_set_configs.assert_not_called()


def test_get_valid_key() -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open(".env", "w") as f:
            f.write("OPENAI_KEY=sk-abc123")
        load_dotenv(".env")
        result = runner.invoke(get, ["OPENAI_KEY"])
        assert result.exit_code == 0
        assert result.output == "sk-abc123\n"


def test_get_invalid_key() -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open(".env", "w") as f:
            f.write("OPENAI_KEY=sk-abc123")
        load_dotenv(".env")
        result = runner.invoke(get, ["INVALID_KEY"])
        assert result.exit_code == 2
        assert "Invalid key format." in result.output
