import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import NoInspectionAvailable

from flights_service.repositories.search_session.redis import (
    RedisSearchSessionRepository,
)


def test_search(search_service, search_session_repo, quote_repo):
    """
    This test demonstrates how we can apply different persistence strategies to offers and quotes, despite their
    domain models being nearly identical (Quote being fully defined as `class Quote(Offer): pass`):

    - We perform a search and show that the entire session can be saved to/loaded from Redis.
    - We show that offers are *not* tracked by SQLAlchemy.
    - We turn an offer into a quote in the most obvious way possible, using *exactly* the same slices.
    - We show that quotes can be saved and loaded via SQLAlchemy session.

    To run this test, start the `postgres` and `redis` services in docker-compose.yaml.
    """

    search_session = search_service.do_search()

    assert isinstance(search_session_repo, RedisSearchSessionRepository)
    search_session_reloaded = search_session_repo.get_session_by_id(search_session.id)

    assert search_session_reloaded.id == search_session.id
    assert search_session_reloaded is not search_session

    offer = search_session_reloaded.offers[0]
    with pytest.raises(NoInspectionAvailable):
        inspect(offer)

    quote = search_service.quote_from_offer(offer)
    assert quote.slices[0] is offer.slices[0]
    assert quote.slices[1] is offer.slices[1]

    assert quote.id is None
    assert inspect(quote).transient

    quote_repo.add_quote(quote)
    assert quote.id is not None
    assert inspect(quote).persistent

    quote_reloaded = quote_repo.get_quote_by_id(quote.id)
    assert quote_reloaded is quote
