import datetime as dt
import difflib
import json
from pathlib import Path
from typing import Any, Iterator, List, Optional, Union

import attr
import pandas as pd

from .exceptions import (
    PassengerAlreadyExistsException,
    PassengerNotFoundException,
    StationNotFoundException,
)
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
            obj["birthday"] = dt.datetime.strptime(obj["birthday"], "%Y-%m-%d").date()
            passengers.append(Passenger(**obj))
        return passengers

    @classmethod
    def __serialize(cls, obj: Any) -> Union[dict, str]:
        if hasattr(obj, "__attrs_attrs__"):
            return attr.asdict(obj)
        elif isinstance(obj, dt.datetime) or isinstance(obj, dt.date):
            return obj.isoformat()
        raise TypeError

    def add(self, passenger: Passenger) -> None:
        if self.find(passenger.name):
            raise PassengerAlreadyExistsException(passenger.name)
        self.passengers.append(passenger)

    def default(self) -> Passenger:
        return Passenger.dummy()

    def find(self, query: str) -> Optional[Passenger]:
        # TODO: Optimize
        for passenger in self.passengers:
            if str(passenger.name).lower() == query.lower():
                return passenger
        return None

    def find_or_raise(self, query: str) -> Passenger:
        passenger = self.find(query)
        if passenger:
            return passenger
        raise PassengerNotFoundException(query)

    def save(self) -> Path:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        obj = list(map(attr.asdict, self.passengers))
        json.dump(obj, open(self.path, "w"), default=self.__serialize, indent=4)
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

    def find(self, query: str) -> Optional[Station]:
        # Try to find matching IDs
        # TODO: Optimize...
        if query in self.frame.sncf_id.values:
            return Station.from_row(self.frame[self.frame.sncf_id == query].iloc[0])
        # Try to find matching name
        matches = difflib.get_close_matches(query, self.frame.name.values, n=1)
        if matches:
            return Station.from_row(self.frame[self.frame.name == matches[0]].iloc[0])
        return None

    def find_or_raise(self, query: str) -> Station:
        station = self.find(query)
        if station:
            return station
        raise StationNotFoundException(query)
