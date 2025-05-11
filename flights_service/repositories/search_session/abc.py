from abc import ABC, abstractmethod

from flights_service.models.search_session import SearchSession


class SearchSessionRepository(ABC):
    @abstractmethod
    def create_session(self) -> SearchSession: ...

    @abstractmethod
    def get_session_by_id(self, str) -> SearchSession: ...
