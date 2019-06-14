"""
Output formatters.
"""

import datetime as dt
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, List, Union

import attr
import chevron

from ..models import Journey, Proposal, Segment
from ..stores import Stations


class Formatter(ABC):
    """
    Abstract class for API response formatters.
    """

    @abstractmethod
    def get_str(self, journeys: List[Journey]) -> str:
        """
        Returns a textual representation of an API response.
        """
        raise NotImplementedError


class JSONFormatter(Formatter):
    """
    JSON output.
    """

    @classmethod
    def __serialize(cls, obj: Any) -> Union[dict, str]:
        if hasattr(obj, "__attrs_attrs__"):
            return attr.asdict(obj)
        elif isinstance(obj, dt.datetime):
            return obj.isoformat()
        raise TypeError

    def get_str(self, journeys: List[Journey]) -> str:
        return json.dumps(journeys, default=self.__serialize, indent=4)


class PrettyFormatter(Formatter):
    """
    Human-readable pretty-printed output.
    """

    @classmethod
    def __format_datetime(cls, obj: dt.datetime) -> str:
        # TODO: Format dates according to user locale
        # TODO: Do this formatting inside the templates ?
        return obj.strftime("%d/%m/%Y %Hh%M")

    @classmethod
    def __format_time(cls, obj: dt.datetime) -> str:
        return obj.strftime("%Hh%M")

    @classmethod
    def __format_timedelta(cls, td: dt.timedelta) -> str:
        delta = td.seconds
        hours, remainder = divmod(delta, 3600)
        minutes, _ = divmod(remainder, 60)
        return "{:02}h{:02}m".format(int(hours), int(minutes))

    def __data_for_proposal(self, proposal: Proposal) -> dict:
        return {
            "amount": proposal.price,
            "currency": "EUR",  # TODO
            "type": proposal.flexibility_level,
        }

    def __data_for_segment(self, segment: Segment) -> dict:
        departure_date = self.__format_datetime(segment.departure_date)
        arrival_date = self.__format_datetime(segment.arrival_date)
        duration = self.__format_timedelta(segment.duration)

        return {
            "transporter": segment.train_label,
            "train_number": segment.train_number,
            "origin_station": segment.departure_station.name,
            "destination_station": segment.destination_station.name,
            "departure_date": departure_date,
            "arrival_date": arrival_date,
            "duration": duration,
        }

    def __data_for_journey(self, journey: Journey) -> dict:
        departure_date = self.__format_datetime(journey.departure_date)
        arrival_date = self.__format_datetime(journey.arrival_date)
        duration = self.__format_timedelta(journey.duration)

        proposals = list(map(self.__data_for_proposal, journey.proposals))
        segments = list(map(self.__data_for_segment, journey.segments))

        return {
            "departure_date": departure_date,
            "arrival_date": arrival_date,
            "duration": duration,
            "proposals": proposals,
            "segments": segments,
        }

    def get_str(self, journeys: List[Journey]) -> str:
        data = list(map(self.__data_for_journey, journeys))

        out = chevron.render(
            template="{{>journeys}}",
            partials_path=str(Path(__file__).parent.joinpath("templates")),
            data={"journeys": data},
        )
        out = out.replace("<b>", "\033[1m")
        out = out.replace("</b>", "\033[0m")
        out = out.strip()
        return out
