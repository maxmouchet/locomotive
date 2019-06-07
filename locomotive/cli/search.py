import datetime as dt
import sys

import click
import dateparser

from ..api.oui_v1 import Client
from ..formatters import PrettyFormatter, RawFormatter
from ..stations import Stations


def err_station_not_found(string):
    click.echo("Train station for {} not found :(".format(string), err=True)
    sys.exit(1)


@click.command()
@click.argument("origin")
@click.argument("destination")
@click.option("--age", default=26)
@click.option("--date", default="now")
@click.option(
    "--class", "travel_class", type=click.Choice(["first", "second"]), default="second"
)
@click.option("--formatter", type=click.Choice(["pretty", "raw"]), default="pretty")
def search(**args):
    """
    Search for trains.

    \b
    sncf-cli search FRBES FRPAR
    sncf-cli search FRBES FRPAR --class second --date 2019-06-01
    """
    date = dateparser.parse(args["date"])

    stations = Stations()

    origin_station = stations.find(args["origin"])
    destination_station = stations.find(args["destination"])

    if origin_station is None:
        err_station_not_found(args["origin"])

    if destination_station is None:
        err_station_not_found(args["destination"])

    click.echo(
        "{} → {} ({:.0f}km) on {}\n".format(
            origin_station["name"],
            destination_station["name"],
            Stations.distance(origin_station, destination_station),
            date.strftime("%b %d %Y"),
        ),
        err=True,
    )

    client = Client()
    res = client.simple_request(
        args["age"], origin_station, destination_station, date, args["travel_class"]
    )

    if args["formatter"] == "pretty":
        formatter = PrettyFormatter(stations=stations)
    else:
        formatter = RawFormatter()

    # We use click.echo because:
    # > Click’s echo() function will automatically strip ANSI color codes if the stream is not connected to a terminal.
    # > the echo() function will transparently connect to the terminal on Windows and translate ANSI codes to terminal API calls.
    # > This means that colors will work on Windows the same way they do on other operating systems.
    # https://click.palletsprojects.com/en/7.x/utils/#ansi-colors
    click.echo(formatter.get_str(res))
