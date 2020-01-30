import contextlib
import difflib
import sqlite3
from pathlib import Path
from typing import Optional

import attr
from text_unidecode import unidecode

from .exceptions import StationNotFoundException
from .models import Station


class Stations:
    """
    A train stations database.
    See https://github.com/trainline-eu/stations.
    """

    path: Path

    def __init__(self, path: Optional[Path] = None) -> None:
        self.path = self.default_path()
        if path:
            self.path = path

    def _conn(self) -> sqlite3.Connection:
        return sqlite3.connect(f"file:{self.path}?mode=ro", uri=True)

    @classmethod
    def default_path(cls) -> Path:
        return Path(__file__).parent.joinpath("data", "stations.sqlite3")

    def count(self) -> int:
        with self._conn() as conn:
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM stations")
            return int(c.fetchone()[0])

    def find(self, query: str) -> Optional[Station]:
        query = unidecode(query.lower())
        with self._conn() as conn:
            c = conn.cursor()

            # a) Try to find matching IDs
            c.execute("SELECT * FROM stations WHERE lower(sncf_id) LIKE ?", (query,))
            row = c.fetchone()
            if row:
                return Station.from_row(row)

            # b) Try to find matching name
            c.execute(
                "SELECT * FROM stations WHERE lower(name_ascii) LIKE ?", (f"%{query}%",)
            )
            rows = c.fetchall()
            matches = difflib.get_close_matches(query, [x[0] for x in rows], n=1)
            if matches:
                row = next(x for x in rows if x[0] == matches[0])
                return Station.from_row(row)

            return None

    def find_or_raise(self, query: str) -> Station:
        station = self.find(query)
        if station:
            return station
        raise StationNotFoundException(query)
