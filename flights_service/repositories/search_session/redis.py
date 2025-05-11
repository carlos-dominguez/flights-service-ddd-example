import uuid
from typing import Optional

from redis import Redis

from flights_service.models.offer import Offer
from flights_service.models.search_session import SearchSession
from flights_service.repositories.airline.abc import AirlineRepository
from flights_service.repositories.search_session.abc import SearchSessionRepository
from flights_service.schemas.session import OfferSchema


class RedisSearchSessionRepository(SearchSessionRepository):
    def __init__(self, redis_client: Redis, airline_repo: AirlineRepository) -> None:
        self._redis = redis_client
        self._airline_repo = airline_repo
        self._sessions_key = "sessions"

    def create_session(self) -> SearchSession:
        id = str(uuid.uuid4())
        # Add session ID to a set of all sessions
        self._redis.sadd(self._sessions_key, id)
        return RedisSearchSession(id, self._redis, self._airline_repo)

    def get_session_by_id(self, session_id: str) -> Optional[SearchSession]:
        # Check if session exists
        if not self._redis.sismember(self._sessions_key, session_id):
            raise KeyError(f"Session with ID {session_id} not found")

        return RedisSearchSession(session_id, self._redis, self._airline_repo)


class RedisSearchSession(SearchSession):
    def __init__(
        self, id: str, redis_client: Redis, airline_repo: AirlineRepository
    ) -> None:
        self.id = id
        self._redis = redis_client
        self._airline_repo = airline_repo

        self._session_key = f"session:{id}"
        self._offers_key = f"{self._session_key}:offers"
        self._id_mapping_key = f"{self._session_key}:id_mapping"

    def _get_new_id(self, remote_id: str) -> str:
        new_id = str(uuid.uuid4())
        # Store mapping from internal ID to remote ID
        self._redis.hset(self._id_mapping_key, new_id, remote_id)
        # Store mapping from remote ID to internal ID
        self._redis.hset(f"{self._id_mapping_key}:reverse", remote_id, new_id)
        return new_id

    def put_offers(self, offers: list[Offer]) -> None:
        # Convert offers to OfferWithID and store them in Redis
        pipe = self._redis.pipeline()

        for offer in offers:
            new_id = self._get_new_id(offer.remote_id)
            offer.id = new_id

            # Serialize the offer to JSON using OfferSchema
            offer_schema = OfferSchema.from_domain(offer)
            offer_json = offer_schema.model_dump_json()

            # Store the serialized offer in Redis with the key pattern "session:{id}:offers:{offer_id}"
            offer_key = f"{self._offers_key}:{new_id}"
            pipe.set(offer_key, offer_json)

            # Add the offer ID to a set for easy retrieval of all offers
            pipe.sadd(self._offers_key, new_id)

        pipe.execute()

    @property
    def offers(self) -> list[Offer]:
        # Get all offer IDs from the set
        offer_ids = self._redis.smembers(self._offers_key)
        if not offer_ids:
            return []

        # Get all offers in a single pipeline
        pipe = self._redis.pipeline()
        for offer_id in offer_ids:
            offer_key = f"{self._offers_key}:{offer_id.decode('utf-8')}"
            pipe.get(offer_key)

        offer_jsons = pipe.execute()

        # Deserialize offers from JSON
        result = []
        for i, offer_json in enumerate(offer_jsons):
            if offer_json:
                offer_schema = OfferSchema.model_validate_json(offer_json, by_name=True)
                offer = offer_schema.to_domain(self._airline_repo)
                result.append(offer)

        return result
