import click
import dateparser

from ...api.oui_v1 import Client
from ..formatters import PrettyFormatter, RawFormatter


class PassengerNotFoundException(click.ClickException):
    def __init__(self, passenger):
        super().__init__("Passenger {} not found".format(string))


class StationNotFoundException(click.ClickException):
    def __init__(self, station):
        super().__init__("Train station for {} not found".format(station))


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
    type=click.Choice(["pretty", "raw"]),
    default="pretty",
    help="Output format.",
)
@click.pass_context
def search(ctx, **args):
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
    date = dateparser.parse(args["date"])

    passengers = ctx.obj["passengers"]
    stations = ctx.obj["stations"]

    origin_station = stations.find(args["origin"])
    destination_station = stations.find(args["destination"])

    if origin_station is None:
        raise StationNotFoundException(args["origin"])

    if destination_station is None:
        raise StationNotFoundException(args["destination"])

    if args["passenger"]:
        passenger = passengers.find(args["passenger"])
        if passenger is None:
            raise PassengerNotFoundException(args["passenger"])
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

    client = Client()
    res = client.simple_request(
        passenger.age, origin_station, destination_station, date, args["travel_class"]
    )

    if args["format"] == "pretty":
        formatter = PrettyFormatter(stations=stations)
    else:
        formatter = RawFormatter()

    # We use click.echo because:
    # > Click’s echo() function will automatically strip ANSI color codes if the stream is not connected to a terminal.
    # > the echo() function will transparently connect to the terminal on Windows and translate ANSI codes to terminal API calls.
    # > This means that colors will work on Windows the same way they do on other operating systems.
    # https://click.palletsprojects.com/en/7.x/utils/#ansi-colors
    click.echo(formatter.get_str(res))
