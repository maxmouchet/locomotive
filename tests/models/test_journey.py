import datetime as dt
import os

import pytest
from locomotive.diff import JourneyDiff, JourneyDiffType, journeys_diff
from locomotive.models import Journey, Proposal, Segment, Transport
from locomotive.stores import Stations


@pytest.fixture
def segments():
    fp = os.path.join(os.path.dirname(__file__), "..", "test-stations.sqlite3")
    stations = Stations(fp)
    departure_station = stations.find("FRFEV")
    arrival_station = stations.find("FRJFU")
    segments = [
        Segment(
            Transport("TER", "TER", "0000", "TRAIN"),
            departure_station,
            arrival_station,
            dt.datetime(2019, 1, 1, 0),
            dt.datetime(2019, 1, 1, 1, 30),
        ),
        Segment(
            Transport("TER", "TER", "0000", "TRAIN"),
            departure_station,
            arrival_station,
            dt.datetime(2019, 1, 1, 1, 45),
            dt.datetime(2019, 1, 1, 2, 15),
        ),
    ]
    return tuple(segments)


@pytest.fixture
def proposals():
    return tuple([Proposal("FLEX", 32.10), Proposal("NOFLEX", 10.0)])


def test_journey_base(segments, proposals):
    journey = Journey(segments, proposals)
    assert journey == journey
    assert journey is journey
    # Should be hashable
    set([journey])


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
    assert journey.arrival_station == segments[-1].arrival_station


def test_journey_lowest_price(segments, proposals):
    journey = Journey(segments, proposals)
    assert journey.lowest_price == 10.0


# TODO: Move in dedicated file
def test_journey_diff(segments, proposals):
    old = Journey(segments, proposals)
    new = Journey(segments, proposals)
    diff = JourneyDiff(old, new)
    assert diff.diff_type == JourneyDiffType.NoChange
    assert diff.price_diff == 0.0

    old = Journey(segments, proposals)
    new = None
    diff = JourneyDiff(old, new)
    assert diff.diff_type == JourneyDiffType.Removed
    assert diff.price_diff == None

    old = None
    new = Journey(segments, proposals)
    diff = JourneyDiff(old, new)
    assert diff.diff_type == JourneyDiffType.Added
    assert diff.price_diff == None

    old = None
    new = None
    diff = JourneyDiff(old, new)
    assert diff.diff_type == None
    assert diff.price_diff == None

    old = Journey(segments, [Proposal("", 10.0)])
    new = Journey(segments, [])
    diff = JourneyDiff(old, new)
    assert diff.diff_type == JourneyDiffType.Unavailable
    assert diff.price_diff == None

    old = Journey(segments, [])
    new = Journey(segments, [Proposal("", 10.0)])
    diff = JourneyDiff(old, new)
    assert diff.diff_type == JourneyDiffType.Available
    assert diff.price_diff == None

    old = Journey(segments, [])
    new = Journey(segments, [])
    diff = JourneyDiff(old, new)
    assert diff.diff_type == JourneyDiffType.NoChange
    assert diff.price_diff == None

    old = Journey(segments, [Proposal("", 10.0)])
    new = Journey(segments, [Proposal("", 11.1)])
    diff = JourneyDiff(old, new)
    assert diff.diff_type == JourneyDiffType.HigherPrice
    assert pytest.approx(diff.price_diff, 1.1)

    old = Journey(segments, [Proposal("", 12.32)])
    new = Journey(segments, [Proposal("", 10.0)])
    diff = JourneyDiff(old, new)
    assert diff.diff_type == JourneyDiffType.LowerPrice
    assert pytest.approx(diff.price_diff, -2.32)


def test_journeys_diff(segments, proposals):
    old_journeys = [
        Journey(segments, proposals),
        Journey(segments[0:1], [Proposal("", 10.0)]),
        Journey(segments[1:2], [Proposal("", 10.0)]),
    ]

    new_journeys = [
        Journey(segments, proposals),
        Journey(segments[0:1], [Proposal("", 12.0)]),
    ]

    diffs = journeys_diff(old_journeys, new_journeys)

    assert len(diffs) == 3
    # TODO: This depends on dict values iteration order...
    assert diffs[0].diff_type == JourneyDiffType.NoChange
    assert diffs[1].diff_type == JourneyDiffType.HigherPrice
    assert diffs[2].diff_type == JourneyDiffType.Removed
