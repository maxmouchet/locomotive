import requests

from .types import Location, Passenger, PassengerProfile, SNCFTravelRequest, TravelClass


class Client:

    ENDPOINT = "https://www.oui.sncf/proposition/rest/search-travels/outward"

    def request(self, req: SNCFTravelRequest) -> requests.Response:
        return requests.post(self.ENDPOINT, json=req.sncf_dict())

    def simple_request(
        self, age, origin_station, destination_station, date, travel_class
    ):
        passengers = [Passenger(PassengerProfile.ADULT, age)]
        origin = Location.from_station_code(origin_station["sncf_id"])
        destination = Location.from_station_code(destination_station["sncf_id"])
        travel_class = TravelClass.from_str(travel_class)
        return self.request(
            SNCFTravelRequest(origin, destination, passengers, date, travel_class)
        )