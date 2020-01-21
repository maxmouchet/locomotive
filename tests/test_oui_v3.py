import json

from locomotive.api.oui_v3 import Client
from locomotive.stores import Stations

stations = Stations()
client = Client(stations)


def test_travel_request_1():
    with open("tests/traces/ios_oui6904_frlys_frnte.res.json") as f:
        res = json.load(f)
    journeys = client.parse_response(res)
    assert len(journeys) == 6
    assert journeys[1].segments[1].transport.equipment == "TGN"
    assert journeys[1].segments[1].transport.label == "TGV"
    assert journeys[1].segments[1].transport.number == "5224"
    assert journeys[1].segments[1].transport.type == "TRAIN"
