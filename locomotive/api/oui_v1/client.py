"""
Client for the oui.sncf/proposition/rest/search-travels/outward API.
"""

import datetime as dt
from typing import List

import requests

# Old structure... oui_v2 client is much cleaner
from ...models import Journey, Passenger, Proposal, Segment, Station
from .types import SNCF_DATE_FORMAT, Location
from .types import Passenger as SNCFPassenger
from .types import PassengerProfile, SNCFTravelRequest, TravelClass


class Client:

    ENDPOINT = "https://www.oui.sncf/proposition/rest/search-travels/outward"
    ORIGIN = "https://www.oui.sncf"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"

    def __init__(self, stations):
        self.stations = stations

    def request(self, req: SNCFTravelRequest) -> requests.Response:
        headers = {
            "Origin": self.ORIGIN,
            "Referer": self.ORIGIN,
            "User-Agent": self.USER_AGENT,
        }

        res = requests.post(
            self.ENDPOINT, headers=headers, json=req.sncf_dict(), timeout=10
        )
        res.raise_for_status()
        return res

    def travel_request(
        self,
        origin_station: Station,
        destination_station: Station,
        passengers: List[Passenger],
        date: dt.datetime,
        travel_class: str,
    ) -> List[Journey]:
        # TODO: Naming consistency (origin/departure, ...)
        passengers = [
            SNCFPassenger(PassengerProfile.ADULT, passenger.age)
            for passenger in passengers
        ]

        origin = Location.from_station_code(origin_station.sncf_id)
        destination = Location.from_station_code(destination_station.sncf_id)
        travel_class = TravelClass.from_str(travel_class)

        res = self.request(
            SNCFTravelRequest(origin, destination, passengers, date, travel_class)
        )

        # import json
        # print(res.json().keys())
        # print(json.dumps(res.json()["trainProposals"][0], indent=2))

        return list(map(self.__to_journey, res.json()["trainProposals"]))

    def __to_journey(self, obj: dict) -> Journey:
        return Journey(
            segments=list(map(self.__to_segment, obj["segments"])),
            proposals=list(map(self.__to_proposal, obj["priceProposals"])),
        )

    def __to_segment(self, obj: dict) -> Segment:
        return Segment(
            train_label=obj["transporter"],
            train_number=obj["trainNumber"],
            departure_station=self.stations.find(obj["originStationCode"]),
            destination_station=self.stations.find(obj["destinationStationCode"]),
            departure_date=dt.datetime.strptime(obj["departureDate"], SNCF_DATE_FORMAT),
            arrival_date=dt.datetime.strptime(obj["arrivalDate"], SNCF_DATE_FORMAT),
        )

    def __to_proposal(self, obj: dict) -> Segment:
        # TODO: Currency
        return Proposal(flexibility_level=obj["type"], price=obj["amount"])
