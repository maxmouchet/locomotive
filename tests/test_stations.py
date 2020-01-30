import os

import pytest
from locomotive.exceptions import StationNotFoundException
from locomotive.stores import Stations


def test_can_load_default_data_if_no_path_provided():
    stations = Stations()
    assert stations.count() > 0


def test_can_load_data():
    fp = os.path.join(os.path.dirname(__file__), "test-stations.sqlite3")
    stations = Stations(fp)
    assert stations.count() == 10


def test_can_find_station_by_name():
    fp = os.path.join(os.path.dirname(__file__), "test-stations.sqlite3")
    stations = Stations(fp)

    assert stations.find("Le Porage")
    assert stations.find("LE PORAGE")
    assert stations.find("le porage")

    # Accents
    assert stations.find("Jeumont Frontière")
    assert stations.find("Jeumont Frontiere")


def test_raises_exception_when_cannot_find_station_by_a_given_name():
    fp = os.path.join(os.path.dirname(__file__), "test-stations.sqlite3")
    stations = Stations(fp)
    with pytest.raises(StationNotFoundException):
        stations.find_or_raise("This station doesn't exist")


def test_can_find_station_by_id():
    fp = os.path.join(os.path.dirname(__file__), "test-stations.sqlite3")
    stations = Stations(fp)

    assert stations.find("FRFEV")
    assert stations.find("frfev")
    assert stations.find("frFeV")


def test_raises_exception_when_cannot_find_station_by_a_given_id():
    fp = os.path.join(os.path.dirname(__file__), "test-stations.sqlite3")
    stations = Stations(fp)
    with pytest.raises(StationNotFoundException):
        stations.find_or_raise("This station ID doesn't exist")


def test_can_retrieve_coords():
    fp = os.path.join(os.path.dirname(__file__), "test-stations.sqlite3")
    stations = Stations(fp)

    station = stations.find("FRFEV")

    coords = station.coords

    assert len(coords) == 2

    assert coords[0] == 44.9288345
    assert coords[1] == -0.4963844


def test_can_compute_distance_between_two_stations():
    fp = os.path.join(os.path.dirname(__file__), "test-stations.sqlite3")
    stations = Stations(fp)

    origin = stations.find("FRFEV")
    destination = stations.find("FRJFU")

    distance = origin.distance_to(destination)

    assert distance > 456
    assert distance < 457
