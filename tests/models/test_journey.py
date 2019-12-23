import datetime as dt
import os

import pytest

from locomotive.models.journey import Journey, Proposal, Segment
from locomotive.stores import Stations


@pytest.fixture
def segments():
    fp = os.path.join(os.path.dirname(__file__), "..", "test-stations.csv")
    stations = Stations(fp)
    origin_station = stations.find("FRFEV")
    destination_station = stations.find("FRJFU")
    segments = [
        Segment(
            "TER",
            "0000",
            origin_station,
            destination_station,
            dt.datetime(2019, 1, 1, 0),
            dt.datetime(2019, 1, 1, 1, 30),
        ),
        Segment(
            "TER",
            "0000",
            origin_station,
            destination_station,
            dt.datetime(2019, 1, 1, 1, 45),
            dt.datetime(2019, 1, 1, 2, 15),
        ),
    ]
    return segments


@pytest.fixture
def proposals():
    return [Proposal("NOFLEX", 10.0)]


def test_journey_dates(segments, proposals):
    journey = Journey(segments, proposals)
    assert journey.departure_date == dt.datetime(2019, 1, 1, 0)
    assert journey.arrival_date == dt.datetime(2019, 1, 1, 2, 15)


def test_journey_duration(segments, proposals):
    journey = Journey(segments, proposals)
    assert journey.duration == dt.timedelta(hours=2, minutes=15)


def test_journey_stations(segments, proposals):
    journey = Journey(segments, proposals)
    assert journey.departure_station == segments[0].departure_station
    assert journey.destination_station == segments[-1].destination_station
