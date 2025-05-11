from flights_service.adapters.abc import SearchAdapter
from flights_service.models.offer import Offer
from flights_service.models.quote import Quote
from flights_service.models.search_session import SearchSession
from flights_service.repositories.search_session.abc import SearchSessionRepository


class SearchService:
    def __init__(
        self,
        search_adapter: SearchAdapter,
        session_repo: SearchSessionRepository,
    ):
        self.search_adapter = search_adapter
        self.session_repo = session_repo

    def do_search(self) -> SearchSession:
        session = self.session_repo.create_session()

        upstream_session = self.search_adapter.create_session()
        while offer_batch := upstream_session.get_offers():
            session.put_offers(offer_batch)

        return session

    def quote_from_offer(self, offer: Offer) -> Quote:
        return self.search_adapter.quote_from_offer(offer)
