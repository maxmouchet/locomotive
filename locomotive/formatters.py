"""
Output formatters.
"""

import datetime as dt
from abc import ABC, abstractmethod

from requests import Response

from .types import SNCF_DATE_FORMAT


class Formatter(ABC):
    @abstractmethod
    def get_str(self, res: Response) -> str:
        raise NotImplementedError


class RawFormatter(Formatter):
    """
    Raw response from the API.
    """

    def get_str(self, res: Response) -> str:
        return res.content.decode("utf-8")


class PrettyFormatter(Formatter):
    """
    Human-readable pretty-printed output.
    """

    def get_str(self, res: Response) -> str:
        outs = []
        for obj in res.json()["trainProposals"]:
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
                    price_proposal["currency"],  # Show currency sign instead (€, $) ?
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
                    dt.datetime.strptime(
                        segment["departureDate"], SNCF_DATE_FORMAT
                    ).strftime("%Hh%M"),
                    dt.datetime.strptime(
                        segment["arrivalDate"], SNCF_DATE_FORMAT
                    ).strftime("%Hh%M"),
                )

            outs.append(out)

        return "\n\n\n".join(outs)