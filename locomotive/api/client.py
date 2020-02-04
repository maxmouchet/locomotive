"""
We use mulitple inheritance to allow the implementation
of clients supporting several types of requests.
"""

import logging
from typing import Iterator, List, Set

import attr

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
        cur_dt = req.date.replace(hour=0, minute=0, second=0)
        journeys: Set[Journey] = set()

        # Finite loop to avoid sending too many requests
        # in case something goes wrong.
        max_iter = 10

        for _ in range(max_iter):
            # 1) Fetch results for the current date, and abort if no results.
            cur_req = attr.evolve(req, date=cur_dt)
            journeys_ = self.travel_request(cur_req)
            if not journeys_:
                break

            # 2) Keep only new results, and yield them sorted by departure date.
            diff = set(journeys_).difference(journeys)
            for journey in sorted(diff, key=lambda x: x.departure_date):
                yield journey

            # 3) Store the results.
            journeys = journeys.union(journeys_)

            # 4) Set the new current date to the latest departure date.
            new_dt = max(x.departure_date for x in journeys)
            if (new_dt == cur_dt) or (new_dt.day > req.date.day):
                break
            cur_dt = new_dt

        # Nice tip from Fluent Python
        # p.464 "else Blocks Beyond If"
        else:
            logging.warning(
                "More than %s pages found, results will be incomplete.", max_iter
            )

    def travel_request_full(self, req: TravelRequest) -> List[Journey]:
        "Batch fetch a full day."
        return list(self.travel_request_iter(req))
