import csv
import sqlite3

import requests
from text_unidecode import unidecode

stations_url = "https://github.com/trainline-eu/stations/raw/master/stations.csv"

sql = """
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

stations_csv_test = """
name;sncf_id;sncf_tvs_id;latitude;longitude;country
Le Porage;FREHF;;;;FR
St-Pons;FRIMM;;43.516667;3.516667;FR
La Gorp;FRFEV;;44.9288345;-0.4963844;FR
Villefranche-sur-Saône;FRXVF;;45.9845;4.72077;FR
Corps-Nuds;FRDXD;;47.9851669;-1.5754723999999998;FR
Rennes;FRRBW;;48.083333;-1.683333;FR
Poitiers;FRPIS;;46.582275;0.333241;FR
Jeumont Frontière;;FRCMW;;;FR
Nolay Place Carnot;FRJFU;;46.944266999999996;4.6366;FR
Douarnenez Ancienne Gare;FREAN;;;;FR
""".strip().split(
    "\n"
)

print("Downloading trainline-eu/stations/stations.csv...")
stations_csv = requests.get(stations_url).content.decode("utf-8").split("\n")


def normalize(s):
    s = s.lower()
    s = unidecode(s)
    s = s.replace("-", " ")
    s = s.replace(".", "")
    s = s.replace("gare de ", "")
    return s


def extract_stations(csvfile):
    print("Extracting stations...")
    rdr = csv.DictReader(csvfile, delimiter=";")
    return [
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


def create_database(path, stations):
    print(f"(Re)Creating {path}...")
    with sqlite3.connect(path) as conn:
        c = conn.cursor()

        print("Applying schema...")
        c.executescript(sql)

        print("Inserting stations...")
        c.executemany("INSERT INTO stations VALUES (?,?,?,?,?,?,?)", stations)

        conn.commit()


def main():
    stations = extract_stations(stations_csv)
    create_database("locomotive/data/stations.sqlite3", stations)

    stations = extract_stations(stations_csv_test)
    create_database("tests/test-stations.sqlite3", stations)


if __name__ == "__main__":
    main()
