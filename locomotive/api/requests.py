import datetime as dt
from typing import List

import attr

from ..models import Passenger, Station


@attr.s(frozen=True)
class BoardRequest:
    "Request the arrival or departure board for a train station."
    station: Station = attr.ib()
    type_: str = attr.ib()  # departure/arrival


@attr.s(frozen=True)
class TravelRequest:
    departure_station: Station = attr.ib()
    arrival_station: Station = attr.ib()
    passengers: List[Passenger] = attr.ib()
    date: dt.datetime = attr.ib()
    travel_class: str = attr.ib()
