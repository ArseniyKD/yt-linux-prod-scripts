import click

from yt.cli.options import verbose_option


@click.group()
def commands() -> None:
    """Entry point"""
    pass


@commands.command()
@verbose_option
def sample_command(verbose: bool) -> None:
    """
    This is a sample command
    :param verbose: Whether the command should be in verbose mode
    :return: None
    """
    print('This is a sample command...')
