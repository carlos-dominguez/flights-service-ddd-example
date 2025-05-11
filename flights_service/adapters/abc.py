from abc import ABC, abstractmethod

from flights_service.models.offer import Offer
from flights_service.models.quote import Quote


class UpstreamSession(ABC):
    @abstractmethod
    def get_offers(self) -> list[Offer]: ...


class SearchAdapter(ABC):
    @abstractmethod
    def create_session(self) -> UpstreamSession: ...

    @staticmethod
    def quote_from_offer(offer: Offer) -> Quote:
        return Quote(
            id=None,
            remote_id=offer.remote_id,
            slices=offer.slices,
            currency=offer.currency,
            total_amount=offer.total_amount,
        )
