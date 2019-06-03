"""
Python objects mapping to SNCF API types.
"""

import datetime as dt
from enum import Enum, auto
from typing import List

SNCF_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"


class PassengerProfile(Enum):
    ADULT = auto()
    # TODO: Add other types


class Passenger:
    def __init__(self, profile: PassengerProfile, age: int):
        self.profile = profile
        self.age = age

        # Non-mandatory properties
        self.traveler_id = None
        self.birth_date = None
        self.fidelity_card_type = "NONE"
        self.commercial_card_number = ""
        self.commercial_card_type = "NONE"
        self.promo_code = None
        self.last_name = None
        self.first_name = None
        self.phone_number = None
        self.han_information = None

    def sncf_dict(self):
        return {
            "travelerId": self.traveler_id,
            "profile": self.profile.name,
            "age": self.age,
            "birthDate": self.birth_date,
            "fidelityCardType": self.fidelity_card_type,
            "commercialCardNumber": self.commercial_card_number,
            "commercialCardType": self.commercial_card_type,
            "promoCode": self.promo_code,
            "lastName": self.last_name,
            "firstName": self.first_name,
            "phoneNumer": self.phone_number,
            "hanInformation": self.han_information,
        }


class LocationType(Enum):
    G = auto()  # Means 'Gare' ?
    # TODO: Implement other types


class Location:
    def __init__(self, t: LocationType, station_code: str):
        self.t = t
        self.station_code = station_code

        # Non-mandatory variables
        self.id = None
        self.label = None
        self.longitude = None
        self.latitude = None
        self.country = None
        self.station_label = None

    @classmethod
    def from_station_code(cls, station_code: str):
        return cls(LocationType.G, station_code)

    def sncf_dict(self):
        return {
            "id": self.id,
            "label": self.label,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "type": self.t.name,
            "country": self.country,
            "stationCode": self.station_code,
            "stationLabel": self.station_label,
        }


class TravelClass(Enum):
    FIRST = auto()
    SECOND = auto()
    # TODO: Implement other types

    @classmethod
    def from_str(cls, str):
        return cls[str.upper()]


class SNCFTravelRequest:
    def __init__(
        self,
        origin: Location,
        destination: Location,
        passengers: List[Passenger],
        departure_date: dt.datetime,
        travel_class: TravelClass,
    ):
        self.origin_location = origin
        self.destination_location = destination
        self.passengers = passengers
        self.departure_date = departure_date
        self.travel_class = travel_class

        # These fields are not actually used in the request, but needs to be specified
        # May as well put 'Jambon' in there
        self.origin = origin.station_code
        self.origin_code = origin.station_code
        self.destination = destination.station_code
        self.destination_code = destination.station_code

        # Non-mandatory or default variables
        self.via = None
        self.via_code = None
        self.via_location = None
        self.direct_travel = False  # Force 'sans correspondance' ?
        self.asymmetrical = False
        self.professional = False
        self.customer_account = False
        self.one_way_travel = True
        self.return_date = None
        self.country = "FR"
        self.language = "fr"
        self.bus_best_price_operator = None
        self.animals = []
        self.bike = "NONE"
        self.with_reclining_seat = False
        self.physical_space = None
        self.fares = []
        self.with_best_prices = False
        self.highlighted_travel = None
        self.next_or_previous = False
        self.source = "FORM_SUBMIT"
        self.target_price = None
        self.han = False
        self.outward_schedule_type = "BY_DEPARTURE_DATE"
        self.inward_schedule_type = "BY_DEPARTURE_DATE"
        self.currency = None

    def sncf_dict(self):
        return {
            "origin": self.origin,
            "origin_code": self.origin_code,
            "origin_location": self.origin_location.sncf_dict(),
            "destination": self.destination,
            "destination_code": self.destination_code,
            "destination_location": self.destination_location.sncf_dict(),
            "via": self.via,
            "viaCode": self.via_code,
            "viaLocation": self.via_location,
            "directTravel": self.direct_travel,
            "asymmetrical": self.asymmetrical,
            "professional": self.professional,
            "customerAccount": self.customer_account,
            "oneWayTravel": self.one_way_travel,
            "departureDate": self.departure_date.strftime(SNCF_DATE_FORMAT),
            "returnDate": self.return_date.strftime(SNCF_DATE_FORMAT)
            if self.return_date
            else None,
            "travelClass": self.travel_class.name,
            "country": self.country,
            "language": self.language,
            "busBestPriceOperator": self.bus_best_price_operator,
            "passengers": [passenger.sncf_dict() for passenger in self.passengers],
            "animals": [animal.sncf_dict() for animal in self.animals],
            "bike": self.bike,
            "withRecliningSeat": self.with_reclining_seat,
            "physicalSpace": self.physical_space,
            "fares": self.fares,
            "withBestPrices": self.with_best_prices,
            "highlightedTravel": self.highlighted_travel,
            "nextOrPrevious": self.next_or_previous,
            "source": self.source,
            "targetPrice": self.target_price,
            "han": self.han,
            "outwardScheduleType": self.outward_schedule_type,
            "inwardScheduleType": self.inward_schedule_type,
            "currency": self.currency,
        }
