from typing import List

import click
import tableformatter as tf
from colored import bg

from ...api.gc import BoardRequest, Client
from ...models import BoardEntry


def get_rows(entries: List[BoardEntry]) -> List[tuple]:
    return [
        (
            x.tofrom.name,
            f"{x.transport.label} {x.transport.number}",
            x.time.strftime("%H:%M"),
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
@click.option("--color/--no-color", default=True)
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

    dep_gs = None
    arr_gs = None
    if args["color"]:
        dep_gs = tf.AlternatingRowGrid(bg(25), bg(18))
        arr_gs = tf.AlternatingRowGrid(bg(34), bg(28))

    departures = client.board_request(BoardRequest(station, "departure"))
    cols = ["Destination", "Number", "Time", "Delay", "Platform"]
    click.echo(tf.generate_table(get_rows(departures), cols, grid_style=dep_gs))

    arrivals = client.board_request(BoardRequest(station, "arrival"))
    cols = ["Origin", "Number", "Time", "Delay", "Platform"]
    click.echo(tf.generate_table(get_rows(arrivals), cols, grid_style=arr_gs))
