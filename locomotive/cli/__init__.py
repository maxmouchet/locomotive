"""
Locomotive CLI.
"""

import click

from .search import search


@click.group()
def cli():
    """
    🚆 Search SNCF journeys from your terminal.

    \b
    Examples:
    sncf-cli search FRBES FRPAR
    """


cli.add_command(search)
