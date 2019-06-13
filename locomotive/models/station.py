"""
Train stations.
"""


from typing import Tuple

import attr
import geopy.distance as gp


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
