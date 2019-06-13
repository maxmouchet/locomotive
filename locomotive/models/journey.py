import datetime as dt
from typing import List

import attr

from .station import Station


@attr.s(frozen=True, slots=True)
class Segment:
    # TODO: Move to a "Train" class ?
    # TODO: Onboard services
    train_label: str = attr.ib()  # TER, TGV, ...
    train_number: str = attr.ib()
    departure_station: Station = attr.ib()
    destination_station: Station = attr.ib()
    departure_date: dt.datetime = attr.ib()
    arrival_date: dt.datetime = attr.ib()

    @property
    def duration(self) -> dt.timedelta:
        return self.arrival_date - self.departure_date


@attr.s(frozen=True, slots=True)
class Proposal:
    # TODO: Function to get friendly name (non echangeable, ...)
    # Look into fares ?
    flexibility_level: str = attr.ib()  # NOFLEX, FLEX
    # TODO: Currency ?
    price: float = attr.ib()


@attr.s(frozen=True, slots=True)
class Journey:
    segments: List[Segment] = attr.ib()
    proposals: List[Proposal] = attr.ib()

    @property
    def departure_date(self) -> dt.datetime:
        return self.segments[0].departure_date

    @property
    def arrival_date(self) -> dt.datetime:
        return self.segments[-1].arrival_date

    @property
    def duration(self) -> dt.timedelta:
        return self.arrival_date - self.departure_date
