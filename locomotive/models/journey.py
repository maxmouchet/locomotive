import datetime as dt
import random
from typing import Optional, Tuple

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

    @classmethod
    def fake(cls) -> "Segment":
        departure_date = dt.datetime(2020, random.randint(1, 12), random.randint(1, 28))
        arrival_date = departure_date + dt.timedelta(
            hours=random.randint(1, 12), minutes=random.randint(0, 59)
        )
        return cls(
            train_label=random.choice(["TER", "TGV"]),
            train_number=str(random.randint(1000, 9999)),
            departure_station=Station.fake(),
            arrival_station=Station.fake(),
            departure_date=departure_date,
            arrival_date=arrival_date,
        )


@attr.s(frozen=True, slots=True)
class Proposal:
    # TODO: Function to get friendly name (non echangeable, ...)
    # Look into fares ?
    flexibility_level: str = attr.ib()  # NOFLEX, FLEX
    # TODO: Price/Currency type
    # https://github.com/vimeo/py-money
    price: float = attr.ib()

    @classmethod
    def fake(cls) -> "Proposal":
        return Proposal(
            flexibility_level=random.choice(["NOFLEX", "FLEX", "UPSELL"]),
            price=random.random() * 200,
        )


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

    @property
    def lowest_price(self) -> Optional[float]:
        """
        Returns the lowest price amongst all proposals.
        """
        if not self.proposals:
            return None
        return min([x.price for x in self.proposals])

    @classmethod
    def fake(cls) -> "Journey":
        return Journey(
            segments=tuple(Segment.fake() for _ in range(random.randint(1, 3))),
            proposals=tuple(Proposal.fake() for _ in range(random.randint(0, 3))),
        )
