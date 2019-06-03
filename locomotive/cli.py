#!/usr/bin/env python3
"""
Locomotive CLI.
"""

import datetime as dt

import click
import dateparser
import requests

from .formatters import PrettyFormatter, RawFormatter
from .types import Location, Passenger, PassengerProfile, SNCFTravelRequest, TravelClass

ENDPOINT = "https://www.oui.sncf/proposition/rest/search-travels/outward"


@click.group()
def cli():
    """
    🚆 Search for trains from your terminal.

    \b
    Examples:
    sncf-cli search FRBES FRPAR
    """


@cli.command()
@click.argument("origin_code")
@click.argument("destination_code")
@click.option("--age", default=26)
@click.option("--date", default=dt.date.today())
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
    if isinstance(args["date"], str):
        date = dateparser.parse(args["date"])

    passengers = [Passenger(PassengerProfile.ADULT, args["age"])]
    origin = Location.from_station_code(args["origin_code"])
    destination = Location.from_station_code(args["destination_code"])
    travel_class = TravelClass.from_str(args["travel_class"])

    sncf_req = SNCFTravelRequest(origin, destination, passengers, date, travel_class)
    res = requests.post(ENDPOINT, json=sncf_req.sncf_dict())

    if args["formatter"] == "pretty":
        formatter = PrettyFormatter()
    else:
        formatter = RawFormatter()

    print(formatter.get_str(res))


if __name__ == "__main__":
    cli()
