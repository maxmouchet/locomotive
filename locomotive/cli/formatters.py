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
from money.money import Money

from ..models import Journey, Proposal, Segment


class Formatter(ABC):
    """
    Abstract class for API response formatters.
    """

    @abstractmethod
    def incr_str(self, journey: Journey) -> str:
        """
        Returns a textual representation of an API response
        for a single journey.
        """
        raise NotImplementedError

    def full_str(self, journeys: List[Journey]) -> str:
        return (
            self.start_str()
            + "".join(self.incr_str(x) for x in journeys)
            + self.end_str()
        )

    def start_str(self) -> str:
        return ""

    def end_str(self) -> str:
        return ""


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
        elif isinstance(obj, Money):
            return {"amount": float(obj.amount), "currency": obj.currency.name}
        raise TypeError

    def incr_str(self, journey: Journey) -> str:
        return json.dumps(journey, default=self.__serialize, indent=4) + ","

    def start_str(self) -> str:
        return "["

    def end_str(self) -> str:
        # TODO: Proper handling of last array element
        return "{}]"


class PrettyFormatter(Formatter):
    """
    Human-readable pretty-printed output.
    """

    @classmethod
    def __format_datetime(cls, obj: dt.datetime) -> str:
        # TODO: Format dates according to user locale (use babel ?)
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
            "amount": proposal.price.amount,
            "currency": proposal.price.currency.name,
            "type": proposal.flexibility_level,
        }

    def __data_for_segment(self, segment: Segment) -> dict:
        departure_date = self.__format_datetime(segment.departure_date)
        arrival_date = self.__format_datetime(segment.arrival_date)
        duration = self.__format_timedelta(segment.duration)

        return {
            "transporter": segment.transport.label,
            "train_number": segment.transport.number,
            "departure_station": segment.departure_station.name,
            "arrival_station": segment.arrival_station.name,
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

    def incr_str(self, journey: Journey) -> str:
        data = self.__data_for_journey(journey)

        out = chevron.render(
            template="{{> journey}}",
            partials_path=str(Path(__file__).parent.joinpath("templates")),
            data=data,
        )
        out = out.replace("<b>", "\033[1m")
        out = out.replace("</b>", "\033[0m")
        return str(out)
