import os
from locomotive.models.stations import Stations

def test_can_load_default_data_if_no_path_provided():
    stations = Stations()
    assert len(stations.df) > 0

    
def test_can_load_data():
    fp = os.path.join(os.path.dirname(__file__), "test-stations.csv")
    stations = Stations(fp)
    assert len(stations.df) == 10

    
def test_can_find_station_by_name():
    fp = os.path.join(os.path.dirname(__file__), "test-stations.csv")
    stations = Stations(fp)

    station = stations.find("Le Porage")

    assert station is not None


def test_return_none_when_cannot_find_station_by_a_given_name():
    fp = os.path.join(os.path.dirname(__file__), "test-stations.csv")
    stations = Stations(fp)

    station = stations.find("This station doesn't exist")

    assert station is None


def test_can_find_station_by_id():
    fp = os.path.join(os.path.dirname(__file__), "test-stations.csv")
    stations = Stations(fp)

    station = stations.find("FRFEV")

    assert station is not None
    

def test_return_none_when_cannot_find_station_by_a_given_id():
    fp = os.path.join(os.path.dirname(__file__), "test-stations.csv")
    stations = Stations(fp)

    station = stations.find("This station ID doesn't exist")

    assert station is None


def test_can_retrieve_coords():
    fp = os.path.join(os.path.dirname(__file__), "test-stations.csv")
    stations = Stations(fp)

    station = stations.find("FRFEV")

    coords = station.coords

    assert len(coords) == 2

    assert coords[0] == 44.9288345
    assert coords[1] == -0.4963844

    
def test_can_compute_distance_between_two_stations():
    fp = os.path.join(os.path.dirname(__file__), "test-stations.csv")
    stations = Stations(fp)

    origin = stations.find("FRFEV")
    destination = stations.find("FRJFU")

    distance = origin.distance_to(destination)

    assert distance > 456
    assert distance < 457
