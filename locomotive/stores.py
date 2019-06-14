import difflib
import json
from pathlib import Path
from typing import Iterator, List, Optional

import attr
import pandas as pd

from .exceptions import PassengerNotFoundException, StationNotFoundException
from .models import Passenger, Station


class Passengers:
    """
    Passengers store.
    """

    path: Path
    passengers: List[Passenger]

    def __init__(self, path: Optional[Path] = None) -> None:
        if path is None:
            path = self.default_path()

        self.path = Path(path).expanduser().absolute()

        if self.path.exists():
            self.passengers = self.__passengers_from_json(self.path)
        else:
            self.passengers = [Passenger.dummy()]

    def __iter__(self) -> Iterator[Passenger]:
        return self.passengers.__iter__()

    @classmethod
    def default_path(cls) -> Path:
        return Path.home().joinpath(".locomotive", "passengers.json")

    @classmethod
    def __passengers_from_json(cls, path: Path) -> List[Passenger]:
        passengers = []
        for obj in json.load(open(path)):
            passengers.append(Passenger(**obj))
        return passengers

    def add(self, passenger: Passenger) -> None:
        # TODO: Handle name conflicts
        self.passengers.append(passenger)

    def default(self) -> Passenger:
        return Passenger.dummy()

    def find(self, query: str) -> Passenger:
        # TODO: Implement
        raise NotImplementedError

    def save(self) -> Path:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        obj = list(map(attr.asdict, self.passengers))
        json.dump(obj, open(self.path, "w"), indent=2)
        return self.path


class Stations:
    """
    A train stations database.
    See https://github.com/trainline-eu/stations.
    """

    frame: pd.DataFrame
    path: Path

    def __init__(self, path: Optional[Path] = None) -> None:
        if path is None:
            path = self.default_path()
        self.frame = pd.read_csv(path, sep=";")

    @classmethod
    def default_path(cls) -> Path:
        return Path(__file__).parent.joinpath("data", "stations-lite.csv")

    def find(self, query: str) -> Station:
        # Try to find matching IDs
        # TODO: Optimize...
        if query in self.frame.sncf_id.values:
            return Station.from_row(self.frame[self.frame.sncf_id == query].iloc[0])
        # Try to find matching name
        matches = difflib.get_close_matches(query, self.frame.name.values, n=1)
        if matches:
            return Station.from_row(self.frame[self.frame.name == matches[0]].iloc[0])
        raise StationNotFoundException(query)
