import datetime as dt
from typing import Tuple

import attr

from .station import Station


@attr.s(frozen=True, slots=True)
class Segment:
    # TODO: Move to a "Train" class ?
    # TODO: Onboard services
    train_label: str = attr.ib()  # TER, TGV, ...
    train_number: str = attr.ib()
    departure_station: Station = attr.ib()
    arrival_station: Station = attr.ib()
    departure_date: dt.datetime = attr.ib()
    arrival_date: dt.datetime = attr.ib()

    @property
    def duration(self) -> dt.timedelta:
        """
        Returns the durations of the segment.
        """
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
    # We use tuples to guaranteed immutability
    # and make Journey hashable.
    segments: Tuple[Segment, ...] = attr.ib()
    proposals: Tuple[Proposal, ...] = attr.ib()

    @property
    def departure_date(self) -> dt.datetime:
        # pylint: disable=unsubscriptable-object
        return self.segments[0].departure_date

    @property
    def arrival_date(self) -> dt.datetime:
        # pylint: disable=unsubscriptable-object
        return self.segments[-1].arrival_date

    @property
    def departure_station(self) -> Station:
        # pylint: disable=unsubscriptable-object
        return self.segments[0].departure_station

    @property
    def arrival_station(self) -> Station:
        # pylint: disable=unsubscriptable-object
        return self.segments[-1].arrival_station

    @property
    def duration(self) -> dt.timedelta:
        """
        Returns the duration of the journey.
        """
        return self.arrival_date - self.departure_date
