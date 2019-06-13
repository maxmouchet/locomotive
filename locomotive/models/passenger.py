"""
Passengers.
"""

import datetime as dt

import attr


@attr.s(frozen=True, slots=True)
class Passenger:
    name: str = attr.ib()
    birthday: dt.date = attr.ib()
    commercial_card_type: str = attr.ib(default="")
    commercial_card_number: str = attr.ib(default="")
    fidelity_card_number: str = attr.ib(default="")

    @classmethod
    def dummy(cls) -> "Passenger":
        birthday = dt.date.today() - dt.timedelta(days=26 * 365)
        return cls(birthday=birthday, name="Default Passenger")

    @property
    def age(self) -> int:
        return ((dt.date.today() - self.birthday) / 365).days
