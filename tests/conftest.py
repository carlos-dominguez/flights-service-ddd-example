import pytest
from redis import Redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flights_service.adapters.abc import SearchAdapter
from flights_service.adapters.test import TestSearchAdapter
from flights_service.db_mapper import mapper_registry
from flights_service.repositories.airline.abc import AirlineRepository
from flights_service.repositories.airline.sqlalchemy import SQLAlchemyAirlineRepository
from flights_service.repositories.quote.sqlalchemy import QuoteRepository
from flights_service.repositories.search_session.abc import SearchSessionRepository
from flights_service.repositories.search_session.redis import (
    RedisSearchSessionRepository,
)
from flights_service.services.search import SearchService


@pytest.fixture
def engine():
    engine = create_engine(
        "postgresql+psycopg://postgres:notsecure@localhost:5432/postgres"
    )
    mapper_registry.metadata.create_all(engine)
    yield engine


@pytest.fixture
def redis():
    yield Redis()


@pytest.fixture
def session(engine):
    sm = sessionmaker(engine)
    with sm.begin() as session:
        yield session


@pytest.fixture
def airline_repo(session):
    yield SQLAlchemyAirlineRepository(session)


@pytest.fixture
def search_adapter(airline_repo):
    yield TestSearchAdapter(airline_repo)


@pytest.fixture
def search_session_repo(redis, airline_repo):
    yield RedisSearchSessionRepository(redis, airline_repo)


@pytest.fixture
def quote_repo(session):
    yield QuoteRepository(session)


@pytest.fixture
def search_service(search_adapter, search_session_repo):
    yield SearchService(search_adapter, search_session_repo)
