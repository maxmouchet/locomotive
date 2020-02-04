# pylint: disable=unsubscriptable-object

import datetime as dt
import random
from typing import Optional, Tuple

import attr
from money.currency import Currency
from money.money import Money

from .station import Station


@attr.s(frozen=True, slots=True)
class Transport:
    # TODO: Onboard services
    equipment: str = attr.ib()
    """
    Euronet equipment code (TGA, TGB, CAR...).
    http://www.raileurope.fr/Extranet/Practical_information/Euronet_Equipment_Codes.pdf
    """

    label: str = attr.ib()
    "TER, TGV, Autocar..."

    number: str = attr.ib()

    type: str = attr.ib()
    "TRAIN, BUS..."

    @classmethod
    def fake(cls) -> "Transport":
        return cls(
            equipment=random.choice(["TGA", "TGB", "TGC", "TGD"]),
            label=random.choice(["TER", "TGV"]),
            number=str(random.randint(1000, 9999)),
            type="TRAIN",
        )


@attr.s(frozen=True, slots=True)
class Segment:
    transport: Transport = attr.ib()
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
            transport=Transport.fake(),
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
    price: Money = attr.ib()

    @classmethod
    def fake(cls) -> "Proposal":
        return Proposal(
            flexibility_level=random.choice(["NOFLEX", "FLEX", "UPSELL"]),
            price=Money.from_sub_units(random.randint(100, 10000), Currency.EUR),
        )


@attr.s(frozen=True, slots=True)
class Journey:
    """A Train Journey."""

    # We use tuples to guaranteed immutability
    # and make Journey hashable.

    segments: Tuple[Segment, ...] = attr.ib()
    """Journey segments, from departure to arrival."""

    proposals: Tuple[Proposal, ...] = attr.ib()
    """Journey proposals."""

    @property
    def departure_date(self) -> dt.datetime:
        return self.segments[0].departure_date

    @property
    def arrival_date(self) -> dt.datetime:
        return self.segments[-1].arrival_date

    @property
    def departure_station(self) -> Station:
        return self.segments[0].departure_station

    @property
    def arrival_station(self) -> Station:
        return self.segments[-1].arrival_station

    @property
    def duration(self) -> dt.timedelta:
        return self.arrival_date - self.departure_date

    @property
    def lowest_price(self) -> Optional[Money]:
        """
        Lowest price for the journey, amongst all proposals.
        """
        if not self.proposals:
            return None
        return min(x.price for x in self.proposals)

    @classmethod
    def fake(cls) -> "Journey":
        return Journey(
            segments=tuple(Segment.fake() for _ in range(random.randint(1, 3))),
            proposals=tuple(Proposal.fake() for _ in range(random.randint(0, 3))),
        )
