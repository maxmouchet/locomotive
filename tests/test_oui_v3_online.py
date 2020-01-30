import datetime as dt
import json

import pytz
from locomotive.api.abstract import TravelRequest
from locomotive.api.oui_v3 import Client
from locomotive.models import Passenger
from locomotive.stores import Stations

stations = Stations()
client = Client(stations)


def test_travel_request_1():
    tz = pytz.timezone("Europe/Paris")
    date = tz.localize((dt.datetime.now() + dt.timedelta(days=1)).replace(hour=2))
    req = TravelRequest(
        stations.find("Paris"),
        stations.find("Lyon"),
        [Passenger.dummy()],
        date,
        "second",
    )
    res = client.travel_request(req)
    assert len(res) > 0
