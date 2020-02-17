import datetime as dt
from typing import Any, Union

import click
from requests.exceptions import HTTPError  # pylint: disable=no-name-in-module

from ...api.oui_v3 import Client
from ...api.requests import TravelRequest
from ...models import Passenger
from ..ext import DateParseParamType
from ..formatters import JSONFormatter, PrettyFormatter


@click.command()
@click.argument("origin")
@click.argument("destination")
@click.option(
    "--date",
    type=DateParseParamType(),
    default="now",
    show_default=True,
    help="Date (e.g 2019-06-01, 1st of June, 1er Juin ...), France timezone.",
)
@click.option(
    "--class",
    "travel_class",
    type=click.Choice(["first", "second"]),
    default="second",
    show_default=True,
    help="Travel class.",
)
@click.option(
    "--format",
    type=click.Choice(["pretty", "json"]),
    default="pretty",
    show_default=True,
    help="Output format.",
)
@click.pass_context
def search(ctx: click.Context, **args: Any) -> None:
    """
    Search for trains.

    Origin and destination can be city names (Paris),
    train station names (Paris Montparnasse),
    or train station codes (FRPMO).

    \b
    Examples:
    locomotive search Brest Paris
    locomotive search Brest Paris --class second --date 2019-06-01
    """
    stations = ctx.obj["stations"]
    client = Client(stations)

    date: dt.datetime = args["date"]
    if date is None:
        raise click.UsageError("Cannot parse date.")
    # TODO: date.start_of("day")

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

    formatter: Union[PrettyFormatter, JSONFormatter] = PrettyFormatter()
    if args["format"] == "json":
        formatter = JSONFormatter()

    try:
        req = TravelRequest(
            departure_station=departure_station,
            arrival_station=arrival_station,
            passengers=[passenger],
            date=date,
            travel_class=args["travel_class"],
        )
        it = client.travel_request_iter(req)
        formatter.print(it, fn=click.echo)
    except HTTPError as exception:
        click.echo(exception.response.content, err=True)
        raise exception
