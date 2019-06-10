"""
Passengers.
"""

import json
from pathlib import Path
from typing import List

import attr


@attr.s(frozen=True, slots=True)
class Passenger:
    age: int = attr.ib()
    name: str = attr.ib()

    @classmethod
    def dummy(cls) -> "Passenger":
        return cls(age=26, name="Default Passenger")


class Passengers:
    """
    Passengers store.
    """

    path: Path
    passengers: List[Passenger]

    def __init__(self, path=None):
        if path is None:
            path = self.default_path()

        self.path = Path(path).expanduser().absolute()

        if self.path.exists():
            self.passengers = self.__passengers_from_json(self.path)
        else:
            self.passengers = [Passenger.dummy()]

    def __iter__(self):
        return self.passengers.__iter__()

    @classmethod
    def default_path(cls) -> Path:
        return Path.home().joinpath(".locomotive", "passengers.json")

    @classmethod
    def __passengers_from_json(self, fp: str) -> List[Passenger]:
        passengers = []
        for obj in json.load(open(fp)):
            passengers.append(Passenger(**obj))
        return passengers

    def add(self, passenger: Passenger) -> None:
        self.passengers.append(passenger)

    def save(self) -> Path:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        obj = list(map(attr.asdict, self.passengers))
        json.dump(obj, open(self.path, "w"), indent=2)
        return self.path
