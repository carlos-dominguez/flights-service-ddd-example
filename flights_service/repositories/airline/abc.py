from abc import ABC, abstractmethod

from flights_service.models.airline import Airline


class AirlineRepository(ABC):
    @abstractmethod
    def get_airline_by_iata_code(self, iata_code: str) -> Airline: ...
