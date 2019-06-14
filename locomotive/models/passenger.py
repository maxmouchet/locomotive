import datetime as dt
from typing import List

import attr


@attr.s(frozen=True, slots=True)
class Passenger:
    """
    A passenger.
    """

    name: str = attr.ib()
    birthday: dt.date = attr.ib()
    commercial_card_type: str = attr.ib(default="")
    commercial_card_number: str = attr.ib(default="")
    fidelity_card_number: str = attr.ib(default="")

    # mypy annotation
    __attrs_attrs__: List[attr.Attribute]

    @classmethod
    def dummy(cls) -> "Passenger":
        """
        Get a dummy passenger.
        """
        birthday = dt.date.today() - dt.timedelta(days=26 * 365)
        return cls(birthday=birthday, name="Default Passenger")

    @property
    def age(self) -> int:
        """
        Returns the age of the passenger on the current date, in years.
        """
        return ((dt.date.today() - self.birthday) / 365).days
