import attr
import datetime as dt
import pytz

from abc import ABC, abstractmethod
from typing import Iterator, List, Set, Union
from ..models import Journey, Passenger, Station


@attr.s(frozen=True, slots=True)
class TravelRequest:
    departure_station: Station = attr.ib()
    arrival_station: Station = attr.ib()
    passengers: List[Passenger] = attr.ib()
    date: dt.datetime = attr.ib()
    travel_class: str = attr.ib()


class AbstractClient(ABC):
    @abstractmethod
    def travel_request(self, req: TravelRequest) -> List[Journey]:
        """
        This is not needed to return all possible journeys for a given day,
        this is handled by `travel_request_full`.
        """
        ...

    def travel_request_iter(self, req: TravelRequest) -> Iterator[Journey]:
        """
        Fetch a full day, iteratively.
        """
        # TODO: Verify date overlaps and timezones...
        tz = pytz.timezone("Europe/Paris")
        cur_dt = dt.datetime(req.date.year, req.date.month, req.date.day, tzinfo=tz)

        journeys: Set[Journey] = set()

        # Finite loop to avoid sending too many requests
        # in case something goes wrong.
        # TODO: Warn if we reach the end of the loop without breaking.
        for _ in range(10):
            cur_req = attr.evolve(req, date=cur_dt)
            journeys_ = self.travel_request(cur_req)
            diff = set(journeys_).difference(journeys)
            for journey in sorted(diff, key=lambda x: x.departure_date):
                yield journey
            journeys = journeys.union(journeys_)
            new_dt = max(x.departure_date for x in journeys)
            if (new_dt == cur_dt) or (new_dt.day > cur_dt.day):
                break
            cur_dt = new_dt

    def travel_request_full(self, req: TravelRequest) -> List[Journey]:
        return list(self.travel_request_iter(req))
