import difflib
import json
from pathlib import Path
from typing import List, Optional

import attr
import pandas as pd

from .models import Passenger, Station


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
        # TODO: Handle name conflicts
        self.passengers.append(passenger)

    def default(self) -> Passenger:
        return Passenger.dummy()

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

    df: pd.DataFrame
    path: Path

    def __init__(self, path=None):
        if path is None:
            path = self.default_path()
        self.df = pd.read_csv(path, sep=";")

    @classmethod
    def default_path(cls) -> Path:
        return Path(__file__).parent.joinpath("data", "stations-lite.csv")

    def find(self, q: str) -> Optional[Station]:
        # Try to find matching IDs
        # TODO: Optimize...
        if q in self.df.sncf_id.values:
            return Station.from_row(self.df[self.df.sncf_id == q].iloc[0])
        # Try to find matching name
        else:
            matches = difflib.get_close_matches(q, self.df.name.values, n=1)
            if matches:
                return Station.from_row(self.df[self.df.name == matches[0]].iloc[0])
        return None
