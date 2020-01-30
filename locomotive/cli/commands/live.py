"""
CLI command for live departures and arrivals information.
"""

from typing import Any, List

import click
import dateparser
import requests
import tableformatter as tf

from ...api.gc import BoardRequest, Client
from ...models import BoardEntry, Station


def get_rows(entries: List[BoardEntry]) -> List[tuple]:
    return [
        (
            x.tofrom.name,
            f"{x.transport.label} {x.transport.number}",
            x.time,
            f"{x.delay} min",
            x.platform,
        )
        for x in entries
    ]


@click.command()
@click.argument("station")
# @click.option(
#    "--format",
#    type=click.Choice(["pretty", "json"]),
#    default="pretty",
#    help="Output format.",
# )
@click.pass_context
def live(ctx: click.Context, **args: str) -> None:
    """
    Show live departures and arrivals for a train station.

    \b
    Examples:
    locomotive live "Paris Montparnasse"
    """
    stations = ctx.obj["stations"]
    station = stations.find_or_raise(args["station"])

    client = Client(stations)

    departures = client.board_request(BoardRequest(station, "departure"))
    cols = ["Destination", "Number", "Time", "Delay", "Platform"]
    click.echo(tf.generate_table(get_rows(departures), cols))

    arrivals = client.board_request(BoardRequest(station, "arrival"))
    cols = ["Origin", "Number", "Time", "Delay", "Platform"]
    click.echo(tf.generate_table(get_rows(arrivals), cols))
