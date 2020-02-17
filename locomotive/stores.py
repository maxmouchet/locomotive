import difflib
import logging
import re
import sqlite3
from csv import DictReader
from pathlib import Path
from typing import List, Optional, Tuple

import requests
from text_unidecode import unidecode

from .exceptions import StationNotFoundException
from .models import Station


# HACK
# Clermont Fd. => Clermont F
# Paris MP => Paris M
def fix_abbr(s: str) -> str:
    p = re.compile(r"\s(\w)\w\.?$")
    return p.sub(r" \1", s)


# TODO: Use same function as in tools/gen_stations.py
# TODO: Remove multiple spaces
def normalize(s: str) -> str:
    s = s.lower()
    s = unidecode(s)
    s = s.replace("-", " ")
    s = s.replace(".", " ")
    s = s.replace("gare de ", "")
    s = s.replace("saint ", "st ")
    s = s.replace("pche", "perrache")
    s = s.replace("zuerich", "zurich")
    return s.strip()


class Stations:
    """
    A train stations database.
    See https://github.com/trainline-eu/stations.
    """

    schema = """
    DROP TABLE IF EXISTS stations;
    CREATE TABLE stations (
        name        TEXT NOT NULL,
        name_norm   TEXT NOT NULL,
        country     TEXT NOT NULL,
        sncf_id     TEXT,
        sncf_tvs_id TEXT,
        latitude    REAL,
        longitude   REAL
    );
    """

    def __init__(self, path: Optional[Path] = None, download: bool = True):
        self.path = path
        if not self.path:
            self.path = self.default_path()
        if not self.path.exists() and download:
            print(f"{self.path} not found, downloading...")
            self.download(self.path)

    def __conn__(self) -> sqlite3.Connection:
        # We can set `check_same_thread` to False
        # since we open the database in read-only mode.
        conn = sqlite3.connect(
            f"file:{self.path}?mode=ro", check_same_thread=False, uri=True
        )
        conn.set_trace_callback(logging.debug)  # type: ignore
        return conn

    def fetchone(self, sql: str, parameters: Tuple = tuple()) -> Tuple:
        with self.__conn__() as conn:
            row: Tuple = conn.execute(sql, parameters).fetchone()
            return row

    def fetchall(self, sql: str, parameters: Tuple = tuple()) -> List[Tuple]:
        with self.__conn__() as conn:
            rows: List[Tuple] = conn.execute(sql, parameters).fetchall()
            return rows

    def count(self) -> int:
        return int(self.fetchone("SELECT COUNT(*) FROM stations")[0])

    def find_by_id(self, query: str) -> Optional[Station]:
        sql = "SELECT * FROM stations WHERE lower(sncf_id) LIKE ?"
        row = self.fetchone(sql, (query.lower(),))
        if row:
            return Station.from_row(row)
        return None

    def find_by_name(self, query: str) -> Optional[Station]:
        query_norm = normalize(fix_abbr(query))
        sql = "SELECT * FROM stations WHERE name_norm LIKE ?"
        rows = self.fetchall(sql, (f"%{query_norm}%",))
        matches = difflib.get_close_matches(
            query_norm, [x[1] for x in rows], cutoff=0.1, n=1
        )
        if matches:
            row = next(x for x in rows if x[1] == matches[0])
            return Station.from_row(row)
        return None

    def find(self, query: str) -> Optional[Station]:
        station = self.find_by_id(query)
        if not station:
            station = self.find_by_name(query)
        return station

    def find_or_raise(self, query: str) -> Station:
        station = self.find(query)
        if station:
            return station
        raise StationNotFoundException(query)

    @classmethod
    def default_path(cls) -> Path:
        return Path.home().joinpath(".locomotive", "stations.sqlite3")

    @classmethod
    def download(cls, path: Path) -> None:
        path.parent.mkdir(exist_ok=True, parents=True)

        print("Downloading trainline-eu/stations/stations.csv...")
        url = "https://github.com/trainline-eu/stations/raw/master/stations.csv"
        csv = requests.get(url).content.decode("utf-8").split("\n")

        print("Extracting stations...")
        rdr = DictReader(csv, delimiter=";")
        stations = [
            (
                row["name"],
                normalize(row["name"]),
                row["country"],
                row["sncf_id"],
                row["sncf_tvs_id"],
                row["latitude"],
                row["longitude"],
            )
            for row in rdr
        ]

        with sqlite3.connect(str(path)) as conn:
            print("Inserting stations...")
            conn.executescript(cls.schema)
            conn.executemany("INSERT INTO stations VALUES (?,?,?,?,?,?,?)", stations)
