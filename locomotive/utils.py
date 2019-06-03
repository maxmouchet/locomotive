"""
Utilities.
"""

import datetime as dt

from .types import SNCF_DATE_FORMAT


def pretty_train_proposal(obj):
    """
    Pretty print a train proposal.
    """
    out = "Proposal {} - {}".format(
        dt.datetime.strptime(obj["departureDate"], SNCF_DATE_FORMAT).strftime(
            "%d/%m/%Y %Hh%M"
        ),
        dt.datetime.strptime(obj["arrivalDate"], SNCF_DATE_FORMAT).strftime(
            "%d/%m/%Y %Hh%M"
        ),
    )

    out += "\nPrices:"
    for price_proposal in obj["priceProposals"]:
        remaining_seats = price_proposal.get("remainingSeat", "?")
        out += "\n+ {} {} ({}) [{} remaining seats]".format(
            price_proposal["amount"],
            price_proposal["currency"],
            price_proposal["type"],
            remaining_seats,
        )

    out += "\nTrains:"
    for segment in obj["segments"]:
        out += "\n+ {} {} from {} to {}".format(
            segment["transporter"],
            segment["trainNumber"],
            segment["originStationCode"],
            segment["destinationStationCode"],
        )
        out += "\n  {} - {}".format(
            dt.datetime.strptime(segment["departureDate"], SNCF_DATE_FORMAT).strftime(
                "%Hh%M"
            ),
            dt.datetime.strptime(segment["arrivalDate"], SNCF_DATE_FORMAT).strftime(
                "%Hh%M"
            ),
        )

    return out
