"""
Locomotive CLI.
"""

import click

from ..config import Config

from .config import config
from .search import search


@click.group()
@click.option("--debug", is_flag=True)
@click.option(
    "--config-file", metavar="PATH", default=Config.default_path(), show_default=True
)
@click.pass_context
def cli(ctx, **args):
    """
    🚆 Search SNCF journeys from your terminal.

    \b
    Examples:
    sncf-cli search Brest Paris
    """
    ctx.ensure_object(dict)
    # Load global configuration object
    ctx.obj["config"] = Config(path=args["config_file"])


cli.add_command(config)
cli.add_command(search)
