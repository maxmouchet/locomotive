import datetime as dt
import json
from pathlib import Path
from typing import Any, Iterable, Union

import attr
import chevron
from money.money import Money

from ..models import Journey, Proposal, Segment


class JSONFormatter:
    """
    JSON output.
    """

    @staticmethod
    def serialize(obj: Any) -> Union[dict, str]:
        if hasattr(obj, "__attrs_attrs__"):
            return attr.asdict(obj)
        if isinstance(obj, dt.datetime):
            return obj.isoformat()
        if isinstance(obj, Money):
            return {"amount": float(obj.amount), "currency": obj.currency.name}
        raise TypeError

    def format(self, journeys: Iterable[Journey]) -> str:
        return json.dumps(list(journeys), default=self.serialize, indent=4)


class PrettyFormatter:
    """
    Human-readable pretty-printed output.
    """

    @classmethod
    def format_datetime(cls, obj: dt.datetime) -> str:
        # TODO: Format dates according to user locale (use babel ?)
        # TODO: Do this formatting inside the templates ?
        return obj.strftime("%d/%m/%Y %Hh%M")

    @classmethod
    def format_time(cls, obj: dt.datetime) -> str:
        return obj.strftime("%Hh%M")

    @classmethod
    def format_timedelta(cls, td: dt.timedelta) -> str:
        delta = td.seconds
        hours, remainder = divmod(delta, 3600)
        minutes, _ = divmod(remainder, 60)
        return "{:02}h{:02}m".format(int(hours), int(minutes))

    def data_for_proposal(self, proposal: Proposal) -> dict:
        return {
            "amount": proposal.price.amount,
            "currency": proposal.price.currency.name,
            "type": proposal.flexibility_level,
        }

    def data_for_segment(self, segment: Segment) -> dict:
        departure_date = self.format_datetime(segment.departure_date)
        arrival_date = self.format_datetime(segment.arrival_date)
        duration = self.format_timedelta(segment.duration)

        return {
            "transporter": segment.transport.label,
            "train_number": segment.transport.number,
            "departure_station": segment.departure_station.name,
            "arrival_station": segment.arrival_station.name,
            "departure_date": departure_date,
            "arrival_date": arrival_date,
            "duration": duration,
        }

    def data_for_journey(self, journey: Journey) -> dict:
        departure_date = self.format_datetime(journey.departure_date)
        arrival_date = self.format_datetime(journey.arrival_date)
        duration = self.format_timedelta(journey.duration)

        proposals = list(map(self.data_for_proposal, journey.proposals))
        segments = list(map(self.data_for_segment, journey.segments))

        return {
            "departure_date": departure_date,
            "arrival_date": arrival_date,
            "duration": duration,
            "proposals": proposals,
            "segments": segments,
        }

    def format(self, journeys: Iterable[Journey]) -> str:
        data = [self.data_for_journey(journey) for journey in journeys]
        out = chevron.render(
            template="{{> journeys}}",
            partials_path=str(Path(__file__).parent.joinpath("templates")),
            data={"journeys": data},
        )
        out = out.replace("<b>", "\033[1m")
        out = out.replace("</b>", "\033[0m")
        return str(out)
