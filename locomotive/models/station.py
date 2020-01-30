# pylint: disable=E0611
from typing import Tuple

import attr
import geopy.distance as gp
from faker import Faker


@attr.s(frozen=True, slots=True)
class Station:
    """
    A train station.
    """

    name: str = attr.ib()
    name_norm: str = attr.ib()
    sncf_id: str = attr.ib()
    sncf_tvs_id: str = attr.ib()
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
        return float(gp.distance(self.coords, station.coords).km)

    @classmethod
    def from_row(cls, row: tuple) -> "Station":
        """
        Instantiate a Station from a row of stations.sqlite3.
        """
        return cls(
            name=row[0],
            name_norm=row[1],
            sncf_id=row[3],
            sncf_tvs_id=row[4],
            latitude=row[5],
            longitude=row[6],
        )

    @classmethod
    def fake(cls) -> "Station":
        f = Faker("fr_FR")
        name = f.city()
        return cls(
            name=name,
            # TODO: Normalize
            name_norm=name,
            sncf_id="FR" + "".join(f.random_uppercase_letter() for _ in range(3)),
            sncf_tvs_id="".join(f.random_uppercase_letter() for _ in range(3)),
            latitude=float(f.latitude()),
            longitude=float(f.longitude()),
        )
