#!/usr/bin/env python3
"""
Locomotive CLI.
"""

import datetime as dt
import sys

import click
import dateparser
import pandas as pd
import requests

from .formatters import PrettyFormatter, RawFormatter
from .stations import Stations
from .types import Location, Passenger, PassengerProfile, SNCFTravelRequest, TravelClass

ENDPOINT = "https://www.oui.sncf/proposition/rest/search-travels/outward"


@click.group()
def cli():
    """
    🚆 Search SNCF journeys from your terminal.

    \b
    Examples:
    sncf-cli search FRBES FRPAR
    """


@cli.command()
@click.argument("origin")
@click.argument("destination")
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
    else:
        date = args["date"]

    stations = Stations()

    origin_station = stations.find(args["origin"])
    if origin_station is None:
        print("Train station for {} not found :(".format(args["origin"]))
        sys.exit(1)

    destination_station = stations.find(args["destination"])
    if destination_station is None:
        print("Train station for {} not found :(".format(args["destination"]))
        sys.exit(1)

    print(
        "{} → {} ({:.0f}km) on {}\n".format(
            origin_station["name"],
            destination_station["name"],
            Stations.distance(origin_station, destination_station),
            date.strftime("%b %d %Y"),
        )
    )

    passengers = [Passenger(PassengerProfile.ADULT, args["age"])]
    origin = Location.from_station_code(origin_station["sncf_id"])
    destination = Location.from_station_code(destination_station["sncf_id"])
    travel_class = TravelClass.from_str(args["travel_class"])

    sncf_req = SNCFTravelRequest(origin, destination, passengers, date, travel_class)
    res = requests.post(ENDPOINT, json=sncf_req.sncf_dict())

    if args["formatter"] == "pretty":
        formatter = PrettyFormatter(stations=stations)
    else:
        formatter = RawFormatter()

    print(formatter.get_str(res))


if __name__ == "__main__":
    cli()
