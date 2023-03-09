from click.testing import CliRunner
from ai_git_commit import main


def test_main() -> None:
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0


def test_example() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["example"])
    assert result.exit_code == 0
