import datetime as dt
import logging
import re
from typing import Any, List

import requests
from money.currency import Currency
from money.money import Money

from ..models import Journey, Proposal, Segment, Transport
from ..stores import Stations
from .client import TravelClient
from .requests import TravelRequest


# TODO: Move somewhere else (in TravelRequest ?)
def strftime_sncf(date: dt.datetime) -> str:
    if not date.tzinfo:
        raise ValueError("`date` must be tz-aware")
    s = date.strftime("%Y-%m-%dT%H:%M:%S.000%z")
    s = s[:-2] + ":" + s[-2:]
    return s


class Client(TravelClient):
    """
    Client for the wshoraires.oui.sncf V3 API
    """

    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
    ENDPOINT = "https://wshoraires.oui.sncf/m730/vmd/maq/v3/proposals/train"
    USER_AGENT = "OUI.sncf/73.2.0 CFNetwork/1125.2 Darwin/19.4.0"

    def __init__(self, stations: Stations) -> None:
        self.logger = logging.getLogger(__name__)
        self.stations = stations

    def request(self, json: dict) -> Any:
        headers = {
            "Accept": "application/json",
            "Accept-Language": "fr-FR",
            "Content-Type": "application/json;charset=UTF8",
            "Cookie": "",
            "User-Agent": self.USER_AGENT,
            "application-user-agent": "iPhone (iOS 13.4.1) - [320x568@2x]",
            "x-vsc-locale": "fr_FR",
            "X-Device-Class": "SMARTPHONE",
            "X-Device-Type": "IOS",
            "X-HR-Version": "73.2",
            "x-vsc-currency": "EUR",
            "x-vsc-token": "",
            "x-screen-density-qualifier": "xhdpi",
        }

        # pylint: disable=no-member
        res = requests.post(self.ENDPOINT, headers=headers, json=json, timeout=10)

        self.logger.debug(res.request.headers)
        self.logger.debug(res.request.url)
        self.logger.debug(res.request.body)
        self.logger.debug(res.content)

        if res.status_code == 404:
            # {"code":"ERR-0102","label":"empty travel result"}
            return {"journeys": []}

        res.raise_for_status()
        return res.json()

    def travel_request(self, req: TravelRequest) -> List[Journey]:
        passengers_dict = []
        for passenger in req.passengers:
            commercial_card = {"type": "NO_CARD"}
            if passenger.commercial_card_type:
                commercial_card = {
                    "type": passenger.commercial_card_type,
                    "number": passenger.commercial_card_number,
                }

            passengers_dict.append(
                {
                    "advantageCode": None,
                    "age": passenger.age,
                    "ageRank": "ADULT",  # TODO
                    "birthday": passenger.birthday.strftime("%Y-%m-%d"),
                    "commercialCard": commercial_card,
                    "fidNumber": passenger.fidelity_card_number,
                    "type": "HUMAN",
                }
            )

        sncf_dict = {
            "departureTown": {"codes": {"resarail": req.departure_station.sncf_id}},
            "destinationTown": {"codes": {"resarail": req.arrival_station.sncf_id}},
            "features": ["TRAIN_AND_BUS"],
            "outwardDate": strftime_sncf(req.date),
            "passengers": passengers_dict,
            "travelClass": req.travel_class.upper(),
        }

        # TODO: Handle cancelled, full trains (no price ?)
        # TODO: Show class in formatter
        res = self.request(sncf_dict)
        return self.parse_response(res)

    def parse_response(self, res: dict) -> List[Journey]:
        return [self.__to_journey(x) for x in res["journeys"]]

    def __to_journey(self, obj: dict) -> Journey:
        return Journey(
            segments=tuple(map(self.__to_segment, obj["segments"])),
            proposals=tuple(map(self.__to_proposal, obj["proposals"])),
        )

    def __to_segment(self, obj: dict) -> Segment:
        # : separated TZ doesn't work with Python < 3.7
        # 2019-06-23T16:18:00.000+02:00 -> 2019-06-23T16:18:00.000+0200
        departure_date_str = re.sub(
            r"([+-])(\d{2}):(\d{2})$", r"\g<1>\g<2>\g<3>", obj["departureDate"]
        )
        arrival_date_str = re.sub(
            r"([+-])(\d{2}):(\d{2})$", r"\g<1>\g<2>\g<3>", obj["arrivalDate"]
        )
        transport = Transport(
            equipment=obj["transport"]["equipment"],
            label=obj["transport"]["label"],
            number=obj["transport"]["number"],
            type=obj["transport"]["type"],
        )
        return Segment(
            transport=transport,
            departure_station=self.stations.find_or_raise(
                obj["departureStation"]["info"]["miInfo"]["code"]
            ),
            arrival_station=self.stations.find_or_raise(
                obj["arrivalStation"]["info"]["miInfo"]["code"]
            ),
            departure_date=dt.datetime.strptime(departure_date_str, self.DATE_FORMAT),
            arrival_date=dt.datetime.strptime(arrival_date_str, self.DATE_FORMAT),
        )

    def __to_proposal(self, obj: dict) -> Proposal:
        return Proposal(
            flexibility_level=obj["flexibility"],
            price=Money(str(obj["price"]["value"]), Currency(obj["price"]["currency"])),
        )
