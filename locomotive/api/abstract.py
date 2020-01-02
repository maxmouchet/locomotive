import datetime as dt
import pytz

from abc import ABC, abstractmethod
from typing import Iterator, List, Set, Union
from ..models import Journey, Passenger, Station


class AbstractClient(ABC):
    @abstractmethod
    def travel_request(
        self,
        departure_station: Station,
        arrival_station: Station,
        passengers: List[Passenger],
        date: dt.datetime,
        travel_class: str,
    ) -> List[Journey]:
        """
        This is not needed to return all possible journeys for a given day,
        this is handled by `travel_request_full`.
        """
        ...

    def travel_request_iter(
        self,
        departure_station: Station,
        arrival_station: Station,
        passengers: List[Passenger],
        date: Union[dt.date, dt.datetime],
        travel_class: str,
    ) -> Iterator[Journey]:
        """
        Fetch a full day, iteratively.
        """
        # TODO: Verify date overlaps and timezones...
        tz = pytz.timezone("Europe/Paris")
        cur_dt = dt.datetime(date.year, date.month, date.day, tzinfo=tz)

        journeys: Set[Journey] = set()

        # Finite loop to avoid sending too many requests
        # in case something goes wrong.
        # TODO: Warn if we reach the end of the loop without breaking.
        for _ in range(10):
            journeys_ = self.travel_request(
                departure_station, arrival_station, passengers, cur_dt, travel_class
            )
            diff = set(journeys_).difference(journeys)
            for journey in sorted(diff, key=lambda x: x.departure_date):
                yield journey
            journeys = journeys.union(journeys_)
            new_dt = max(x.departure_date for x in journeys)
            if (new_dt == cur_dt) or (new_dt.day > cur_dt.day):
                break
            cur_dt = new_dt

    def travel_request_full(self, *args, **kwargs) -> List[Journey]:  # type: ignore
        return list(self.travel_request_iter(*args, **kwargs))
