"""
CLI command for searching train journeys.
"""

import click
import dateparser
from requests.exceptions import HTTPError

from ...api.oui_v2 import Client
from ..formatters import Formatter, JSONFormatter, PrettyFormatter


@click.command()
@click.argument("origin")
@click.argument("destination")
@click.option(
    "--date", default="now", help="Date (e.g 2019-06-01, 1st of June, 1er Juin ...)."
)
@click.option(
    "--class",
    "travel_class",
    type=click.Choice(["first", "second"]),
    default="second",
    help="Travel class.",
)
@click.option(
    "--passenger", metavar="NAME", help="Passenger profile (see `sncf-cli passengers`)."
)
@click.option(
    "--format",
    type=click.Choice(["pretty", "json"]),
    default="pretty",
    help="Output format.",
)
@click.pass_context
def search(ctx: click.Context, **args: str) -> None:
    """
    Search for trains.

    Origin and destination can be city names (Paris),
    train station names (Paris Montparnasse),
    or train station codes (FRPMO).

    \b
    Examples:
    sncf-cli search Brest Paris
    sncf-cli search Brest Paris --class second --date 2019-06-01
    """
    passengers = ctx.obj["passengers"]
    stations = ctx.obj["stations"]
    client = Client(stations)

    date = dateparser.parse(args["date"])
    if date is None:
        raise click.UsageError("Cannot parse date.")

    # Hack: if set to 0 (midnight), the API
    # returns results for the day before.
    date = date.replace(hour=2)

    origin_station = stations.find_or_raise(args["origin"])
    destination_station = stations.find_or_raise(args["destination"])

    if args["passenger"]:
        passenger = passengers.find_or_raise(args["passenger"])
    else:
        passenger = passengers.default()

    click.echo(
        "{} → {} ({:.0f}km) on {}".format(
            origin_station.name,
            destination_station.name,
            origin_station.distance_to(destination_station),
            date.strftime("%b %d %Y"),
        ),
        err=True,
    )

    click.echo("{} ({} years old)\n".format(passenger.name, passenger.age), err=True)

    try:
        res = client.travel_request(
            origin_station, destination_station, [passenger], date, args["travel_class"]
        )
    except HTTPError as exception:
        click.echo(exception.response.content, err=True)
        raise exception

    # TODO: Option to print raw api response
    if args["format"] == "pretty":
        formatter: Formatter = PrettyFormatter()
    else:
        formatter = JSONFormatter()

    # We use click.echo because:
    # > Click’s echo() function will automatically strip ANSI color codes if the stream is not
    # > connected to a terminal.
    # > the echo() function will transparently connect to the terminal on Windows and translate
    # > ANSI codes to terminal API calls.
    # > This means that colors will work on Windows the same way they do on other operating systems.
    # https://click.palletsprojects.com/en/7.x/utils/#ansi-colors
    click.echo(formatter.get_str(res))
