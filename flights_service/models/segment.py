from datetime import datetime

from flights_service.models.airline import Airline


class Segment:
    def __init__(
        self,
        marketing_airline: Airline,
        operating_airline: Airline,
        flight_number: str,
        departure_time: datetime,
        arrival_time: datetime,
    ):
        self.marketing_airline = marketing_airline
        self.operating_airline = operating_airline
        self.flight_number = flight_number
        self.departure_time = departure_time
        self.arrival_time = arrival_time
