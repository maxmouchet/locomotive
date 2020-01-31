import datetime as dt
import logging
from typing import Any, List

import pytz
import requests

from ..models import BoardEntry, Transport
from ..stores import Stations
from .client import BoardClient
from .requests import BoardRequest


class Client(BoardClient):
    """
    Client for the www.garesetconnexions.sncf/fr/train-time API.
    """

    ENDPOINT = "https://www.garesetconnexions.sncf/fr/train-times"
    TZ = pytz.timezone("Europe/Paris")

    def __init__(self, stations: Stations) -> None:
        self.logger = logging.getLogger(__name__)
        self.stations = stations

    def request(self, tvs_id: str, type_: str) -> Any:
        url = f"{self.ENDPOINT}/{tvs_id}/{type_}"
        # pylint: disable=no-member
        res = requests.get(url, timeout=10)

        self.logger.debug(res.request.headers)
        self.logger.debug(res.request.url)
        self.logger.debug(res.request.body)
        self.logger.debug(res.content)

        res.raise_for_status()
        return res.json()

    def board_request(self, req: BoardRequest) -> List[BoardEntry]:
        res = self.request(req.station.sncf_tvs_id, req.type_)
        return self.parse_response(res)

    def parse_response(self, res: dict) -> List[BoardEntry]:
        return [self.__to_entry(x) for x in res["trains"]]

    def __to_entry(self, obj: dict) -> BoardEntry:
        tofrom = self.stations.find_or_raise(obj["origdest"])
        transport = Transport("", obj["type"], obj["num"], "")
        time = self.__parse_time(obj["heure"])
        delay = self.__parse_delay(obj["retard"])
        return BoardEntry(tofrom, transport, time, delay, obj["voie"])

    def __parse_delay(self, s: str) -> int:
        # TODO: Is is really that ?
        if s:
            hours, minutes = int(s[:2]), int(s[2:])
            return hours * 60 + minutes
        return 0

    def __parse_time(self, s: str) -> dt.datetime:
        today = dt.date.today()
        hour, minute = [int(x) for x in s.split(":")]
        time = dt.datetime(today.year, today.month, today.day, hour, minute)
        return self.TZ.localize(time)
