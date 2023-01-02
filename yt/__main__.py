import click

from yt.cli.commands import commands

# noinspection PyTypeChecker
cli = click.CommandCollection(sources=[commands])

if __name__ == '__main__':
    cli()
