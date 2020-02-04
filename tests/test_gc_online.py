import datetime as dt

import pytz
from locomotive.api.gc import Client
from locomotive.api.requests import BoardRequest
from locomotive.stores import Stations

stations = Stations()
client = Client(stations)


def test_board_request_1():
    req = BoardRequest(stations.find("Lyon Part-Dieu"), "departure")
    res = client.board_request(req)
    assert len(res) > 0

    req = BoardRequest(stations.find("Lyon Part-Dieu"), "arrival")
    res = client.board_request(req)
    assert len(res) > 0
