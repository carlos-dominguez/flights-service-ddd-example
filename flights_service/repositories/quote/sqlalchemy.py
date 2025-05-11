from sqlalchemy.orm import Session

from flights_service.models.quote import Quote


class QuoteRepository:
    def __init__(self, session: Session):
        self._session = session

    def add_quote(self, quote: Quote) -> Quote:
        self._session.add(quote)
        self._session.flush()
        return quote

    def get_quote_by_id(self, quote_id: int) -> Quote:
        return self._session.get_one(Quote, quote_id)  # type:ignore
