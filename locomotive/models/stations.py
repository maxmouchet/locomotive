"""
Train stations.
"""

import difflib
from pathlib import Path

import attr

import geopy.distance as gp
import pandas as pd

from typing import Optional, Tuple


@attr.s(frozen=True, slots=True)
class Station:
    name: str = attr.ib()
    sncf_id: str = attr.ib()
    latitude: float = attr.ib()
    longitude: float = attr.ib()

    @property
    def coords(self) -> Tuple[float, float]:
        """
        Get train station coordinates in geopy format.
        """
        return (self.latitude, self.longitude)

    def distance_to(self, station: "Station") -> float:
        """
        Get distance in kilometers between two train stations.
        """
        return gp.distance(self.coords, station.coords).km

    @classmethod
    def from_row(cls, row) -> "Station":
        return cls(
            name=row["name"],
            sncf_id=row.sncf_id,
            latitude=row.latitude,
            longitude=row.longitude,
        )


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
        return Path(__file__).parent.parent.joinpath("data", "stations-lite.csv")

    def find(self, q: str) -> Optional[Station]:
        # Try to find matching IDs
        # TODO: Optimize...
        if q in self.df.sncf_id.values:
            return Station.from_row(self.df[self.df.sncf_id == q].iloc[0])
        # Try to find matching name
        else:
            matches = difflib.get_close_matches(q, self.df.name.values, n=1)
            if len(matches) > 0:
                return Station.from_row(self.df[self.df.name == matches[0]].iloc[0])
        return None
