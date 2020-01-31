"""
We use mulitple inheritance to allow the implementation
of clients supporting several types of requests.
"""

import datetime as dt
from typing import Iterator, List, Set

import attr
import pytz

from ..models import BoardEntry, Journey
from .requests import BoardRequest, TravelRequest


class BoardClient:
    def board_request(self, req: BoardRequest) -> List[BoardEntry]:
        "Request the arrival or departure board for a train station."
        raise NotImplementedError


class TravelClient:
    def travel_request(self, req: TravelRequest) -> List[Journey]:
        """
        Request the available journeys and prices
        for a departure and arrival train station.
        """
        raise NotImplementedError

    def travel_request_iter(self, req: TravelRequest) -> Iterator[Journey]:
        "Iteratively fetch a full day."
        # TODO: Verify date overlaps and timezones...
        tz = pytz.timezone("Europe/Paris")
        cur_dt = dt.datetime(req.date.year, req.date.month, req.date.day)
        cur_dt = tz.localize(cur_dt)

        journeys: Set[Journey] = set()

        # Finite loop to avoid sending too many requests
        # in case something goes wrong.
        # TODO: Warn if we reach the end of the loop without breaking.
        for _ in range(10):
            cur_req = attr.evolve(req, date=cur_dt)
            journeys_ = self.travel_request(cur_req)
            if not journeys_:
                break
            diff = set(journeys_).difference(journeys)
            for journey in sorted(diff, key=lambda x: x.departure_date):
                yield journey
            journeys = journeys.union(journeys_)
            new_dt = max(x.departure_date for x in journeys)
            if (new_dt == cur_dt) or (new_dt.day > req.date.day):
                break
            cur_dt = new_dt

    def travel_request_full(self, req: TravelRequest) -> List[Journey]:
        "Batch fetch a full day."
        return list(self.travel_request_iter(req))
