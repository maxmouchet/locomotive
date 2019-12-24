"""
Client for the wshoraires.oui.sncf API
"""

import datetime as dt
import logging
import re
from typing import Dict, List

import requests

from ...models import Journey, Passenger, Proposal, Segment, Station
from ...stores import Stations


class Client:

    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
    ENDPOINT = "https://wshoraires.oui.sncf/m670/vmd/maq/v2/proposals/train"
    USER_AGENT = "OUI.sncf/61.2 CFNetwork/978.0.7 Darwin/18.5.0"

    def __init__(self, stations: Stations) -> None:
        self.logger = logging.getLogger(__name__)
        self.stations = stations

    def request(self, json: dict) -> Dict:
        headers = {
            "User-Agent": self.USER_AGENT,
            "x-vsc-locale": "fr_FR",
            "x-Device-Type": "IOS",
        }

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

    def travel_request(
        self,
        departure_station: Station,
        arrival_station: Station,
        passengers: List[Passenger],
        date: dt.datetime,
        travel_class: str,
    ) -> List[Journey]:

        passengers_dict = []
        for passenger in passengers:
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
            "departureTownCode": departure_station.sncf_id,
            "destinationTownCode": arrival_station.sncf_id,
            "directTravel": True,
            "features": [],
            # TODO: microseconds + timezone (needs to be present)
            "outwardDate": date.strftime("%Y-%m-%dT%H:%M:%S.000+02:00"),
            "passengers": passengers_dict,
            "token": "",
            "travelClass": travel_class.upper(),
        }

        # TODO: Handle full trains (no price ?)
        # TODO: Show class in formatter
        res = self.request(sncf_dict)
        return list(map(self.__to_journey, res["journeys"]))

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
        return Segment(
            train_label=obj["trainLabel"],
            train_number=obj["trainNumber"],
            departure_station=self.stations.find_or_raise(
                obj["departureStation"]["resarailCode"]
            ),
            arrival_station=self.stations.find_or_raise(
                obj["destinationStation"]["resarailCode"]
            ),
            departure_date=dt.datetime.strptime(departure_date_str, self.DATE_FORMAT),
            arrival_date=dt.datetime.strptime(arrival_date_str, self.DATE_FORMAT),
        )

    def __to_proposal(self, obj: dict) -> Proposal:
        return Proposal(flexibility_level=obj["flexibilityLevel"], price=obj["price"])
