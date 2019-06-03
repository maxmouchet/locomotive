#!/usr/bin/env python3
"""
Locomotive CLI.
"""

import datetime as dt

import click
import dateparser
import requests

from .types import (
    Location,
    LocationType,
    Passenger,
    PassengerProfile,
    SNCFTravelRequest,
    TravelClass,
)
from .utils import pretty_train_proposal

ENDPOINT = "https://www.oui.sncf/proposition/rest/search-travels/outward"


@click.group()
def cli():
    """

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
@click.option("--raw-output", is_flag=True)
def search(origin_code, destination_code, age, date, travel_class, raw_output):
    """
    Search for trains.

    \b
    sncf-cli search FRBES FRPAR
    sncf-cli search FRBES FRPAR --class second --date 2019-06-01
    """
    passengers = [Passenger(PassengerProfile.ADULT, age)]
    origin = Location(LocationType.G, origin_code)
    destination = Location(LocationType.G, destination_code)
    klass = TravelClass[travel_class.upper()]

    if isinstance(date, str):
        date = dateparser.parse(date)

    sncf_req = SNCFTravelRequest(origin, destination, passengers, date, klass)
    res = requests.post(ENDPOINT, json=sncf_req.sncf_dict())

    if raw_output:
        print(res.content)
    else:
        for proposal in res.json()["trainProposals"]:
            print(pretty_train_proposal(proposal))
            print("\n")


if __name__ == "__main__":
    cli()
