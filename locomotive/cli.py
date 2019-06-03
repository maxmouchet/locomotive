#!/usr/bin/env python3

import click
import requests
import datetime as dt
import dateparser

from .types import *
from .utils import *

ENDPOINT = "https://www.oui.sncf/proposition/rest/search-travels/outward"


@click.group()
def cli():
    pass


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

    if type(date) is str:
        date = dateparser.parse(date)

    sncf_req = SNCFTravelRequest(origin, destination, passengers, date, klass)
    r = requests.post(ENDPOINT, json=sncf_req.sncf_dict())

    if raw_output:
        print(r.content)
    else:
        for proposal in r.json()["trainProposals"]:
            print(pretty_train_proposal(proposal))
            print("\n")


if __name__ == "__main__":
    cli()
