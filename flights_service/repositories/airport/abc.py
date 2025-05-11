from abc import ABC, abstractmethod

from flights_service.models.airport import Airport


class AirportRepository(ABC):
    @abstractmethod
    def get_airport_by_iata_code(self, iata_code: str) -> Airport: ...
