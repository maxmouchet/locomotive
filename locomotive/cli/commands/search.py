"""
CLI command for searching train journeys.
"""

import click
import dateparser
from requests.exceptions import HTTPError

from ...api.abstract import TravelRequest
from ...api.oui_v3 import Client
from ...models import Passenger
from ..formatters import Formatter, JSONFormatter, PrettyFormatter

# We use click.echo because:
# > Click’s echo() function will automatically strip ANSI color codes if the stream is not
# > connected to a terminal.
# > the echo() function will transparently connect to the terminal on Windows and translate
# > ANSI codes to terminal API calls.
# > This means that colors will work on Windows the same way they do on other operating systems.
# https://click.palletsprojects.com/en/7.x/utils/#ansi-colors


@click.command()
@click.argument("origin")
@click.argument("destination")
@click.option(
    "--date",
    default="now",
    help="Date (e.g 2019-06-01, 1st of June, 1er Juin ...), France timezone.",
)
@click.option(
    "--class",
    "travel_class",
    type=click.Choice(["first", "second"]),
    default="second",
    help="Travel class.",
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
    stations = ctx.obj["stations"]
    client = Client(stations)

    date = dateparser.parse(
        args["date"],
        settings={"TIMEZONE": "Europe/Paris", "RETURN_AS_TIMEZONE_AWARE": True},
    )
    if date is None:
        raise click.UsageError("Cannot parse date.")

    # Hack: if set to 0 (midnight), the API
    # returns results for the day before.
    if date.hour < 2:
        date = date.replace(hour=2)

    departure_station = stations.find_or_raise(args["origin"])
    arrival_station = stations.find_or_raise(args["destination"])
    passenger = Passenger.dummy()

    click.echo(
        "{} → {} ({:.0f}km) on {}".format(
            departure_station.name,
            arrival_station.name,
            departure_station.distance_to(arrival_station),
            date.strftime("%b %d %Y at %H:%M"),
        ),
        err=True,
    )

    click.echo("{} ({} years old)\n".format(passenger.name, passenger.age), err=True)

    # TODO: Option to print raw api response
    if args["format"] == "pretty":
        formatter: Formatter = PrettyFormatter()
    else:
        formatter = JSONFormatter()

    click.echo(formatter.start_str())

    try:
        req = TravelRequest(
            departure_station=departure_station,
            arrival_station=arrival_station,
            passengers=[passenger],
            date=date,
            travel_class=args["travel_class"],
        )
        it = client.travel_request_iter(req)
        for journey in it:
            click.echo(formatter.incr_str(journey))
    except HTTPError as exception:
        click.echo(exception.response.content, err=True)
        raise exception

    click.echo(formatter.end_str())
