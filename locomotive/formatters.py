"""
Output formatters.
"""

import datetime as dt
import os
from abc import ABC, abstractmethod

import chevron
from requests import Response

from .api.oui_v1 import SNCF_DATE_FORMAT
from .stations import Stations


class Formatter(ABC):
    """
    Abstract class for API response formatters.
    """

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

    def __init__(self, stations: Stations):
        self.stations = stations

    @classmethod
    def __parse_sncf_date(cls, string):
        return dt.datetime.strptime(string, SNCF_DATE_FORMAT)

    @classmethod
    def __format_datetime(cls, obj):
        # TODO: Format dates according to user locale
        # TODO: Do this formatting inside the templates ?
        return obj.strftime("%d/%m/%Y %Hh%M")

    @classmethod
    def __format_time(cls, obj):
        return obj.strftime("%Hh%M")

    @classmethod
    def __timedelta(cls, start, end):
        start = dt.datetime.strptime(start, "%d/%m/%Y %Hh%M")
        end = dt.datetime.strptime(end, "%d/%m/%Y %Hh%M")
        delta = end - start
        delta = delta.seconds

        hours, remainder = divmod(delta, 3600)
        minutes, _ = divmod(remainder, 60)

        return "{:02}h{:02}m".format(int(hours), int(minutes))

    def __data_for_price(self, obj):
        return {
            "amount": obj["amount"],
            "currency": obj["currency"],  # Show currency sign instead (€, $) ?
            "type": obj["type"],
            "seats": obj.get("remainingSeat", "?"),
        }

    def __data_for_segment(self, obj):
        origin_station = self.stations.find(obj["originStationCode"])
        destination_station = self.stations.find(obj["destinationStationCode"])

        # TODO: Cleanup...
        if origin_station is not None:
            origin_station_name = origin_station["name"]
        else:
            origin_station_name = obj["originStationCode"]

        if destination_station is not None:
            destination_station_name = destination_station["name"]
        else:
            destination_station_name = obj["destinationStationCode"]

        departure_date = self.__format_datetime(
            self.__parse_sncf_date(obj["departureDate"])
        )
        arrival_date = self.__format_datetime(
            self.__parse_sncf_date(obj["arrivalDate"])
        )

        duration = self.__timedelta(departure_date, arrival_date)
        print(duration)
        print(departure_date, arrival_date)

        return {
            "transporter": obj["transporter"],
            "train_number": obj["trainNumber"],
            "origin_station": origin_station_name,
            "destination_station": destination_station_name,
            "departure_date": departure_date,
            "arrival_date": arrival_date,
            "duration": duration,
        }

    def __data_for_proposal(self, obj):
        departure_date = self.__format_datetime(
            self.__parse_sncf_date(obj["departureDate"])
        )
        arrival_date = self.__format_datetime(
            self.__parse_sncf_date(obj["arrivalDate"])
        )

        prices = list(map(self.__data_for_price, obj["priceProposals"]))
        segments = list(map(self.__data_for_segment, obj["segments"]))

        print("Global: ", departure_date, arrival_date)
        duration = self.__timedelta(departure_date, arrival_date)
        print(duration)

        return {
            "departure_date": departure_date,
            "arrival_date": arrival_date,
            "duration": duration,
            "prices": prices,
            "segments": segments,
        }

    def get_str(self, res: Response) -> str:
        proposals = list(map(self.__data_for_proposal, res.json()["trainProposals"]))

        args = {
            "template": "{{>proposals}}",
            "partials_path": os.path.join(os.path.dirname(__file__), "templates"),
            "data": {"proposals": proposals},
        }

        out = chevron.render(**args)
        out = out.replace("<b>", "\033[1m")
        out = out.replace("</b>", "\033[0m")
        out = out.strip()
        return out
