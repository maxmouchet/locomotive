"""
Locomotive CLI.
"""

import click

from ..models.passengers import Passengers
from ..models.stations import Stations

from .commands.passengers import passengers
from .commands.search import search


@click.group()
@click.option("--debug", is_flag=True)
@click.option(
    "--passengers-file",
    metavar="PATH",
    default=Passengers.default_path(),
    show_default=True,
)
@click.option(
    "--stations-file",
    metavar="PATH",
    default=Stations.default_path(),
    show_default=True,
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
    ctx.obj["passengers"] = Passengers(path=args["passengers_file"])
    ctx.obj["stations"] = Stations(path=args["stations_file"])


cli.add_command(passengers)
cli.add_command(search)
