from abc import ABC, abstractmethod

from flights_service.models.offer import Offer


class SearchSession(ABC):
    id: str

    @abstractmethod
    def put_offers(self, offers: list[Offer]): ...

    @property
    @abstractmethod
    def offers(self) -> list[Offer]: ...
