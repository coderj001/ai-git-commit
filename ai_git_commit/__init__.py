import os

import click

from ai_git_commit.config import KnownError, config_parsers, get_config, set_configs


@click.group(invoke_without_command=True)
@click.option("--debug/--no-debug")
@click.pass_context
def main(ctx: click.Context, debug: bool) -> None:
    """
    main command
    """
    ctx.obj = {"debug": debug}

    if ctx.invoked_subcommand is None:
        click.echo("Hello World!")


@main.command()
@click.pass_obj
def example(ctx: dict) -> None:
    """
    Example subcommand
    """
    click.echo("Example subcommand")


@main.group()
def config():
    """
    Configure Local Variables
    """


@config.command()
@click.argument("key_value")
@click.pass_obj
def set(ctx: dict, key_value: str) -> None:
    """
    Set configure for local variable
    """
    key, value = key_value.split("=")
    if key not in config_parsers:
        raise click.BadParameter(
            "Invalid key format. Example Should be OPENAI_KEY=<your token>"
        )
    parsed = config_parsers[key](value)
    set_configs(key_values=((key, parsed),))


@config.command()
@click.argument("key")
@click.pass_obj
def get(ctx: dict, key: str) -> None:
    """
    Get configure for local variable
    """
    if key not in config_parsers.keys():
        raise click.BadParameter("Invalid key format. Example Should be OPENAI_KEY")
    value = get_config().get(key)
    click.echo(value)


if __name__ == "__main__":
    main(obj={})
